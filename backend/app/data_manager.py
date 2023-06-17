import json
import os

from youtube_transcript_api import YouTubeTranscriptApi

DATA_FILE = "data.json"


def load_data() -> list:
    if os.path.isfile(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []
    return data


# TODO - Get video summary from database
data = load_data()


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


# TODO - Refactor to use video_id instead of url
def get_video_summary(video_id, not_exists_ok: bool = True, use_cache: bool = False):
    global data
    if use_cache:
        for video_data in data:
            if video_data["url"] == video_id:
                return video_data
        if not not_exists_ok:
            return None
    else:
        transcript = get_transcript(video_id)
        summary = generate_summary(transcript)
        return summary


def get_transcript(video_id):
    # TODO - Handle errors with video without subtitles
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    # Add end instead of duration
    for section in transcript:
        section["end"] = round(section["start"] + section["duration"], 4)

    return transcript


def generate_summary(transcript):
    # TODO - Generate summary from transcript
    # Will require splitting transcript into sections
    # generating a summary for each section
    # and geneating a summary for the entire video from the section summaries
    return {
        "summary_all": transcript[0]["text"],
        "summary_sections": [section for section in transcript],
    }


def save_video_summary(url, summary_all, summary_sections):
    global data
    data.append(
        {"url": url, "summary_all": summary_all, "summary_sections": summary_sections}
    )
    save_data(data)
