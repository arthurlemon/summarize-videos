from data_manager import get_video_summary, save_video_summary
from fastapi import APIRouter
from loguru import logger
from pydantic import BaseModel

router = APIRouter()


class VideoSummaryRequest(BaseModel):
    # TODO - Add validation to ensure this is a valid youtube url
    url: str


class VideoSummaryResponse(BaseModel):
    video_id: str
    summary_all: str
    summary_sections: list


@router.post("/summarize", response_model=VideoSummaryResponse)
async def summarize_video(video: VideoSummaryRequest):
    # TODO - Better way to extract video id?
    video_id = video.url.split("v=")[-1]
    logger.info(f"Summarizing video: {video_id}")
    video_summary = get_video_summary(video_id, not_exists_ok=True)
    # Save the summary
    save_video_summary(
        video_id, video_summary["summary_all"], video_summary["summary_sections"]
    )

    return VideoSummaryResponse(
        video_id=video_id,
        summary_all=video_summary["summary_all"],
        summary_sections=video_summary["summary_sections"],
    )


@router.get("/summary/{video_id}", response_model=VideoSummaryResponse | dict)
async def get_summary(video_id: str):
    video_data = get_video_summary(video_id, not_exists_ok=False)
    if video_data is not None:
        return video_data

    # If not, return an error
    return {"detail": "Video summary not found"}
