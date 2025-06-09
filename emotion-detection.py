
import requests, json

url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"

headers = {
    "Content-Type": "application/json",
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    # If your environment requires auth, add e.g.  "Authorization": f"Bearer {TOKEN}"
}

payload = {
    "raw_document": {
        "text": "I'm excited to try this out!"
    }
}

resp = requests.post(url, headers=headers, json=payload, timeout=30)
resp.raise_for_status()           # throws if non-200
print(json.dumps(resp.json(), indent=2))

             