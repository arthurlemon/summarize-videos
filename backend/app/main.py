from fastapi import FastAPI
from api.video_summary import router as video_summary_router

app = FastAPI()

app.include_router(video_summary_router, prefix="/api")

@app.get("/")
def read_root():
    return {"Hello": "World"}
