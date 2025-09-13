"""
Watson NLP emotion detection client and formatting helpers.
"""

from __future__ import annotations

from typing import Dict, Any
import json
import requests

WATSON_URL = (
    "https://sn-watson-emotion.labs.skills.network/v1/"
    "watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {
    "Content-Type": "application/json",
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
}


def _dominant(emotions: Dict[str, float]) -> str:
    """Return the emotion label with the highest score."""
    return max(emotions, key=emotions.get)


def emotion_detector(text_to_analyze: str) -> Dict[str, Any]:
    """
    Runs emotion detection on the given text using Watson Emotion Detection API.
    (Task 2 + Task 7 error handling)

    Args:
        text_to_analyze: The text string to analyze for emotions.

    Returns:
        A dict with keys: anger, disgust, fear, joy, sadness, dominant_emotion.

    Raises:
        ValueError: If input is blank/whitespace, mapped by server to 400.
        requests.HTTPError: For non-2xx HTTP responses from Watson API.
        requests.RequestException: For network-level errors/timeouts.
        KeyError/ValueError: If unexpected JSON shape is returned.
    """
    if text_to_analyze is None or not text_to_analyze.strip():
        # Task 7: explicit handling so the Flask layer can map to HTTP 400.
        raise ValueError("Blank input.")

    payload = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(WATSON_URL, headers=HEADERS, json=payload, timeout=30)
    response.raise_for_status()

    data = response.json()

    # Expected shape (Skills Network Watson endpoint):
    # {
    #   "emotionPredictions": [
    #     { "emotion": {"anger":0, "disgust":0, "fear":0, "joy":1, "sadness":0}, ... }
    #   ]
    # }
    try:
        emotions: Dict[str, float] = data["emotionPredictions"][0]["emotion"]
    except (KeyError, IndexError) as exc:
        raise ValueError(f"Unexpected response shape: {json.dumps(data)[:200]}...") from exc

    result = {
        "anger": float(emotions.get("anger", 0.0)),
        "disgust": float(emotions.get("disgust", 0.0)),
        "fear": float(emotions.get("fear", 0.0)),
        "joy": float(emotions.get("joy", 0.0)),
        "sadness": float(emotions.get("sadness", 0.0)),
    }
    result["dominant_emotion"] = _dominant(result)
    return result


def emotion_predictor(text_to_analyze: str) -> Dict[str, Any]:
    """
    Formatting wrapper (Task 3): returns the required output format:

    {
      "anger": 0.0,
      "disgust": 0.0,
      "fear": 0.0,
      "joy": 0.9,
      "sadness": 0.1,
      "dominant_emotion": "joy"
    }
    """
    return emotion_detector(text_to_analyze)