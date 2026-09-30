from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from projet_api_rest.auth.dependencies import get_current_user
from projet_api_rest.database.connection import get_db
from projet_api_rest.models.user import User
from projet_api_rest.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from projet_api_rest.services.task_service import (
    complete_task,
    create_task,
    delete_task,
    get_user_task,
    get_user_tasks,
    update_task,
)


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_task(
        db,
        task_data,
        current_user,
    )


@router.get(
    "",
    response_model=list[TaskResponse],
)
def read_tasks(
    completed: bool | None = Query(
        default=None
    ),
    priority: Literal["low", "medium", "high"] | None = Query(
        default=None
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_tasks(
        db,
        current_user,
        completed,
        priority,
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_user_task(
        db,
        task_id,
        current_user,
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tâche introuvable.",
        )

    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_existing_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_user_task(
        db,
        task_id,
        current_user,
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tâche introuvable.",
        )

    return update_task(
        db,
        task,
        task_data,
    )


@router.patch(
    "/{task_id}/complete",
    response_model=TaskResponse,
)
def complete_existing_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_user_task(
        db,
        task_id,
        current_user,
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tâche introuvable.",
        )

    return complete_task(
        db,
        task,
    )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_user_task(
        db,
        task_id,
        current_user,
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tâche introuvable.",
        )

    delete_task(
        db,
        task,
    )

    return None
