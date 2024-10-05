# YouTube Transcript Summarizer

This Python script extracts transcripts from YouTube videos and generates concise summaries using OpenAI's GPT model. It's designed to work with multiple languages and save summaries as markdown files.

## Features

- Extract transcripts from YouTube videos
- Support for multiple languages
- Generate summaries using OpenAI's GPT model
- Save summaries as markdown files
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
   git clone https://github.com/yourusername/youtube-transcript-summarizer.git
   cd youtube-transcript-summarizer
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
