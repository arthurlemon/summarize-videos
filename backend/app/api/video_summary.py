from data_manager import DataManager
from fastapi import APIRouter
from loguru import logger
from pydantic import BaseModel

router = APIRouter()

data_manager = DataManager()


class VideoSummaryRequest(BaseModel):
    # TODO - Add validation to ensure this is a valid youtube url
    url: str


class VideoSummaryResponse(BaseModel):
    video_id: str
    summary_all: str
    summary_sections: list


@router.post("/summarize")  # , response_model=VideoSummaryResponse)
async def summarize_video(video: VideoSummaryRequest):
    # TODO - Better way to extract video id?
    video_id = video.url.split("v=")[-1]
    video_summary = data_manager.get_video_summary(video_id)
    # Save the summary
    logger.info(video_summary)

    data_manager.save_video_summary(
        video_id, video_summary["summary_all"], video_summary["summary_sections"]
    )

    return VideoSummaryResponse(
        video_id=video_id,
        summary_all=video_summary["summary_all"],
        summary_sections=video_summary["summary_sections"],
    )


@router.get("/summary/{video_id}", response_model=VideoSummaryResponse | dict)
async def get_summary(video_id: str):
    video_data = data_manager.get_video_summary(video_id)
    if video_data is not None:
        return video_data

    # If not, return an error
    return {"detail": "Video summary not found"}
