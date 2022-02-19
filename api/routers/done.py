from fastapi import APIRouter


router = APIRouter()

'''
app = FastAPI() に app.include_router(task.router)という風に
渡すと定義したパスにアクセスできる
'''
@router.put("/tasks/{task_id}/done", response_model=None)
async def mark_task_as_done(task_id: int):
    return


@router.delete("/tasks/{task_id}/done", response_model=None)
async def unmark_task_as_done(task_id: int):
    return