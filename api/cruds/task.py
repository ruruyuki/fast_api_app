from sqlalchemy.ext.asyncio import AsyncSession
import api.models.task as task_model
import api.schemas.task as task_schema
from typing import List, Tuple
from sqlalchemy import select
from sqlalchemy.engine import Result
from typing import List, Tuple, Optional

# データ作成処理
async def create_task(
    db: AsyncSession, task_create: task_schema.TaskCreate
) -> task_model.Task:
    task = task_model.Task(**task_create.dict())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

# データ取得処理
async def get_tasks_with_done(db: AsyncSession) -> List[Tuple[int, str, bool]]:
    result: Result = await (
        db.execute(
            select(
                task_model.Task.id,
                task_model.Task.title,
                task_model.Done.id.isnot(None).label("done"),
            ).outerjoin(task_model.Done)
        )
    )
    return result.all()

'''
get_task() では、 .filter() を使って SELECT ~ WHERE として対象を絞り込んでいます。
'''
# 更新処理(サブ)
async def get_task(db: AsyncSession, task_id: int) -> Optional[task_model.Task]:
    result: Result = await db.execute(
        select(task_model.Task).filter(task_model.Task.id == task_id)
    )
    task: Optional[Tuple[task_model.Task]] = result.first()
    return task[0] if task is not None else None  # 要素が一つであってもtupleで返却されるので１つ目の要素を取り出す

'''
update_task() は create_task() とほとんど見た目が同じです。
original としてDBモデルを受け取り、これの中身を更新して返却しているのが唯一の差分です。
'''
# 更新処理(メイン)
async def update_task(
    db: AsyncSession, task_create: task_schema.TaskCreate, original: task_model.Task
) -> task_model.Task:
    original.title = task_create.title
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original

# 削除処理
async def delete_task(db: AsyncSession, original: task_model.Task) -> None:
    await db.delete(original)
    await db.commit()