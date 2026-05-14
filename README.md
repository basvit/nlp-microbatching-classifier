# nlp-microbatching-classifier

### Testing:
API testen via Swagger UI 

`uv run uvicorn app.main:app --reload`

URL: http://localhost:8000/docs

Loadtest starten

`uv run python loadtest/load_generator.py`

Metrics testen: http://localhost:8000/metrics/

