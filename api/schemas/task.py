from typing import Optional

from pydantic import BaseModel, Field

'''
このファイルは、FastAPIのスキーマを表す。
APIのスキーマは、APIのリクエストやレスポンスの型を定義するためのもので、
データベースのスキーマとは異なる。
BaseModel はFastAPIのスキーマモデルであることを表すので、このクラスを継承して Task クラスを作成する。
右辺の Field はフィールドに関する付加情報を記述する。最初の変数はフィールドのデフォルト値を表す。
title は None 、 done は False をデフォルト値に取っているのがわかります。
example はフィールドの値の例をとります。
'''
class TaskBase(BaseModel):
    title: Optional[str] = Field(None, example="クリーニングを取りに行く")

class TaskCreate(TaskBase):
    pass

class TaskCreateResponse(TaskCreate):
    id: int

    class Config:
        orm_mode = True

class Task(TaskBase):
    id: int
    done: bool = Field(False, description="完了フラグ")

    class Config:
        orm_mode = True

