import asyncio
from src.crawl import get_website_data
from src.llm_response import get_llm_response
from src.tts import tts

def main() -> None:
    """
    Main function to fetch website data, summarize it, and optionally convert the summary to speech.
    """
    url: str = input("Enter the URL to scrape: ")
    convert_to_speech: str = input("Do you want the summary as audio? (yes/no): ").strip().lower()

    try:
        # Fetch website data
        print("Fetching website data...")
        website_data: dict = asyncio.run(get_website_data(url))
        text_content: str = website_data.get("text", "")

        if not text_content:
            print("No text content found on the website.")
            return

        # Generate summary
        print("Generating summary...")
        llm_response: dict = get_llm_response(text_content)
        summary: str = llm_response.get("summary", "")

        if not summary:
            print("Failed to generate summary.")
            return

        print("\nSummary:")
        print(summary)

        # Convert summary to speech if requested
        if convert_to_speech == "yes":
            print("Converting summary to speech...")
            audio_stream = tts(summary)
            with open("summary.mp3", "wb") as audio_file:
                audio_file.write(audio_stream.read())
            print("Audio saved as 'summary.mp3'.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
