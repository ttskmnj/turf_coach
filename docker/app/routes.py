from fastapi import APIRouter, Request, Path
from typing import Annotated
from models import Pitch, PitchUpdate, PitchCreate
from bson import ObjectId
from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta

load_dotenv()
OPENWETHERMAP_URL = os.getenv("OPENWETHERMAP_URL")
OPENWETHERMAP_KEY = os.getenv("OPENWETHERMAP_KEY")

router = APIRouter()


@router.post("/")
async def createPitch(pitch: PitchCreate, request: Request):
    new_pitch = request.app.database["pitch"].insert_one(dict(pitch))

    return {"message": f"new pitch: {new_pitch.inserted_id} is created"}


@router.get("/")
async def readAllPitch(request: Request) -> list[Pitch]:
    pitches = list(request.app.database["pitch"].find(limit=100))
    pitches = objId_to_str(pitches)
    return pitches


@router.get("/{id}")
async def readPitch(id: str, request: Request):
    pitch = request.app.database["pitch"].find_one({"_id": ObjectId(id)})

    if pitch is None:
        return {'error': f"pitch: {id} is not found"}

    pitch['_id'] = str(pitch['_id'])
    return pitch


@router.get("/update_next_maintenance/")
async def updatePitchNextMaintenance(request: Request):
    pitches_need_maintenance = []
    three_days_dt = datetime.now() + timedelta(days=3)
    three_days_ts = int(three_days_dt.timestamp())
    
    pitches = \
      request.app.database["pitch"].find(
          {"$and": [
              {"type": {"$ne": 0}},
              {"next_maintenace_date": {"$gt": three_days_dt}}
          ]}
      )
    
    for pitch in pitches:
        geo_code_raw = requests.get(f"{OPENWETHERMAP_URL}geo/1.0/direct?q={pitch['city']},{pitch['state']},{pitch['country']}&appid={OPENWETHERMAP_KEY}")
        geo_code = geo_code_raw.json()
        
        five_days_forecast_raw = requests.get(f"{OPENWETHERMAP_URL}data/2.5/forecast?lat={geo_code[0]['lat']}&lon={geo_code[0]['lat']}&appid={OPENWETHERMAP_KEY}")
        five_days_forecast = five_days_forecast_raw.json()

        need_maintenance = 1

        for forecast in five_days_forecast['list']:
            if forecast['dt'] > three_days_ts:
                break
            if forecast['weather'] == "Rain":
                need_maintenance = 0
                print("\n\n RAIN ##################################################")
                break

        if need_maintenance:
            pitches_need_maintenance.append(pitch)

    for pitch in pitches_need_maintenance:
        id = ObjectId(pitch.pop('_id'))
        pitch['next_maintenace_date'] = three_days_dt


        request.app.database["pitch"].update_one(
            {"_id": id}, {"$set": dict(pitch)}
        )

    return {'msg': "update next maintenance"}


@router.get("/need_maintenance/")
async def readPitchNeedMaintenance(request: Request) -> list[Pitch]:
    dt = datetime.now() + timedelta(days=3)

    pitches = \
      request.app.database["pitch"].find(
          {"$and": [
              {"type": {"$ne": 0}},
              {"next_maintenace_date": {"$lt": dt}}
          ]}
      )
    pitches = objId_to_str(list(pitches))
    
    return pitches


@router.put("/{id}")
async def updatePitch(
    id: Annotated[str, Path()],
    pitch_update: PitchUpdate, 
    request: Request
):
    updated_pitch =\
        request.app.database["pitch"].update_one(
            {"_id": ObjectId(id)}, {"$set": dict(pitch_update)}
        )

    if updated_pitch.matched_count == 0:
        return {'error': f"pitch: {id} is not found"}
    return {'msg':  f"pitch: {id} is updated"}


@router.delete("/{id}")
async def deletePitch(id: str, request: Request):
    deleted_pitch = request.app.database["pitch"].delete_one({"_id": ObjectId(id)})
    print(deleted_pitch.raw_result)
    if deleted_pitch.deleted_count == 0:
        return {'error': f"failed to delete pitch: {id}"}

    return {"message": f"pitch: {id} is deleted"}


def objId_to_str(pitches: list[Pitch]): 
    return_pitches = []
    for pitch in pitches:
        pitch['_id'] = str(pitch['_id'])
        return_pitches.append(pitch)

    return return_pitches