from dotenv import load_dotenv
from yt_crawler import YouTubeTranscriptExtractor
from yt_summarizer import summarize_transcript, save_summary_to_markdown
from yt_chat import chat_with_video

# Load environment variables from .env file
load_dotenv()

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

            print(f"\nTranscript retrieved for: {title} - {channel_name}")
            
            mode = input("Enter 'chat' to chat with the video or 'summary' to summarize: ").strip().lower()

            if mode == 'summary':
                summary = summarize_transcript(transcript)
                print("\nVideo Summary:")
                print(summary)

                filepath = save_summary_to_markdown(title, url, channel_name, summary)
                print(f"\nSummary saved to {filepath}")

            elif mode == 'chat':
                chat_with_video(transcript, title, url, channel_name)

            else:
                print("Invalid mode selected. Please choose 'chat' or 'summary'.")

            print("\n" + "-"*50 + "\n")
        except Exception as e:
            print(f"Error: {str(e)}")

    print("Thank you for using the YouTube transcript grabber, summarizer, and question answerer!")

if __name__ == "__main__":
    main()