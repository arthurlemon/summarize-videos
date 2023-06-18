from unittest.mock import patch

from app.data_manager import get_section_chunks, get_transcript


@patch("app.data_manager.YouTubeTranscriptApi.get_transcript")
def test_get_transcript(mock_get_transcript):
    # Set up the mock to return a known transcript
    mock_get_transcript.return_value = [
        {"start": 0, "duration": 60, "text": "Hello, world!"},
        {"start": 60, "duration": 15, "text": "This is a test."},
    ]

    # Call the function under test
    result = get_transcript("fake_video_id")

    # Assert that the function processed the transcript correctly
    assert result == [
        {"start": 0, "end": 1.0, "duration": 60, "text": "Hello, world!"},
        {"start": 1, "end": 1.25, "duration": 15, "text": "This is a test."},
    ]


def test_get_section_chunks():
    # Set up a known transcript
    transcript = [
        {"start": 0, "end": 5, "duration": 60, "text": "Hello, world!"},
        {"start": 5, "end": 5.5, "duration": 30, "text": "This is a test."},
        {"start": 12, "end": 15, "duration": 60, "text": "Another section."},
    ]

    # Call the function under test
    result = get_section_chunks(transcript)

    # Assert that the function chunked the transcript correctly
    assert result == [
        {"start": 0, "end": 5.5, "text": "Hello, world! This is a test."},
        {"start": 12, "end": 15, "text": "Another section."},
    ]
