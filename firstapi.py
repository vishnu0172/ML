import argparse
import os
import sys
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()


def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "Missing GEMINI_API_KEY in your environment or .env file. "
            "Add it before running this script."
        )
    return genai.Client(api_key=api_key)


def generate_response(prompt: str, model: str | None = None):
    model_name = model or os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    client = get_client()

    last_error = None
    for attempt in range(1, 5):
        try:
            start = time.perf_counter()
            chat = client.chats.create(model=model_name)
            response = chat.send_message(prompt)
            latency = time.perf_counter() - start

            usage = getattr(response, "usage_metadata", None)
            return {
                "text": getattr(response, "text", ""),
                "model": model_name,
                "latency_seconds": latency,
                "input_tokens": getattr(usage, "prompt_token_count", None),
                "output_tokens": getattr(usage, "candidates_token_count", None),
            }
        except Exception as exc:
            last_error = exc
            message = str(exc).lower()
            if "503" in message or "unavailable" in message or "high demand" in message:
                if attempt < 4:
                    delay = 2 ** attempt
                    print(f"Gemini is busy. Retrying in {delay} seconds...", file=sys.stderr)
                    time.sleep(delay)
                    continue
            raise

    raise last_error


def main():
    parser = argparse.ArgumentParser(description="Generate a response using the Gemini API.")
    parser.add_argument(
        "--prompt",
        default="Explain what a Large Language Model is in two sentences for a 3rd-year engineering student.",
        help="The prompt to send to the model.",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
        help="Gemini model name to use.",
    )
    args = parser.parse_args()

    result = generate_response(args.prompt, args.model)
    print(result["text"])
    print("-" * 40)
    print(f"Model        : {result['model']}")
    print(f"Input tokens : {result['input_tokens']}")
    print(f"Output tokens: {result['output_tokens']}")
    print(f"Latency      : {result['latency_seconds']:.2f} s")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)