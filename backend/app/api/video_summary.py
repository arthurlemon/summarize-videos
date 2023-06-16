from fastapi import APIRouter
from data_manager import get_video_summary, save_video_summary
from pydantic import BaseModel

# import and setup your Youtube and GPT-3.5 API here

router = APIRouter()


class VideoSummaryRequest(BaseModel):
    url: str


class VideoSummaryResponse(BaseModel):
    url: str
    summary_all: str
    summary_sections: list


@router.post("/summarize", response_model=VideoSummaryResponse)
async def summarize_video(video: VideoSummaryRequest):
    # Check if video summary exists
    video_summary = get_video_summary(video.url)

    # Save the summary
    save_video_summary(video.url, video_summary, [])

    return {"url": video.url, "summary_all": video_summary, "summary_sections": []}


@router.get("/summary/{url}", response_model=VideoSummaryResponse)
async def get_summary(url: str):
    # Get video summary if it exists
    video_data = get_video_summary(url)
    if video_data is not None:
        return video_data

    # If not, return an error
    return {"detail": "Video summary not found"}
