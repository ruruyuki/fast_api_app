from urls import app
import uvicorn

if __name__ == '__main__':
    # コンソールのこのファイルがある階層で [$ uvicorn run:app --reload]を実行
    uvicorn.run(app=app, port=8000)
