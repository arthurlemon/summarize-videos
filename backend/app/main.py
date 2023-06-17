from api.video_summary import router as video_summary_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"Incoming request: {request.method} {request.url.path}")
        response = await call_next(request)
        print(f"Outgoing response: {response.status_code}")
        return response


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001"],  # Only allow this origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.add_middleware(LoggingMiddleware)

app.include_router(video_summary_router, prefix="/api")


@app.get("/")
def read_root():
    return {"data": "It works!"}
