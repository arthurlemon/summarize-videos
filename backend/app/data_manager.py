import json
import os
import time

import openai
from dotenv import load_dotenv
from loguru import logger
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv("../../.env")
openai.api_key = os.getenv("OPENAI_API_KEY", None)
assert openai.api_key is not None, "No OPENAI_API_KEY environment variable set"


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


def save_video_summary(video_id, summary_all, summary_sections):
    global data
    data.append(
        {
            "video_id": video_id,
            "summary_all": summary_all,
            "summary_sections": summary_sections,
        }
    )
    save_data(data)


def get_video_summary(video_id, not_exists_ok: bool = True, use_cache: bool = False):
    global data
    if use_cache and data:
        for video_data in data:
            if video_data["video_id"] == video_id:
                return video_data
        if not not_exists_ok:
            return None
    else:
        transcript = get_transcript(video_id)
        chunks = get_section_chunks(transcript)
        summary = generate_summary(chunks)
        return summary


def get_transcript(video_id):
    # TODO - Handle errors with video without subtitles
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    # Add end instead of duration
    for section in transcript:
        section["end"] = section["start"] + section["duration"]

    # convert to minutes
    for section in transcript:
        section["start"] = round(section["start"] / 60, 4)
        section["end"] = round(section["end"] / 60, 4)

    return transcript


def get_section_chunks(
    transcript, chunk_duration: int = 5, min_chunk_duration: float = 0.5
):
    # Group sections into chunks of approximately 5 minutes
    chunks = []
    current_chunk = {
        "start": transcript[0]["start"],
        "end": transcript[0]["end"],
        "text": transcript[0]["text"],
    }
    for section in transcript[1:]:
        if section["start"] - current_chunk["start"] <= chunk_duration:
            current_chunk["end"] = section["end"]
            current_chunk["text"] += " " + section["text"]
        else:
            chunks.append(current_chunk)
            current_chunk = {
                "start": section["start"],
                "end": section["end"],
                "text": section["text"],
            }

    chunks.append(current_chunk)

    if current_chunk["end"] - current_chunk["start"] <= min_chunk_duration:
        # Merge the last chunk with the previous chunk
        previous_chunk = chunks[-1]
        previous_chunk["end"] = current_chunk["end"]
        previous_chunk["text"] += " " + current_chunk["text"]
        chunks.pop()

    return chunks


def generate_summary(chunks, strategy: str = "fake"):
    if strategy == "openai":
        for section in chunks:
            summary = create_summary_openai(section["text"])
            section["summary"] = summary
        overall_summary = create_summary_openai(
            " ".join([section["summary"] for section in chunks]),
            summary_start="In this video",
        )
    else:
        for section in chunks:
            section["summary"] = "summary"
        time.sleep(1)
        overall_summary = "fake global summary"
    logger.info(chunks)
    return {
        "summary_all": overall_summary,
        "summary_sections": [section for section in chunks],
    }


def create_summary_openai(text: str, summary_start: str = "In this section") -> str:
    prompt = [
        {
            "role": "user",
            "content": f"Summarize the following transcript from a youtube video in 5 sentences or less:"
            f"\n{text}\n\nStart your summary with {summary_start}",
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=0.7,
        max_tokens=100,
    )
    return response.choices[0]["message"]["content"]


if __name__ == "__main__":
    video_id = "kR1buRTIKhk"
    transcript = get_transcript(video_id)
    chunks = get_section_chunks(transcript, chunk_duration=5)
    summary = generate_summary(chunks)
