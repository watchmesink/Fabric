# YouTube Transcript Summarizer and Chat

This Python application extracts transcripts from YouTube videos, generates concise summaries, and allows users to chat with the video content using OpenAI's GPT model. It supports multiple languages and saves summaries and chat sessions as markdown files.

## Features

- Extract transcripts from YouTube videos
- Support for multiple languages
- Generate summaries using OpenAI's GPT model
- Chat with video content using AI
- Save summaries and Q&A sessions as markdown files
- Retrieve video titles and channel names

## Requirements

- Python 3.6+
- Required Python packages (install using `pip install -r requirements.txt`):
  - requests
  - beautifulsoup4
  - openai
  - python-dotenv

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/youtube-transcript-summarizer-chat.git
   cd youtube-transcript-summarizer-chat
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the script:
