import os
import argparse
from google.cloud import language_v1
import sys
import glob


def analyze(movie_review_filename):
    """Run a sentiment analysis request on text within a passed filename."""
    client = language_v1.LanguageServiceClient()

    with open(movie_review_filename, "r") as review_file:
        # Instantiates a plain text document.
        content = review_file.read()

    document = language_v1.Document(
        content=content, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    annotations = client.analyze_sentiment(request={"document": document})

    # Print the results
    # print_result(annotations)
    return annotations.document_sentiment.score, annotations.document_sentiment.magnitude


if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\a881910\GitHub\ODPP\mongodb_insert\key.json"
    # sys.argv.append("video_ids.txt")
    results = []
    dir = r"C:\Users\a881910\GitHub\ODPP\mongodb_insert\transcripts"
    for path in os.listdir(dir):
        score, magnitude = analyze(os.path.join(dir, path))
        results.append(score * magnitude)
    print(round(sum(results) / len(results), 2))

