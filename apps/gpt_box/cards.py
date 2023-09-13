import sys
import traceback

from h2o_wave import Q, data, expando_to_dict, ui
from llmbox.chat import Chat, Role
from llmbox.llms.gpt import GPTModels

# LLM Box
llmbox_logo_url = 'https://raw.githubusercontent.com/victorycrest/llmbox/main/docs/source/_static/llmbox_1024.png'
llmbox_colour = '#e5d5c0'

# App name
app_name = 'GPT Box'

# Repo details
repo_url = 'https://github.com/victorycrest/llmbox'
issue_url = f'{repo_url}/issues/new?assignees=victorycrest&labels=app%2C+bug&template=app-error-report.md&title=%5BAPP+ERROR%5D'

# Meta information
meta = ui.meta_card(
    box='',
    title=f'{app_name} | LLM Box',
    icon=llmbox_logo_url,
    layouts=[
        ui.layout(
            breakpoint='xs',
            zones=[
                ui.zone(name='header'),
                ui.zone(name='tabs', size='90px'),
                ui.zone(name='main', direction='row', size='calc(100vh - 170px)')
            ]
        )
    ],
    themes=[
        ui.theme(
            name='llmbox-dark',
            primary=llmbox_colour,
            text='white',
            card='#111111',
            page='black',
        ),
        ui.theme(
            name='llmbox-light',
            primary='black',
            text='black',
            card='#eeeeee',
            page='#f7f7f7',
        )
    ],
    theme='llmbox-dark'
)

# Header
header = ui.header_card(
    box='header',
    title=app_name,
    subtitle='Chat with the GPT family of LLMs by OpenAI',
    image=llmbox_logo_url,
    items=[
        ui.buttons(
            items=[
                ui.button(name='github', icon='GitHubLogo', path=repo_url),
                ui.button(name='x', icon='TwitterLogo', path='https://x.com/victorycrest'),
                ui.button(name='update_theme', icon='Light')
            ]
        )
    ]
)

# Tabs
tabs = ui.tab_card(
    box='tabs',
    items=[
        ui.tab(name='tab_chat', label='Chat', icon='ChatBot')
    ],
    link=True
)

# API dialog
dialog_api = ui.dialog(
    name='dialog_api',
    title='API Key Required',
    items=[
        ui.textbox(
            name='api_key',
            label='API Key',
            placeholder='Paste your API key here',
            password=True,
            required=True
        ),
        ui.buttons(
            items=[ui.button(name='save_api', label='Save', primary=True)],
            justify='center'
        ),
        ui.separator(label='or'),
        ui.text('<center>Set the environment variable OPENAI_API_KEY with your API key & restart the app')
    ],
    blocking=True,
    events=['dismissed']
)

# Fallback card
fallback = ui.form_card(
    box='fallback',
    items=[ui.text('Uh-oh, something went wrong!')]
)


def chatbox(chat: Chat) -> ui.ChatbotCard:
    """
    Card for chatting with LLM.
    """

    role_icon = {Role.User: '🧑', Role.Assistant: '🤖'}
    if len(chat.messages) == 0:
        rows = [['🤖: Hello! I\'m GPT, how can I help you today?', False]]
        placeholder = 'Type something to get started...'
    else:
        rows = [[f'{role_icon[m.role]}: {m.text}', m.role == Role.User] for m in chat.messages]
        placeholder = 'Type a message'

    return ui.chatbot_card(
        box='main',
        name='chat',
        data=data(fields=['content', 'from_user'], rows=rows),
        placeholder=placeholder,
        commands=[
            ui.command(name='restart', label='Restart', icon='ClearSelection'),
            ui.command(name='settings', label='Settings', icon='Settings')
        ]
    )


def dialog_settings(
    settings_tab: str,
    model: str,
    max_tokens: int,
    temperature: float,
    top_p: float
) -> ui.Dialog:
    """
    Dialog for settings.
    """

    dialog_items = [
        ui.tabs(
            name='settings_tab',
            items=[
                ui.tab(name='tab_model', label='Model'),
                ui.tab(name='tab_general', label='General')
            ],
            value=settings_tab,
            link=True
        )
    ]

    if settings_tab == 'tab_general':
        dialog_items.extend([
            ui.textbox(
                name='new_api_key',
                label='API Key',
                placeholder='Paste your API key here',
                password=True,
                trigger=True,
                tooltip='The API key will be saved into the environment and not accessible by the app.'
            )
        ])
    elif settings_tab == 'tab_model':
        dialog_items.extend([
            ui.dropdown(
                name='model',
                label='Model',
                choices=[ui.choice(name=m.value.lower(), label=m.value.lower()) for m in GPTModels],
                value=model,
                trigger=True,
                tooltip='Model to be used.'
            ),
            ui.spinbox(
                name='max_tokens',
                label='Max tokens to generate',
                min=1,
                max=99999,
                step=1,
                value=max_tokens,
                trigger=True,
                tooltip='Maximum number of tokens to generate before stopping.'
            ),
            ui.slider(
                name='temperature',
                label='Temperature (Randomness)',
                min=0.0,
                max=1.0,
                step=0.01,
                value=temperature,
                trigger=True,
                tooltip='Amount of randomness injected into the response.'
            ),
            ui.slider(
                name='top_p',
                label='Top-p (Nucleus Sampling)',
                min=0.0,
                max=1.0,
                step=0.01,
                value=top_p,
                trigger=True,
                tooltip='Cutoff probability for nucleus sampling of each subsequent token.'
            )
        ])
    else:
        pass

    return ui.dialog(
        name='dialog_settings',
        title='Settings',
        items=dialog_items,
        closable=True,
        events=['dismissed']
    )


def crash_report(q: Q) -> ui.FormCard:
    """
    Card for error reporting.
    """

    def code_block(content): return '\n'.join(['```', *content, '```'])

    type_, value_, traceback_ = sys.exc_info()
    stack_trace = traceback.format_exception(type_, value_, traceback_)

    dump = ['### Stack Trace', code_block(stack_trace)]
    states = [
        ('q.app', q.app),
        ('q.user', q.user),
        ('q.client', q.client),
        ('q.events', q.events),
        ('q.args', q.args)
    ]

    for name, source in states:
        dump.append(f'### {name}')
        dump.append(code_block([f'{k}: {v}' for k, v in expando_to_dict(source).items()]))

    return ui.form_card(
        box='main',
        items=[
            ui.stats(
                items=[
                    ui.stat(
                        label='',
                        value='Oops!',
                        caption='Something went wrong',
                        icon='Error',
                        icon_color=llmbox_colour
                    )
                ],
            ),
            ui.separator(),
            ui.text_l(content='Apologies for the inconvenience!'),
            ui.buttons(items=[ui.button(name='reload', label='Reload', primary=True)]),
            ui.expander(name='report', label='Error Details', items=[
                ui.text(
                    f'To report this, <a href="{issue_url}" target="_blank">please open an issue</a> with details:'),
                ui.text_l(content=f'Report Issue in App: **{app_name}**'),
                ui.text(content='\n'.join(dump)),
            ])
        ]
    )
