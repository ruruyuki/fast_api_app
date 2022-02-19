from fastapi import FastAPI
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.responses import HTMLResponse
import pathlib
import uvicorn


app = FastAPI()

# テンプレートの設定 (jinja2)
# templates = Jinja2Templates(directory="templates") 
#jinja_env = templates.env  # Jinja2.Environment : filterやglobalの設定用
 
# @app.get("/", response_class=HTMLResponse)
# async def site_index(request: Request):
#     """test subpage"""
#     title = "test page"
#     return templates.TemplateResponse(
#         "index.html",   # `templates`ディレクトリにおける相対パス
#         context={   # 変数をdict形式で渡すことが出来る
#             "request": request,
#             "title": title,
#         }
#     )

# response_class=HTMLResponse はreturnがhtmlであることを教える
@app.get("/",response_class=HTMLResponse)
async def site_index():
    return """
        <html>
            <head>
                <title>Hello World page</title>
            </head>
            <body>
                <h1>Hello World !!</h1>
            </body>
        </html>
        """

if __name__ == '__main__':
    # コンソールから実行する場合は [$ uvicorn run:app --reload]を実行
    uvicorn.run(app=app, port=8888)