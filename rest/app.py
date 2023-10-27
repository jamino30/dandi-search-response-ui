from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from script import scan_for_relevant_dandisets

import boto3
import json
import uuid

app = FastAPI()
templates = Jinja2Templates(directory="static")

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
    data = responses.data
    json_data = json.dumps(data)

    s3 = boto3.client("s3")
    bucket_name = "dandi-search-bucket"
    object_key = f"response_data_{uuid.uuid4()}.json"

    try:
        s3.put_object(
            Bucket=bucket_name, 
            Key=object_key, 
            Body=json_data,
            ContentType="application/json"
        )
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