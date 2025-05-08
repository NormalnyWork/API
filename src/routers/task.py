from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from const import defaultNULL
from database import get_session
from routers.auth import get_current_user
from schema.error import ErrorResponse
from schema.http_exeption import HttpException400, HttpException401
from schema.task import TaskStatus, TaskOut
from schema.user import UserOut
from service.task_service import TaskService

responses = {
    400: {"model": HttpException400},
    401: {"model": HttpException401}
}

router = APIRouter(prefix="/tasks", tags=["Tasks"], responses=responses)

@router.get("/today", response_model=List[TaskOut], responses={
    404: {
        "model": ErrorResponse,
        "description": "404\n- no_tasks_found_for_today"
    }
})
async def get_today_tasks(
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    tasks = TaskService(db).get_today_tasks(current_user.id)
    if not tasks:
        raise HTTPException(status_code=404, detail="no_tasks_found_for_today")

    return [
        TaskOut(
            id=task.id,
            care_type=task.care_type,
            scheduled_at=task.scheduled_at,
            status=task.status,
            plant_name=task.plant.name,
            plant_image=task.plant.image
        )
        for task in tasks
    ]


@router.put("/{task_id}/status", responses={
    200: defaultNULL,
    404: {
        "model": ErrorResponse,
        "description": "404\n- task_not_found"
    }
})
async def update_status(
    task_id: int,
    status: TaskStatus,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    updated_task = TaskService(db).update_task_status(task_id, status)
    return updated_task

@router.post("/{task_id}/postpone", responses={
    200: defaultNULL,
    404: {
        "model": ErrorResponse,
        "description": "404\n- task_not_found"
    }
})
async def postpone_task(
    task_id: int,
    db: Session = Depends(get_session),
    current_user: UserOut = Depends(get_current_user)
):
    TaskService(db).postpone_task(task_id)
