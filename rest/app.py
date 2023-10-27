from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from script import scan_for_relevant_dandisets

app = FastAPI()
templates = Jinja2Templates(directory="static")


class QueryItem(BaseModel):
    query: str


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

# @app.get("/submit/")
# async def submit_data(data: str = Form(...)):
#     json_data = {"key": data}

#     s3 = boto3.client("s3", )



@app.get("/styles.css", response_class=FileResponse)
async def read_css():
    return "static/styles.css"

@app.get("/scripts/{script_name}", response_class=FileResponse)
async def read_script(script_name: str):
    return f"static/scripts/{script_name}"