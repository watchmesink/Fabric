from openai import OpenAI
import os
import re
import dotenv

dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_transcript(transcript: str, instructions: str) -> tuple:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant responding in the language of the information provided."},
                {"role": "user", "content": f"{instructions}\n\n{transcript}"}
            ],
            max_tokens=1000,
            n=1,
            temperature=0.7
        )
        summary = response.choices[0].message.content.strip()
        tokens_used = response.usage.total_tokens
        return summary, tokens_used
    except Exception as e:
        return f"Error in summarizing: {str(e)}", 0

def save_summary_to_markdown(title: str, url: str, channel_name: str, summary: str):
    summaries_folder = os.path.join(os.getcwd(), 'summaries')
    os.makedirs(summaries_folder, exist_ok=True)

    filename = re.sub(r'[^\w\-_\. ]', '', title).replace(' ', '') + '.md'
    filepath = os.path.join(summaries_folder, filename)

    content = f"# {title} - {channel_name}\n\n{url}\n\n{summary}"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath