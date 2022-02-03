from fastapi import APIRouter
from fastapi import Body
from pydantic import BaseModel
from service import waiterService
from typing import List
from util import response_code
import asyncio

router = APIRouter()


class Order(BaseModel):
    table_num: int
    uid: str
    date: str
    dish_array: List[list]
    money: float


result = dict()


@router.get("/waiter/all/ord/list", tags=['waiter'])
async def waiterQueryAllOrd(uid: str):
    """
        获取所有订单的接口，输入为员工编号(waiter1)\n
        输出为该员工对应的订单信息，订单详细信息包括：\n
        订单号；桌子号；开始时间；结束时间；总价格；（三个状态位）开始制作，结束制作，结束订单
        服务员号（str)，厨师号(str)
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, waiterService.queryAllOrd, uid)
    return response_code.resp(r)


@router.get("/waiter/ord/search", tags=["waiter"])
async def waiterQueryOrd(ord_id: int):
    """
        获取服务员单个订单的接口，输入为订单编号\n
        输出为该订单的详细信息,依次为菜品名称
        ，菜品数量，对应订单号
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, waiterService.queryOrd, ord_id)
    return response_code.resp(r)


@router.get("/waiter/desk/list", tags=['waiter'])
async def waiterQueryDesk():
    """
        获取所有桌子的状态接口\n
        输出为桌子对应的信息，包括：桌号，最大收纳人数，当前人数，是否有客人(0表示没有，1表示有)
    """

    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, waiterService.queryDesk)
    return response_code.resp(r)


@router.get("/waiter/dish/by/category/list", tags=["waiter"])
async def qDishByC(category: str):
    """
        根据类别返回当前类别下所有菜品
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, waiterService.queryDishByCategory, category)
    return response_code.resp(r)


@router.get("/waiter/all/dish/list", tags=["waiter"])
async def queryAllDish():
    """
        返回所有菜品信息：菜品id；菜品名称；简介；价格；图片url
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, waiterService.queryAllDish)
    return response_code.resp(r)


@router.get("/waiter/dish/fuzzy/list", tags=['waiter'])
async def waiterFuzzyQuery(key: str):
    """
        菜品模糊查询，输入模糊关键字(查询字符串，例如"肉")\n
        输出为模糊查询的结果，具体信息为：\n
        菜品id；菜品名称；简介；价格；图片url
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, waiterService.fuzzyQuery, key)
    return response_code.resp(r)


@router.put("/waiter/select/table", tags=['waiter'])
async def waiterSelectTable(*, table_num: int = Body(...), guest_num: int = Body(...)):
    """
        服务员选择桌号和顾客人数\n
        输入为选择的桌号和顾客人数，输出为True/False\n
        如果没有这个桌号或者该桌子已经被占用或者人数超过最大容纳人数，则返回False\n
        否则返回True
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, waiterService.selectTable, table_num, guest_num)
    return response_code.resp(r)


@router.put("/waiter/put/orders", tags=['waiter'])
async def waiterPutOrders(order: Order):
    """
        服务员下单，若订单不存在则创建，否则修改 输入为\n
        桌号；服务员id；下单时间（格式为xxxx-xx-xx字符串)；菜单列表，格式如下\n
        [[菜1_id,数量],[菜2_id,数量],...];价格\n
        输出为True/False，表示下单失败或者成功

    """
    #时间格式转换
    currData=""
    tmp=order.date.split()
    for i in range(1,6):
        if len(tmp[i])==1:
            tmp[i]="0"+tmp[1]
    currData=tmp[0]+"-"+tmp[1]+"-"+tmp[2]+" "+tmp[3]+":"+tmp[4]+":"+tmp[5]
    order.date=currData


    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, waiterService.putOrders, order.table_num,
                                    order.uid, order.date, order.dish_array,
                                    order.money)
    return response_code.resp(r)


@router.put("/waiter/finish/order", tags=["waiter"])
async def waiterFinishOrder(*, ordid: int = Body(...), date: str = Body(...)):
    """
        服务员完成订单，输入为订单号和日期\n
        日期格式为 YYYY-MM-DD hh:mm:ss\n
        输出为 True / False（有对应订单则输出为True,否则为False）
    """
    #时间格式转换
    currDate=""
    tmp=date.split()
    for i in range(1,6):
        if len(tmp[i])==1:
            tmp[i]="0"+tmp[1]
    currDate=tmp[0]+"-"+tmp[1]+"-"+tmp[2]+" "+tmp[3]+":"+tmp[4]+":"+tmp[5]

    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, waiterService.finishOrd, ordid, currDate)
    return response_code.resp(r)
