import torch # type: ignore
from transformers import pipeline # type: ignore

try:
    print("Attempting to load Hugging Face model...")
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    print("Hugging Face model loaded successfully!")

    test_text = "The quick brown fox jumps over the lazy dog."
    result = summarizer(test_text, max_length=15, min_length=5, truncation=True)
    print("Test summarization successful:")
    print(result)

except ImportError as e:
    print(f"Import Error: {e}")
    print("Please make sure you have `transformers` and `torch` installed.")
    print("Run: pip install transformers torch")

except Exception as e:
    print(f"An unexpected error occurred: {e}")