import os
from dotenv import load_dotenv
from openai import OpenAI


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("Key is not available")
        print("Hello from bootdev-aiagent!")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages = [
        {
            "role": "user",
            "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
        }
    ]
    response = client.chat.completions.create(
        messages=messages, model="openrouter/free")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
