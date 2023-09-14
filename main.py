import os

import ujson
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from autocomplete import Autocomplete

data_path = os.path.join(os.getcwd(), "word_dict.json")
config_path = os.path.join(os.getcwd(), "config.json")
data = ujson.load(open(data_path))
CONFIG = ujson.load(open(config_path))
suggester = Autocomplete(data)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class WithoutKey(BaseModel):
    sentence: str
    with_score: bool


class WithKey(BaseModel):
    key: str
    sentence: str
    with_score: bool


@app.get("/")
def root():
    return {"message": "Autocomplete API"}


@app.get("/ping")
def ping():
    return "Pong"


@app.post("/suggest")
async def suggest_without_key(params: WithoutKey):
   
    result = suggester.autocomplete(
        params.sentence, 
        CONFIG["num_of_suggestions"],
        CONFIG["match_score"],
        CONFIG["n_grams"],
        params.with_score
    )

    return result


@app.post("/suggest_with_key")
async def suggest_with_key(params: WithKey):
    
    result = suggester.autocomplete_with_key(
        params.key,
        params.sentence,
        CONFIG["num_of_suggestions"],
        CONFIG["match_score"],
        CONFIG["n_grams"],
        params.with_score,
    )

    return result
