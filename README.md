# Dandi Search Response UI

[![llmsearch.dandiarchive.org](https://img.shields.io/badge/dandiarchive-llmsearch-<COLOR>?style=flat&color=blue)](https://llmsearch.dandiarchive.org/)
[![Push Docker image to ECR](https://github.com/jamino30/dandi-search-response-ui/actions/workflows/deploy_new_version.yml/badge.svg)](https://github.com/jamino30/dandi-search-response-ui/actions/workflows/deploy_new_version.yml)

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

Important: Ensure to change `DANDI_COLLECTION` constant in `rest/constants/` to `dandi_collection`.

In order to deploy a new version, please invoke the `deploy_new_version` workflow with your desired branch in 
GitHub Actions.

## Stress-testing

In order to stress test the app locally, we include a setup for Locust tooling.

Steps:

1. Edit the `stress-test/locustfile.py` to reflect simulating endpoints that can be invoked via the Locust test
2. Launch the Locust UI via `docker-compose -f docker-compose.locust.yml up --scale worker=4` -- note: you may need to bring up/down the containers locally to enable hot-reloading in your `locustfile.py`

## Purpose

- Dandi's LLM-powered search enhances user experience by enabling precise retrieval of relevant dandisets based on scientific inquiries, surpassing basic text and semantic search methods
- The Dandi Search Response UI empowers users to actively contribute to the evaluation of semantic search performance and the creation of valuable testing datasets for model assessment.
- Through the optimization of semantic search performance and the identification of the most effective LLM-powered processes, we are paving the way to develop an optimal search engine tailored for the Dandi Archive

<img src="media/llm-search.drawio.svg" alt="LLM Search Roadmap">

## Todo

- [ ] Avoid showing a fixed number of dandisets (but place a limit) to allow for more accurate results/responses (e.g. no relevant dandisets, 2 relevant dandisets). There is no point in forcing a fixed number of dandisets if they have no relevance at all.
- [ ] Allow users to upload their own Dandiset IDs that do not appear in the list (but may be relevant to the query or may seem like they are related to the query but are not).
- [ ] Show confidence levels of dandisets chosen via similarity search (and place a threshold at which dandisets should be considered "relevant" or "not relevant").
- [ ] Improve vector embeddings used for similarity search to allow for identification of dandisets relevant to scientific or quantatitve queries (e.g. "Show me dandisets that contain two or more species.")

