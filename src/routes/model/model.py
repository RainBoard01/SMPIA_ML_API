from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Depends, Security, status, File, UploadFile
from SMPIA_ML_MODEL.predict import predict
import shutil
import requests

from src.database import MongoDBConnectionManager
from src.config import ACCESS_TOKEN_DURATION_MINUTES
from src.auth import (
    User,
    Token,
    UserInDB,
    UserCreate,
    get_user,
    get_password_hash,
    authenticate_user,
    create_access_token,
    current_active_user,
)


model_routes = APIRouter()


@model_routes.get(
    "/predict-by-path", tags=["Model"]
)
async def predict_by_path(path:str):
    resultados = predict(path)
    # requests.post('http://localhost:1337/api/auth/local') # Just to test the connection with the backend
    return resultados

@model_routes.post(
	'/predict-by-file', tags=["Model"]
)
async def predict_by_file(file: UploadFile = File(...)):
    print(file)
    try:
        # Save the file in the server in temp folder, if not exists create it
        import os
        os.makedirs('SMPIA_ML_MODEL/.temp', exist_ok=True)
        with open(f'SMPIA_ML_MODEL/.temp/{file.filename}', 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Predict the results
        resultados = predict(f'.temp/{file.filename}')

        # Delete the folder and file
        shutil.rmtree('SMPIA_ML_MODEL/.temp')

        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))