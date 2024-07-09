import os
import openai

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key is not set. Please set the OPENAI_API_KEY environment variable.")

client = openai.OpenAI(api_key=api_key)

def generate_text(prompt, chat_log=None):
    try:
        if chat_log is None:
            chat_log = []
        chat_log.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_log
        )
        answer = response.choices[0].message.content.strip()
        chat_log.append({"role": "assistant", "content": answer})
        
        return answer, chat_log
    except Exception as e:
        return f"An error occurred: {e}", chat_log

if __name__ == "__main__":
    chat_log = []
    while True:
        user_prompt = input("You: ")
        if user_prompt.lower() in ["quit", "exit", "bye"]:
            print("Exiting chat...")
            break
        result, chat_log = generate_text(user_prompt, chat_log)
        print("Bot:", result)