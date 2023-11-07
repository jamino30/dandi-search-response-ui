# Dandi Search Response UI

[![Push Docker image to ECR and deploy new version to Elastic Beanstalk](https://github.com/jamino30/dandi-search-response-ui/actions/workflows/deploy_new_version.yml/badge.svg)](https://github.com/jamino30/dandi-search-response-ui/actions/workflows/deploy_new_version.yml)

![image](media/ui-demo.gif)

## Running Locally

1. Create ```envfile.txt``` (in root directory) and fill with the following environment variables.
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
docker run --env-file envfile.txt -p 8000:8000 dsru-app
```

## Deployment

In order to deploy a new version, please invoke the `deploy_new_version` workflow with your desired branch in 
GitHub Actions.

## Purpose

- Dandi's LLM-powered search enhances user experience by enabling precise retrieval of relevant dandisets based on scientific inquiries, surpassing basic text and semantic search methods
- The Dandi Search Response UI empowers users to actively contribute to the evaluation of semantic search performance and the creation of valuable testing datasets for model assessment.
- Through the optimization of semantic search performance and the identification of the most effective LLM-powered processes, we are paving the way to develop an optimal search engine tailored for the Dandi Archive

<img src="media/llm-search.drawio.svg" alt="LLM Search Roadmap">
