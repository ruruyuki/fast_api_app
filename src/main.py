from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from starlette.templating import Jinja2Templates 
from starlette.requests import Request

# 正常トークン
correct_token = "correct_token"

# 模擬ユーザーデータ
dummy_user_db = {
    "abcde12345": {"id": "abcde12345", "name": "Yamada", "email_address": "yamada@example.com"},
    "fghij67890": {"id": "fghij67890", "name": "Tanaka", "email_address": "tanaka@example.com"},
}

app = FastAPI()

class User(BaseModel):
    id: str
    name: str
    email_address: str

@app.get("/")
async def index():
    return {"message": "Hello World"}

# ユーザー情報取得API
@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str, token: str = Header(...)):
    # トークン不正時
    if token != correct_token:
        raise HTTPException(
            status_code=400, detail="token_verification_failed")
    # ユーザー非存在時
    if user_id not in dummy_user_db:
        raise HTTPException(status_code=404, detail="user_not_found")
    return dummy_user_db[user_id]


# ユーザー情報登録API
@app.post("/users/", response_model=User)
async def create_user(user: User, token: str = Header(...)):
    # トークン不正時
    if token != correct_token:
        raise HTTPException(
            status_code=400, detail="token_verification_failed")
    # ユーザーID重複時
    if user.id in dummy_user_db:
        raise HTTPException(status_code=400, detail="user_id_duplicated")
    dummy_user_db[user.id] = user
    return user
