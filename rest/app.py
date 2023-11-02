from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from .get_secrets import get_secrets

from .script import scan_for_relevant_dandisets
from .clients.aws_s3 import S3Bucket

app = FastAPI()
templates = Jinja2Templates(directory="static")

@app.on_event("startup")
async def startup_event():
    get_secrets()

class QueryItem(BaseModel):
    query: str

class ResponseItem(BaseModel):
    data: dict


@app.post("/scan/")
async def scan_query(query_item: QueryItem):
    try:
        result: dict = scan_for_relevant_dandisets(query_item.query)
        return result
    except Exception as e:
        return {"error": str(e)}, 500

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def submit_data(responses: ResponseItem):
    s3_client = S3Bucket("dandi-search-bucket")

    try:
        s3_client.put_json_object(responses.data)
        return {"message": "Responses uploaded"}
    except Exception as e:
        return {"error": str(e)}


# read styling and script files
@app.get("/styles.css", response_class=FileResponse)
async def read_css():
    return "static/styles.css"

@app.get("/scripts/{script_name}", response_class=FileResponse)
async def read_script(script_name: str):
    return f"static/scripts/{script_name}"