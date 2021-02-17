import json
from fastapi import FastAPI, UploadFile, File,HTTPException
import pydantic
from pydantic import BaseModel
from datetime import datetime


app = FastAPI()

with open('shows.json', 'r') as f:
    shows = json.load(f)

show = shows['_embedded']['episodes']

class nb_of_episodes(BaseModel):
    seasons: list = []

class episode_titles(BaseModel):
    seasons: list = []
    episodes: list = []

class episode_by_date(BaseModel):
    date: str = pydantic.Field(default="2011-01-01", example="2011-01-01")

@app.post("/episodes/counts")
async def number_of_episodes(item: nb_of_episodes):
    try:
        seasons = item.seasons
        ep = 0
        i = 0
        for it in show:
            if show[i]['season'] in seasons:
                ep = ep +1
            i=i+1
        return {"Total number of episodes is ": ep}
    except Exception as ex:
        raise HTTPException(status_code=404, detail="error reading Database")

@app.post("/episodes/title")
async def episode_title(item: episode_titles):
    try:
        seasons = item.seasons
        ep = item.episodes
        i = 0
        names = []
        for it in show:
            if show[i]['season'] in seasons and show[i]['number'] in ep:
                names.append(show[i]['name'])
            i = i+1
        if not names:
            return {"Invalid season or episode number"}
        else:
            return {"tiles are ": names}
    except Exception as ex:
        raise HTTPException(status_code=404, detail="error!!")

@app.post("/date")
async def episode_date(item: episode_by_date):
    try:
        datee = item.date
        date = datetime.strptime(datee,'%Y-%m-%d')
    except Exception as ex:
        raise HTTPException(status_code=300, detail="date should be yyyy-mm-dd")
    try:
        date = item.date
        i = 0
        names = []
        for it in show:
            if show[i]['airdate'] < date:
                names.append(show[i]['name'])
            i = i + 1
        return {"tiles are ": names}
    except Exception as ex:
        raise HTTPException(status_code=404, detail="error!!")