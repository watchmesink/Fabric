from openai import OpenAI
import os
import re
import dotenv
from datetime import datetime

dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def answer_question(transcript: str, question: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant responding in the language of the information provided."},
                {"role": "user", "content": f"Based on the following transcript, please answer the question. Transcript:\n\n{transcript}\n\nQuestion: {question}"}
            ],
            max_tokens=500,
            n=1,
            temperature=0.7
        )
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        return f"Error in answering: {str(e)}"

def save_qa_to_markdown(title: str, url: str, channel_name: str, question: str, answer: str):
    questions_folder = os.path.join(os.getcwd(), 'questions')
    os.makedirs(questions_folder, exist_ok=True)

    filename = re.sub(r'[^\w\-_\. ]', '', title).replace(' ', '') + '.md'
    filepath = os.path.join(questions_folder, filename)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not os.path.exists(filepath):
        # Create the file with the header if it doesn't exist
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {title} - {channel_name}\n\n{url}\n\n")

    # Append the new question and answer
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(f"## Question: {question}\n\nTimestamp: {timestamp}\n\n{answer}\n\n---\n\n")
    
    return filepath

def chat_with_video(transcript: str, title: str, url: str, channel_name: str):
    print(f"\nChat with video: {title} - {channel_name}")
    print("Enter your questions or type 'quit' to exit.")

    while True:
        question = input("\nYour question: ")
        if question.lower() == 'quit':
            break

        answer = answer_question(transcript, question)
        print(f"\nAnswer: {answer}")

        filepath = save_qa_to_markdown(title, url, channel_name, question, answer)
        print(f"\nQuestion and answer saved to {filepath}")

    print("Chat session ended.")