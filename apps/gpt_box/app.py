import logging

from h2o_wave import Q, main, app, copy_expando, handle_on, on
from llmbox.llms import GPT35Turbo, GPT4
from llmbox.chat import Chat, Message, Role

import cards

# Set up logging
logging.basicConfig(format='%(levelname)s:\t[%(asctime)s]\t%(message)s', level=logging.INFO)


@app('/')
async def serve(q: Q):
    """
    Main serving function.
    """

    try:
        # Initialize the app if not already
        if not q.app.initialized:
            await initialize_app(q)

        # Initialize the client if not already
        if not q.client.initialized:
            await initialize_client(q)

        # Update theme if toggled
        if q.args.theme_dark is not None and q.args.theme_dark != q.client.theme_dark:
            await update_theme(q)

        # Switch settings tab if clicked
        elif q.args.settings_tab:
            await settings(q)

        # Delegate query to query handlers
        elif await handle_on(q):
            pass

        # Handle fallback
        else:
            await handle_fallback(q)

    except Exception as error:
        await display_error(q, error=str(error))


async def initialize_app(q: Q):
    """
    Initialize the app.
    """

    logging.info('Initializing app')

    # Set initial argument values
    q.app.cards = ['tabs', 'chatbox', 'error']

    q.app.initialized = True


async def initialize_client(q: Q):
    """
    Initialize the client.
    """

    logging.info('Initializing client')

    # Set initial argument values
    q.client.theme = 'llmbox-dark'
    q.client.settings_tab = 'tab_model'
    q.client.model = 'gpt-4'
    q.client.max_tokens = 300
    q.client.temperature = 0.5
    q.client.top_p = 0.7

    # Initialize llm data
    q.client.api_key = None
    q.client.chat = Chat()

    # Add layouts and header
    q.page['meta'] = cards.meta
    q.page['header'] = cards.header

    # Add cards for the main page
    q.page['tabs'] = cards.tabs
    q.page['chatbox'] = cards.chatbox(chat=q.client.chat)

    # Check API
    try:
        q.client.llm = GPT4(api_key=q.client.api_key)
    except ValueError:
        q.page['meta'].dialog = cards.dialog_api

    q.client.initialized = True

    await q.page.save()


@on('save_api')
async def save_api(q: Q):
    """
    Save API key.
    """

    logging.info('Saving API key')

    # Check API key
    if q.args.api_key is None or q.args.api_key == '':
        await handle_fallback(q)
    else:
        # Save API key
        q.client.api_key = q.args.api_key

        # Initialize LLM
        if q.client.model == 'gpt-3.5-turbo':
            q.client.llm = GPT35Turbo(api_key=q.client.api_key)
        else:
            q.client.llm = GPT4(api_key=q.client.api_key)

        # Remove dialog
        q.page['meta'].dialog = None

        await q.page.save()


@on('update_theme')
async def update_theme(q: Q):
    """
    Update theme of app.
    """

    if q.client.theme == 'llmbox-light':
        logging.info('Updating theme to dark mode')

        # Update theme from light to dark mode
        q.page['meta'].theme = 'llmbox-dark'
        q.page['header'].icon_color = 'black'
        q.client.theme = 'llmbox-dark'
    else:
        logging.info('Updating theme to light mode')

        # Update theme from dark to light mode
        q.page['meta'].theme = 'llmbox-light'
        q.page['header'].icon_color = '#e5d5c0'
        q.client.theme = 'llmbox-light'

    await q.page.save()


@on('chat')
async def chat(q: Q):
    """
    Generate chat response from LLM.
    """

    logging.info('Generating chat response from LLM')

    # Add message to chat
    q.client.chat.add_message(message=Message(text=q.args.chat, role=Role.User))

    # Generate LLM response
    llm_response = q.client.llm.generate(
        chat=q.client.chat,
        max_tokens=q.client.max_tokens,
        temperature=q.client.temperature,
        top_p=q.client.top_p
    )

    # Add response to chat
    q.client.chat.add_message(message=Message(text=llm_response, role=Role.Assistant))

    # Update chat
    q.page['chatbox'] = cards.chatbox(chat=q.client.chat)

    await q.page.save()


@on('settings')
async def settings(q: Q):
    """
    Display settings.
    """

    if q.args.settings_tab:
        logging.info('Switching settings tab')

        # Copy settings tab to client
        copy_expando(q.args, q.client)
    else:
        logging.info('Displaying settings')

    # Dialog with settings
    q.page['meta'].dialog = cards.dialog_settings(
        settings_tab=q.client.settings_tab,
        model=q.client.model,
        max_tokens=q.client.max_tokens,
        temperature=q.client.temperature,
        top_p=q.client.top_p
    )

    await q.page.save()


@on('top_p')
@on('temperature')
@on('max_tokens_to_sample')
@on('model')
@on('new_api_key')
async def update_settings(q: Q):
    """
    Update settings.
    """

    logging.info('Updating settings')

    if q.args.new_api_key:
        # Save new API key
        q.client.api_key = q.args.new_api_key

        # Initialize LLM
        if q.client.model == 'gpt-3.5-turbo':
            q.client.llm = GPT35Turbo(api_key=q.client.api_key)
        else:
            q.client.llm = GPT4(api_key=q.client.api_key)
    elif q.args.model:
        # Save new model
        q.client.model = q.args.model

        # Initialize LLM
        if q.client.model == 'gpt-3.5-turbo':
            q.client.llm = GPT35Turbo(api_key=q.client.api_key)
        else:
            q.client.llm = GPT4(api_key=q.client.api_key)
    else:
        # Copy settings to client
        copy_expando(q.args, q.client)

    # Update settings change message
    q.page['meta'].dialog = cards.dialog_settings(
        settings_tab=q.client.settings_tab,
        model=q.client.model,
        max_tokens=q.client.max_tokens,
        temperature=q.client.temperature,
        top_p=q.client.top_p,
        save_message=True
    )

    await handle_fallback(q)


@on('restart')
async def restart(q: Q):
    """
    Restart chat.
    """

    logging.info('Restarting chat')

    # Reset chat
    q.client.chat = Chat()

    # Update chat
    q.page['chatbox'] = cards.chatbox(chat=q.client.chat)

    await q.page.save()


@on('dialog_settings.dismissed')
async def dismiss_dialog(q: Q):
    """
    Dismiss dialog.
    """

    logging.info('Dismissing dialog')

    # Remove dialog
    q.page['meta'].dialog = None

    await q.page.save()


def clear_cards(q: Q, card_names: list):
    """
    Clear cards from the page.
    """

    logging.info('Clearing cards')

    # Delete cards from the page
    for card_name in card_names:
        del q.page[card_name]


async def display_error(q: Q, error: str):
    """
    Display the error.
    """

    logging.error(error)

    # Clear all cards
    clear_cards(q, q.app.cards)

    # Format and display the error
    q.page['error'] = cards.crash_report(q)

    await q.page.save()


@on('reload')
async def reload_client(q: Q):
    """
    Reload the client.
    """

    logging.info('Reloading client')

    # Clear all cards
    clear_cards(q, q.app.cards)

    # Reload the client
    await initialize_client(q)


async def handle_fallback(q: Q):
    """
    Handle fallback cases.
    """

    logging.info('Adding fallback page')

    q.page['fallback'] = cards.fallback

    await q.page.save()
