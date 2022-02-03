from fastapi import APIRouter
from pydantic import BaseModel
from service import userService
from util import response_code
import asyncio

router = APIRouter()
class account(BaseModel):
    uid: str
    pwd: str

result = dict()

@router.put("/user/login",tags=["user"])
async def userLogin(acco: account):
    """
        用户登录 
        输入用户名和密码
        根据密码是否匹配返回用户，包括用户身份（1、2、3分别代表管理员、服务员、后厨），\n
        用户姓名，用户头像url
    """
    loop = asyncio.get_event_loop()#采用事件循环实现协程并行
    r = await loop.run_in_executor(None, userService.getUser, acco.uid, acco.pwd)
    return response_code.resp(r)

