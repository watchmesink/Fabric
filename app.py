from flask import Flask, render_template, request
from yt_crawler import YouTubeTranscriptExtractor
from yt_summarizer import summarize_transcript, save_summary_to_markdown
import markdown

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    tokens_used = 0
    cost = 0.0
    if request.method == 'POST':
        language = request.form.get('language')
        url = request.form.get('youtube_url')
        instructions = request.form.get('instructions')

        try:
            youtube = YouTubeTranscriptExtractor(language)
            video_id = youtube.get_video_id(url)
            title = youtube.get_video_title(video_id)
            channel_name = youtube.get_channel_name(video_id)
            transcript = youtube.grab_transcript_for_url(url)

            summary, tokens_used = summarize_transcript(transcript, instructions)
            summary_html = markdown.markdown(summary)
            filepath = save_summary_to_markdown(title, url, channel_name, summary)

            # Assuming $0.02 per 1000 tokens as an example
            cost = (tokens_used / 1000) * 0.02

            return render_template('index.html', summary=summary_html, filepath=filepath, tokens_used=tokens_used, cost=cost)

        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True, port=5002) 