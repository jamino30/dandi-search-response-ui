# Dandi Search Response UI
![image](media/ui-demo.gif)

## Running Locally

1. Fill in ```envfile.txt``` with the following environment variables
```bash
QDRANT_HOST=
QDRANT_PORT=
QDRANT_COLLECTION_NAME=
QDRANT_VECTOR_SIZE=
QDRANT_API_KEY=
OPENAI_API_KEY=
DANDI_API_KEY=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=
```

2. To run the web application service, first build the Docker image.

```bash
docker build -t dsru-app .
```

3. Run the container with the specific configurations (environment variables, port mapping).

```bash
docker run --env-file envfile.txt -p 8000:8000
```
