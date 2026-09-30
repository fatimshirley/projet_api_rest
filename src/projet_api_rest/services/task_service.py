from sqlalchemy import select
from sqlalchemy.orm import Session

from projet_api_rest.models.task import Task
from projet_api_rest.models.user import User
from projet_api_rest.schemas.task import TaskCreate, TaskUpdate


def create_task(
    db: Session,
    task_data: TaskCreate,
    current_user: User,
) -> Task:
    task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        completed=False,
        user_id=current_user.id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_user_tasks(
    db: Session,
    current_user: User,
    completed: bool | None = None,
    priority: str | None = None,
) -> list[Task]:
    query = select(Task).where(
        Task.user_id == current_user.id
    )

    if completed is not None:
        query = query.where(
            Task.completed == completed
        )

    if priority is not None:
        query = query.where(
            Task.priority == priority
        )

    query = query.order_by(Task.id.desc())

    return list(db.scalars(query).all())


def get_user_task(
    db: Session,
    task_id: int,
    current_user: User,
) -> Task | None:
    return db.scalar(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == current_user.id,
        )
    )


def update_task(
    db: Session,
    task: Task,
    task_data: TaskUpdate,
) -> Task:
    update_data = task_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


def complete_task(
    db: Session,
    task: Task,
) -> Task:
    task.completed = True

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    db: Session,
    task: Task,
) -> None:
    db.delete(task)
    db.commit()
