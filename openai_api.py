import os
import openai

# Make sure to set your API key in the environment variable or manage it securely.
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key is not set. Please set the OPENAI_API_KEY environment variable.")

# Initialize the OpenAI client with your API key.
client = openai.OpenAI(api_key=api_key)

def generate_text(prompt):
    try:
        # Create chat completions using the GPT-3.5-turbo model.
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        # Accessing the message content correctly.
        # If the response structure has 'choices' and each choice has 'message' attribute containing 'content'.
        generated_text = response.choices[0].message.content.strip()
        return generated_text
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    user_prompt = input("Enter a prompt: ")
    result = generate_text(user_prompt)
    print("Generated Text:", result)