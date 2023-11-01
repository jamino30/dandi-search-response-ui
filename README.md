# Dandi Search Response UI
![image](media/ui-demo.gif)

## Running Locally

1. Set necessary environment variables
```bash
export QDRANT_HOST=
export QDRANT_PORT=
export QDRANT_COLLECTION_NAME=
export QDRANT_VECTOR_SIZE=
export QDRANT_API_KEY=
export OPENAI_API_KEY=
export DANDI_API_KEY=
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_DEFAULT_REGION=
```

2. To run the web application service, first build the Docker image.

```bash
docker build -t dsru-app .
```

3. Run the container with the specific configurations (environment variables, port mapping).

```bash
docker run --env-file envfile.txt -p 8000:8000 dsru-app
```

