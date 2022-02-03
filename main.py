import uvicorn
from fastapi import FastAPI
from api import userLogin
from api import waiters
from api import chefs
from api import admins

from starlette.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

app = FastAPI()

# 配置跨域
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

# 注册api路由
app.include_router(userLogin.router, prefix="/api")
app.include_router(waiters.router, prefix="/api")
app.include_router(chefs.router, prefix="/api")
app.include_router(admins.router, prefix="/api")


if __name__ == '__main__':
    uvicorn.run(app, host='192.168.43.190', port=10086)