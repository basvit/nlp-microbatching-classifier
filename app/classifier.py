from transformers import pipeline

from app.config import CANDIDATE_LABELS, MODEL_NAME


classifier = pipeline("zero-shot-classification", model=MODEL_NAME)


def classify_comments_batch(comments: list[str]) -> list[dict]:
    """Classify multiple comments in a single batch inference"""

    # Classify the comments using the zero-shot classifier
    results = classifier(
        comments,
        CANDIDATE_LABELS,
    )

    classified_comments = []

    # Zip the original comments with their classification results and format the output
    for comment, result in zip(comments, results, strict=True):
        classified_comments.append(
            {
                "comment": comment,
                "label": result["labels"][0],
                "score": result["scores"][0],
            }
        )

    return classified_comments
