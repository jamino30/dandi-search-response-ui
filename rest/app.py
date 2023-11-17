from fastapi import FastAPI, BackgroundTasks, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool
from starlette.requests import Request
from pathlib import Path
import json

from .script import scan_for_relevant_dandisets
from .clients.aws_s3 import S3Bucket
from .clients.qdrant import QdrantClient
from .constants import OPENAI_COLLECTION_NAME, LLAMA2_COLLECTION_NAME

# docker build -t main . && docker run --env-file envfile.txt -p 8000:8000 main

app = FastAPI()
templates = Jinja2Templates(directory="static")

@app.on_event("startup")
async def startup_event():    
    qdrant_client = QdrantClient(host="https://906c3b3f-d3ff-4497-905f-2d7089487cf9.us-east4-0.gcp.cloud.qdrant.io")
    
    if not qdrant_client.has_collection(collection_name=OPENAI_COLLECTION_NAME):
        with open(str(Path.cwd() / "data/qdrant_points_ada002.json"), "r") as openai_file:
            openai_emb = json.load(openai_file)
        qdrant_client.update_collection(collection_name=OPENAI_COLLECTION_NAME, emb=openai_emb)
    
    # if not qdrant_client.has_collection(collection_name=LLAMA2_COLLECTION_NAME):
    #     with open(str(Path.cwd() / "data/qdrant_points_llama2.json"), "r") as llama2_file:
    #         llama2_emb = json.load(llama2_file)
    #     qdrant_client.update_collection(collection_name=LLAMA2_COLLECTION_NAME, emb=llama2_emb)
    
    app.state.qdrant_client = qdrant_client


class QueryItem(BaseModel):
    query: str
    model: str

class ResponseItem(BaseModel):
    data: dict

def get_qdrant_client(request: Request) -> QdrantClient:
    return request.app.state.qdrant_client

@app.post("/scan/")
async def scan_query(query_item: QueryItem, qdrant_client: QdrantClient = Depends(get_qdrant_client)):
    try:
        result: dict = await run_in_threadpool(scan_for_relevant_dandisets, query_item.query, query_item.model, qdrant_client)
        return result
    except Exception as e:
        return {"error": str(e)}, 500


def render_template(template_name: str, context: dict):
    return templates.TemplateResponse(template_name, context)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, background_tasks: BackgroundTasks):
    template_context = {"request": request}
    response = await run_in_threadpool(render_template, "index.html", template_context)
    return response


@app.post("/upload/")
def submit_data(responses: ResponseItem):
    s3_client = S3Bucket("dandi-search-llm-bucket")

    try:
        s3_client.put_json_object(responses.data)
        return {"message": "Responses uploaded"}
    except Exception as e:
        return {"error": str(e)}


# read styling and script files
@app.get("/styles.css", response_class=FileResponse)
def read_css():
    return "static/styles.css"

@app.get("/scripts/{script_name}", response_class=FileResponse)
def read_script(script_name: str):
    return f"static/scripts/{script_name}"