# summarize-videos
Simple web app to summarize youtube videos
Inspired by https://www.summarize.tech/

## Setup

### openai

This is based on openai so one needs to add a `.env` file at the root of the repo with the following content:

`.env`
```
OPENAI_API_KEY=sk-... # your openai key, found at https://platform.openai.com/account/api-keys
```

Monitor your usage of openai at https://platform.openai.com/account/usage


### Backend

In one terminal:
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
