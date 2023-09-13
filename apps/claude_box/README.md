<h2>Claude Box <img src="https://raw.githubusercontent.com/victorycrest/llmbox/main/docs/source/_static/llmbox_1024.png" width="18px"></img></h2>
Chat with the Claude family of LLMs by Anthropic.

## Setup ⚙️
1. Check the version of Python, must be Python 3.10+ but recommended to use Python 3.11+ for best experience

```commandline
python3 --version
```

2. Clone the repository

```commandline
git clone https://github.com/victorycrest/llmbox.git
```

3. Create a virtual environment

```commandline
cd llmbox/apps/claude_box
python3 -m venv venv
source venv/bin/activate
```

4. Install the packages

```commandline
python3 -m pip install -U pip
python3 -m pip install -r requirements.txt
```

5. (Optional) Add <a href="https://console.anthropic.com/account/keys" target="_blank">Anthropic API Key</a> to the environment

```commandline
export ANTHROPIC_API_KEY="YOUR_KEY"
```

6. Run the application

```commandline
wave run app
```

7. View the application on your local browser: <a href="http://localhost:10101" target="_blank">http://localhost:10101</a>

8. (If Step 5 was skipped) Add <a href="https://console.anthropic.com/account/keys" target="_blank">Anthropic API Key</a> to the app directly in the UI.
