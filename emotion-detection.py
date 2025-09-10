import requests
import json


url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"

headers = {
    "Content-Type": "application/json",
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
   
}

def emotion_detector(text_to_analyze: str) -> str:
    """
    Runs emotion detection on the given text using Watson Emotion Detection API.
    
    Args:
        text_to_analyze (str): The text string to analyze for emotions.
    
    Returns:
        str: The 'text' attribute from the API response.
    """
    payload = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()  
    result = resp.json()
    
    
    return result.get("text", "")
