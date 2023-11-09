from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool

from .script import scan_for_relevant_dandisets
from .clients.aws_s3 import S3Bucket

# docker build -t main . && docker run --env-file envfile.txt -p 8000:8000 main

app = FastAPI()
templates = Jinja2Templates(directory="static")

class QueryItem(BaseModel):
    query: str

class ResponseItem(BaseModel):
    data: dict


@app.post("/scan/")
def scan_query(query_item: QueryItem):
    try:
        result: dict = scan_for_relevant_dandisets(query_item.query)
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