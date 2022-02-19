from sqlalchemy import create_engine
from api.models.task import Base

'''
次のコマンドでこのスクリプトを実行することで、
DockerコンテナのMySQLにテーブルを作成する。
既に同名のテーブルがある場合は、削除してから作成される。

docker-compose exec todo_app poetry run python -m api.migrate_db
'''

DB_URL = "mysql+pymysql://root@db:3306/todo?charset=utf8"
engine = create_engine(DB_URL, echo=True)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()