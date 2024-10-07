import re
import requests
from bs4 import BeautifulSoup
import json

class YouTubeTranscriptExtractor:
    def __init__(self, language: str):
        self.language = language

    def get_video_id(self, url: str) -> str:
        pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        raise ValueError("Invalid YouTube URL, can't get video ID")

    def grab_transcript_for_url(self, url: str) -> str:
        video_id = self.get_video_id(url)
        return self.grab_transcript(video_id, self.language)

    def grab_transcript(self, video_id: str, language: str = "en") -> str:
        transcript = self.grab_transcript_base(video_id, language)
        soup = BeautifulSoup(transcript, 'html.parser')
        text_tags = soup.find_all('text')
        return ' '.join(tag.text for tag in text_tags)

    def grab_transcript_base(self, video_id: str, language: str = "en") -> str:
        watch_url = f"https://www.youtube.com/watch?v={video_id}"
        response = requests.get(watch_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script')

        for script in scripts:
            if 'captionTracks' in script.text:
                match = re.search(r'"captionTracks":(\[.*?\])', script.text)
                if match:
                    caption_tracks = json.loads(match.group(1))
                    for track in caption_tracks:
                        if track.get('languageCode') == self.language:
                            transcript_url = track['baseUrl']
                            transcript_response = requests.get(transcript_url)
                            transcript_response.raise_for_status()
                            return transcript_response.text

        raise ValueError(f"Transcript not found for language: {self.language}")

    def get_video_title(self, video_id: str) -> str:
        watch_url = f"https://www.youtube.com/watch?v={video_id}"
        response = requests.get(watch_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find('meta', property='og:title')
        if title_tag:
            return title_tag['content']
        else:
            return "Untitled Video"

    def get_channel_name(self, video_id: str) -> str:
        watch_url = f"https://www.youtube.com/watch?v={video_id}"
        response = requests.get(watch_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        channel_name = soup.find('link', itemprop='name')['content']
        return channel_name