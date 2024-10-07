# Fabric: AI-Powered YouTube Video Analyzer

Fabric is an innovative tool that leverages AI to extract, summarize, and interact with YouTube video content. It offers a seamless way to digest information from videos and engage with their content through natural language conversations.

## Features

- **Transcript Extraction**: Pulls transcripts from YouTube videos in multiple languages.
- **AI-Powered Summarization**: Generates concise summaries of video content using OpenAI's GPT model.
- **Interactive Chat**: Allows users to ask questions about the video content and receive AI-generated responses.
- **Multi-Language Support**: Works with various language transcripts.
- **Markdown Export**: Saves summaries and Q&A sessions as markdown files for easy reference.

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/fabric.git
   cd fabric
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key in a `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

4. Run the main script:
   ```
   python main.py
   ```

## Usage

1. Enter the desired language code (e.g., 'en' for English).
2. Provide a YouTube URL.
3. Choose between 'summary' mode for a video summary or 'chat' mode to interact with the video content.

## Output

- Summaries are saved in the `summaries` folder.
- Chat Q&A sessions are stored in the `questions` folder.
- Each file is named after the video title and includes metadata.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool uses the OpenAI API, which may incur costs. Please review OpenAI's pricing before extensive use.
