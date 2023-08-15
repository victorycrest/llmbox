import logging

from h2o_wave import Q, main, app, copy_expando, handle_on, on
from llmbox.llms import Claude2
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
        elif q.args.theme_dark is not None and q.args.theme_dark != q.client.theme_dark:
            await update_theme(q)

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
    q.app.cards = ['chatbox', 'error']

    q.app.initialized = True


async def initialize_client(q: Q):
    """
    Initialize the client.
    """

    logging.info('Initializing client')

    # Set initial argument values
    q.client.theme_dark = True
    q.client.llm = Claude2()
    q.client.chat = Chat()

    # Add layouts, header and footer
    q.page['meta'] = cards.meta
    q.page['header'] = cards.header
    q.page['footer'] = cards.footer

    # Add cards for the main page
    q.page['chatbox'] = cards.chatbox(chat=q.client.chat)

    q.client.initialized = True

    await q.page.save()


async def update_theme(q: Q):
    """
    Update theme of app.
    """

    # Copy argument values to client
    copy_expando(q.args, q.client)

    if q.client.theme_dark:
        logging.info('Updating theme to dark mode')

        # Update theme from light to dark mode
        q.page['meta'].theme = 'llmbox-dark'
        q.page['header'].icon_color = 'black'
    else:
        logging.info('Updating theme to light mode')

        # Update theme from dark to light mode
        q.page['meta'].theme = 'llmbox-light'
        q.page['header'].icon_color = '#e5d5c0'

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
    llm_response = q.client.llm.generate(prompt=q.client.chat.generate_prompt_anthropic())

    # Add response to chat
    q.client.chat.add_message(message=Message(text=llm_response, role=Role.AI))

    # Update chat
    q.page['chatbox'] = cards.chatbox(chat=q.client.chat)

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
