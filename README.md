# Dandi Search Response UI
![image](media/ui-demo.gif)

## Running Locally

1. To run the web application service, first build the Docker image.

```bash
docker build -t dsru-app .
```

2. Run the container with the specific configurations (environment variables, port mapping).

```bash
docker run --env-file envfile.txt -p 8000:8000 dsru-app
```

