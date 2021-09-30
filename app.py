from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import numpy as np
from joblib import load
import pandas as pd

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class Item(BaseModel):
    tipo_prop: str
    tipo_viv: str
    prop_area: float
    habitaciones: int
    banos: int
    estrato: int
    ubicacion: str


@app.get("/home", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/api/")
async def send_item(item: Item):
    
    price_model = load("xgboost.joblib")
    X_data=pd.read_csv('x_labels.csv', sep=';')
    
    if item.tipo_prop=='nueva':
        X_data.loc[0,'tipo_Nueva']=1
    else:
        X_data.loc[0,'tipo_Usada']=1


    if item.tipo_viv=='apartamento':
        X_data.loc[0,'tipo_propiedad_apartamento']=1
    elif item.tipo_viv=='apartaestudio':
        X_data.loc[0,'tipo_propiedad_apartaestudio']=1
    elif item.tipo_viv=='casa':
        X_data.loc[0,'tipo_propiedad_casa']=1
    elif item.tipo_viv=='finca':
        X_data.loc[0,'tipo_propiedad_finca']=1

    X_data.loc[0,'area_m2']=item.prop_area
    X_data.loc[0,'habitaciones']=item.habitaciones
    X_data.loc[0,'banos']=item.banos
    X_data.loc[0,'estrato']=item.estrato


    if item.ubicacion=='rionegro':
        X_data.loc[0,'ubicacion_rionegro']=1

    elif item.ubicacion=='llanogrande':
        X_data.loc[0,'ubicacion_llanogrande']=1

    elif item.ubicacion=='marinilla':
        X_data.loc[0,'ubicacion_marinilla']=1

    elif item.ubicacion=='el retiro':
        X_data.loc[0,'ubicacion_el retiro']=1

    elif item.ubicacion=='la ceja':
        X_data.loc[0,'ubicacion_la ceja']=1

    elif item.ubicacion=='el carmen de viboral':
        X_data.loc[0,'ubicacion_el carmen de viboral']=1

    elif item.ubicacion=='san antonio de pereira':
        X_data.loc[0,'ubicacion_san antonio de pereira']=1

    elif item.ubicacion=='guarne':
        X_data.loc[0,'ubicacion_guarne']=1

    elif item.ubicacion=='santuario':
        X_data.loc[0,'ubicacion_santuario']=1
     
          
    stimated_price=price_model.predict(X_data)[0]

    print(stimated_price)

    json_compatible_item_data = jsonable_encoder({'status':'OK', 'stimated_price':stimated_price.item()})
    return JSONResponse(content=json_compatible_item_data)
