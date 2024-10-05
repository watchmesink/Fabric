import re
import requests
from bs4 import BeautifulSoup
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

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

def summarize_transcript(transcript: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant responding in the language of the information provided."},
                {"role": "user", "content": f"You need to provide 10 key takeaways from the video in a format of bullet points. The takeaways need to be quite exhaustive. Here is the video:\n\n{transcript}"}
            ],
            max_tokens=1000,
            n=1,
            temperature=0.7
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        return f"Error in summarizing: {str(e)}"

def save_to_markdown(title: str, url: str, channel_name: str, summary: str):
    # Create a 'summaries' folder if it doesn't exist
    summaries_folder = os.path.join(os.getcwd(), 'summaries')
    os.makedirs(summaries_folder, exist_ok=True)

    # Create filename and full path
    filename = re.sub(r'[^\w\-_\. ]', '', title).replace(' ', '') + '.md'
    filepath = os.path.join(summaries_folder, filename)

    content = f"# {title} - {channel_name}\n\n{url}\n\n{summary}"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath

def main():
    while True:
        language = input("Enter the desired language code (e.g., 'en' for English, or 'quit' to exit): ").strip().lower()
        
        if language == 'quit':
            break

        youtube = YouTubeTranscriptExtractor(language)

        url = input("Enter a YouTube URL: ")

        try:
            video_id = youtube.get_video_id(url)
            title = youtube.get_video_title(video_id)
            channel_name = youtube.get_channel_name(video_id)
            transcript = youtube.grab_transcript_for_url(url)

            summary = summarize_transcript(transcript)
            
            output = f"# {title} - {channel_name}\n\n{url}\n\nLanguage: {language}\n\n{summary}"
            print("\nVideo Summary:")
            print(output)

            filepath = save_to_markdown(title, url, channel_name, summary)
            print(f"\nSummary saved to {filepath}")

            print("\n" + "-"*50 + "\n")
        except Exception as e:
            print(f"Error: {str(e)}")

    print("Thank you for using the YouTube transcript grabber and summarizer!")

if __name__ == "__main__":
    main()