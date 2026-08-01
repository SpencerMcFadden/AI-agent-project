import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "user", "content": args.user_prompt},
    ]
    generate_content(client, messages)


def generate_content(client: OpenAI, messages: list) -> None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages
    )

    if not response.usage:
        raise RuntimeError("Usage property is None")

    print("Prompt tokens:", response.usage.prompt_tokens)
    print("Response tokens:", response.usage.completion_tokens)
    print("Response:")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
