from datetime import datetime
from decimal import Decimal
import logging
from fastapi import APIRouter, Depends, HTTPException, status

from services.queue.rabbitmq_connector import send_to_queue
from DTO.ml_task_create_request import MlTaskCreateRequest
from database.database import get_session
from DTO.ml_task_update_request_simple import MlTaskUpdateRequestSimple
from core.exceptions import PredictionError
from services.business_logic import prediction as PredictService

predict_route = APIRouter()

logger = logging.getLogger(__file__)



@predict_route.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    response_model = int)
async def predict(data: MlTaskCreateRequest, session=Depends(get_session)):
    try:
        task_id = PredictService.create_prediction(data, session)
    except PredictionError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return task_id

@predict_route.post("/update/positive",
    status_code=status.HTTP_200_OK,
    response_model = int)
async def update_predict(data: MlTaskUpdateRequestSimple, session=Depends(get_session)):
    logger.info(f'запрос {data}')
    try:
        task_id = PredictService.add_positive_result(data, session)
    except PredictionError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return task_id

@predict_route.post("/update/negative",
    status_code=status.HTTP_200_OK,
    response_model = int)
async def update_predict(data: MlTaskUpdateRequestSimple, session=Depends(get_session)):
    logger.info(f'запрос {data}')
    try:
        task_id = PredictService.add_negative_result(data, session)
    except PredictionError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return task_id