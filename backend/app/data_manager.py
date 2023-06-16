import pandas as pd
import os
from youtube_transcript_api import YouTubeTranscriptApi

# TODO - Deal with cache with dataframe

DATA_FILE = "data.csv"
dataframe = pd.DataFrame(columns=["url", "summary_all", "summary_sections"])


def load_data():
    global dataframe
    if os.path.isfile(DATA_FILE):
        dataframe = pd.read_csv(DATA_FILE)
    else:
        dataframe = pd.DataFrame(columns=["url", "summary_all", "summary_sections"])


def save_data():
    global dataframe
    dataframe.to_csv(DATA_FILE, index=False)


def get_video_summary(url):
    global dataframe
    video_data = dataframe[dataframe["url"] == url]
    if video_data.empty:
        transcript = get_transcript(url)
        summary = generate_summary(transcript)
        return summary
    else:  # cache hit
        return video_data.iloc[0]


def get_transcript(url):
    # dirty logic to extract video id from url
    start_index = url.index("v=") + 2
    extracted_string = url[start_index:]

    transcript = YouTubeTranscriptApi.get_transcript(extracted_string)
    return transcript


def generate_summary(transcript):
    # TODO - Generate summary from transcript
    return transcript[0]


def save_video_summary(url, summary_all, summary_sections):
    global dataframe
    dataframe = pd.concat(dataframe, 
        pd.DataFrame.from_dict({"url": url, "summary_all": summary_all, "summary_sections": summary_sections},
    ))
    save_data()
