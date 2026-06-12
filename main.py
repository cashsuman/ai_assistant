import os
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing. Please add it to your .env file.")

client = Groq(api_key=GROQ_API_KEY)


def get_user_input():
    task = input("Enter your productivity task: ").strip()

    if not task:
        raise ValueError("Task cannot be empty.")

    return task


def generate_response(task):
    prompt = f"""
You are an AI Productivity Assistant.

User task:
{task}

Generate a clear, structured response with:

1. Goal
2. Key Steps
3. Suggested Timeline
4. Tools or Resources Needed
5. Final Recommendation
"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI productivity assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=MODEL_NAME,
            temperature=0.4,
            max_tokens=1000
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"Error while generating response: {str(e)}"


def save_response(task, response):
    try:
        os.makedirs("outputs", exist_ok=True)

        file_path = "outputs/response.txt"

        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f"Date: {datetime.now()}\n")
            file.write(f"Task: {task}\n")
            file.write("AI Response:\n")
            file.write(response)
            file.write("\n")
            file.write("-" * 60)
            file.write("\n\n")
        

        print(f"\nResponse saved to {file_path}")
        


    except Exception as e:
        print(f"Error saving file: {e}")


def main():
    try:
        print("AI Productivity Assistant using Groq")
        print("-" * 40)

        task = get_user_input()

        response = generate_response(task)

        print("\nAI Response:\n")
        print(response)

        save_response(task, response)

    except ValueError as e:
        print(f"Input Error: {e}")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")

    except Exception as e:
        print(f"Unexpected Error: {e}")


if __name__ == "__main__":
    main()