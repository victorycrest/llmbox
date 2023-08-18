import sys
import traceback

from h2o_wave import Q, data, expando_to_dict, ui
from llmbox.chat import Chat, Role
from llmbox.llms.anthropic import AnthropicModels

# LLM Box
llmbox_logo_url = 'https://raw.githubusercontent.com/victorycrest/llmbox/main/docs/source/_static/llmbox_1024.png'
llmbox_colour = '#e5d5c0'

# App name
app_name = 'Claude Box'

# Repo details
repo_url = 'https://github.com/victorycrest/llmbox'
issue_url = f'{repo_url}/issues/new?assignees=victorycrest&labels=app%2C+bug&template=app-error-report.md&title=%5BAPP+ERROR%5D'

# Meta card
meta = ui.meta_card(
    box='',
    title='LLM Box',
    icon=llmbox_logo_url,
    layouts=[
        ui.layout(
            breakpoint='xs',
            zones=[
                ui.zone(name='header'),
                ui.zone(name='main', direction='row', size='calc(100vh - 165px)'),
                ui.zone(name='footer')
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

# Header card
header = ui.header_card(
    box='header',
    title=app_name,
    subtitle='Chat with the Claude family of LLMs by Anthropic',
    image=llmbox_logo_url,
    items=[ui.button(name='settings', label='Settings', icon='Settings', primary=True)]
)

# Footer card
footer = ui.footer_card(
    box='footer',
    caption=f'''<a href="{repo_url}" target="_blank">
        <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="21"></a>
        <a href="https://twitter.com/victorycrest" target="_blank">
        <img src="https://pbs.twimg.com/profile_images/1683899100922511378/5lY42eHs_400x400.jpg" width="21"></a>'''
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

    role_icon = {'User': '🧑', 'AI': '🤖'}
    if len(chat.messages) == 0:
        rows = [['🤖: Hello! I\'m Claude, how can I help you today?', False]]
        placeholder = 'Type something to get started...'
    else:
        rows = [[f'{role_icon[m.role.name]}: {m.text}', m.role == Role.User] for m in chat.messages]
        placeholder = 'Type a message'

    return ui.chatbot_card(
        box='main',
        name='chat',
        data=data(fields=['content', 'from_user'], rows=rows),
        placeholder=placeholder
    )


def dialog_settings(theme_dark: bool, model: str, max_tokens_to_sample: int):
    """
    Dialog for settings.
    """

    return ui.dialog(
        name='dialog_settings',
        title='Settings',
        items=[
            ui.separator(label='General'),
            ui.textbox(name='api_key', label='API Key', password=True, trigger=True),
            ui.toggle(name='theme_dark', label='Dark Mode', value=theme_dark, trigger=True),
            ui.separator(label='Model'),
            ui.dropdown(
                name='model',
                label='Model',
                choices=[ui.choice(name=m.value.lower(), label=m.value.lower()) for m in AnthropicModels],
                value=model,
                trigger=True
            ),
            ui.spinbox(
                name='max_tokens_to_sample',
                label='Max tokens to generate',
                min=1,
                max=99999,
                step=1,
                value=max_tokens_to_sample,
                trigger=True
            )
        ],
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
