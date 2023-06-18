# summarize-videos
Simple web app to summarize youtube videos.

Inspired by https://www.summarize.tech/

## Setup

### repo

```
git clone git@github.com:arthurlemon/summarize-videos.git
```

### openai

This is based on openai so one needs to add a `.env` file at the root of the repo with the following content:

`.env`
```
OPENAI_API_KEY=sk-... # your openai key, found at https://platform.openai.com/account/api-keys
```

Monitor your usage of openai at https://platform.openai.com/account/usage

(expect a few cents per youtube video)


### Backend

This app relies on python 3.11 and poetry.

To install on Mac:

```
brew update && brew install pyenv
pyenv install 3.11.1

# setup pyenv to manage python
echo -e '\nif command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init --path)"\nfi\n' >> ~/.zshrc
. ~/.zshrc

# install poetry
curl -sSL https://install.python-poetry.org | python3 -

```

Then in a new terminal:
```
cd backend && poetry shell && poetry install
uvicorn main:app --reload
```

Navigate to http://127.0.0.1:8000/docs to view and test the available APIs.

### Frontend
In another terminal
```
cd frontend/app
python -m http.server 8001 --bind 127.0.0.1
```

Navigate to http://127.0.0.1:8001/ in your browser to test the website!
