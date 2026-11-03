import sys
import argparse
from pathlib import Path
try:
    from .core import chat_with_pdf
    from . import __version__
except (ImportError, ValueError):
    from pdfjin_ai_chat.core import chat_with_pdf
    from pdfjin_ai_chat import __version__


def main():
    parser = argparse.ArgumentParser(
        prog="pdfjin-ai-chat",
        description="Ask questions and converse with PDF documents using AI.",
        epilog="Online web version available at https://pdfjin.com/pages/ai-pdf-chat.html",
    )
    parser.add_argument("input", metavar="INPUT_PDF", help="Path to the PDF file")
    parser.add_argument("-q", "--question", required=True, help="Question to ask about the PDF")
    parser.add_argument("--key", help="Google Gemini API Key (or set GEMINI_API_KEY environment variable)")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")

    args = parser.parse_args()

    try:
        answer = chat_with_pdf(args.input, question=args.question, api_key=args.key)
        print("\n💡 Answer:")
        print(answer)
    except Exception as e:
        print(f"❌ AI Chat failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
