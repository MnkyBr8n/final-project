# Emotion Detection App (Watson NLP)

## Quick Start
```bash
python -m pip install -r requirements.txt
export FLASK_APP=app.server:app
flask run --port 5000
# POST:
curl -s -X POST http://localhost:5000/analyze -H 'Content-Type: application/json' \
  -d '{"text":"I am extremely happy today!"}' | jq
