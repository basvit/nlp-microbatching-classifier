# nlp-microbatching-classifier

### Testing
API testen via Swagger UI 

`uv run uvicorn app.main:app --reload`

URL: http://localhost:8000/docs

Loadtest starten

`uv run python loadtest/load_generator.py`

Anschliessend Metrics testen: http://localhost:8000/metrics/

### Lokaler Docker testen
Docker-Image erstellen
`docker build -t nlp-classifier .`

Container starten
`docker run -p 8000:8000 nlp-classifier`

Testen
`http://localhost:8000/docs`
`http://localhost:8000/metrics`

### Docker Compose 

Starten
`docker compose up --build`

Classifier starten
`http://localhost:8000/docs`

Metrics starten
`http://localhost:8000/metrics`

Prometheus
`http://localhost:9090`

Grafana
`http://localhost:3000`

User: admin

Passwort: admin


