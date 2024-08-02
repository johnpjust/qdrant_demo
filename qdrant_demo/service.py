import os
import json
from typing import Optional

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from qdrant_demo.config import COLLECTION_NAME, STATIC_DIR
from qdrant_demo.neural_searcher import NeuralSearcher
from qdrant_demo.text_searcher import TextSearcher

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

neural_searcher = NeuralSearcher(collection_name=COLLECTION_NAME)
text_searcher = TextSearcher(collection_name=COLLECTION_NAME)


@app.get("/api/search")
async def read_item(q: str, neural: bool = True, filter_: Optional[str] = None, n_limit: Optional[int] = 5):
    filter_dict = json.loads(filter_) if filter_ else None
    return {
        "result": neural_searcher.search(text=q, filter_=filter_dict, n_limit=n_limit)
        if neural else text_searcher.search(query=q, top=n_limit)
    }


# Mount the static files directory once the search endpoint is defined
if os.path.exists(STATIC_DIR):
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
