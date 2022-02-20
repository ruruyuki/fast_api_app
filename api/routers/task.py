from typing import List
import api.schemas.task as task_schema
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import api.cruds.task as task_crud
from api.db import get_db
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

# データ取得処理
# @router.get("/tasks", response_model=List[task_schema.Task])
# async def list_tasks():
#     return [task_schema.Task(id=1, title="1つ目のTODOタスク")]

@router.get("/tasks", response_model=List[task_schema.Task])
async def list_tasks(db: AsyncSession = Depends(get_db)):
    return await task_crud.get_tasks_with_done(db)

# 新規作成処理
'''
Depends(get_db)
Depends は引数に関数を取り、 DI（Dependency Injection、依存性注入） を行う機構です。
DB接続部分にDIを利用することにより、ビジネスロジックとDBが密結合になることを防ぎます。
また、DIによってこのdbインスタンスの中身を外部からoverrideすることが可能になるため、
例えばテストのときに get_db と異なるテスト用の接続先に置換するといったことが、
プロダクションコードに触れることなく可能になります。
'''
@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_task(
    task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)
):
    return await task_crud.create_task(db, task_body)

# 更新処理
# @router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
# async def update_task(task_id: int, task_body: task_schema.TaskCreate):
#     return task_schema.TaskCreateResponse(id=task_id, **task_body.dict())

@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(
    task_id: int, task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)
):
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.update_task(db, task_body, original=task)

# 削除処理
# @router.delete("/tasks/{task_id}", response_model=None)
# async def delete_task(task_id: int):
#     return

@router.delete("/tasks/{task_id}", response_model=None)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.delete_task(db, original=task)