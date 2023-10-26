import uvicorn
import sys
from os.path import dirname, abspath

sys.path.append(abspath(dirname(__file__)))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)