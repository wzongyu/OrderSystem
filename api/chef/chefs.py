from fastapi import APIRouter
from fastapi import Body
from pydantic import BaseModel
from service import chefService
from typing import List
from util import response_code
import asyncio

router = APIRouter()
result = dict()

@router.get("/chef/ord/list", tags=['chef'])
async def getChefList(uid:str):
    """
        获取厨师主页所需的订单，依次为\n
        [已开始但未完成订单，未开始订单，制作完成但未结账订单，已结账订单]
    """
    loop = asyncio.get_event_loop()
    r=await loop.run_in_executor(None,chefService.getChefList,uid)
    return response_code.resp(r)


@router.get("/chef/unstart/ord/list", tags=['chef'])
async def chefGetUnstartedOrder():
    """
        厨师获取没有没有开始制作的订单\n
        输出为：\n
        订单号，桌号，起始时间，结束时间，总金额，是否开始烹饪\n
        是否完成烹饪，是否付款，服务员编号，厨师编号
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, chefService.getUnstartedOrder)
    return response_code.resp(r)


@router.get("/chef/ord/detail/list", tags=['chef'])
async def chefGetOrdDetail(uid: str):
    """
        获得给定厨师的订单\n
        输入为给定厨师的id\n
        输出为订单详细信息，包括：\n
        订单号，桌号，起始时间，结束时间，总金额，是否开始烹饪\n
        是否完成烹饪，是否付款，服务员编号，厨师编号
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, chefService.getChefOrdDetail, uid)
    return response_code.resp(r)


@router.get("/chef/ord/search", tags=['chef'])
async def getOrdDetail(ord_id: int):
    """
        获取某个订单的详细信息，比如厨师需要点击某个订单才能知道自己需要做什么菜\n
        输入为：订单号\n
        输出为选定订单的详细信息，包括：菜品编号，菜品数量，对应订单号
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, chefService.getOrdDetail, ord_id)
    return response_code.resp(r)


@router.put("/chef/ord/start", tags=["chef"])
async def chefStart(*, ord_id: int = Body(...), uid: str = Body(...)):
    """
        输入为订单号以及厨师id,更改订单状态为开始制作\n
        并为订单指定厨师
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, chefService.chefStart, ord_id, uid)
    return response_code.resp(r)


@router.put("/chef/ord/finish", tags=["chef"])
async def chefFinish(ord_id: int = Body(...)):
    """
        订单完成，传入订单号，修改订单状态为已做完
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, chefService.chefFinish, ord_id)
    return response_code.resp(r)


@router.get("/chef/info/search", tags=["chef"])
async def getChefInfo(*, uid: str, date: str):
    """
        查询厨师信息，根据厨师id和日期获得厨师完成订单总数，\n
        厨师今日完成数（传入日期），厨师姓名
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, chefService.chefInfo, uid, date)
    return response_code.resp(r)
