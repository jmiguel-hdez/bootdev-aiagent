import os
import sys
from dotenv import load_dotenv
from google import genai


def main():
    if len(sys.argv) < 2:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    args = sys.argv[1:]
    print(f"args: {args}")
    prompt_text = " ".join(args)
    print(f"prompt text: {prompt_text}")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt_text,
    )

    if response:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print("Response:")
        print(response.text)


if __name__ == "__main__":
    main()
