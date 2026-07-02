import os
import argparse

from dotenv import load_dotenv
from openai import OpenAI


def main() -> None:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY enviroment variable not set")

    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str,
                        help="input prompt to send to the LLM")
    args = parser.parse_args()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages = [
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages
    )
    if response is None or response.usage is None:
        raise RuntimeError("openrouter response came as None")

    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")

    print("Response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
