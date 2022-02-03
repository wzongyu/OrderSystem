from util import uploadFile
from fastapi import APIRouter
from fastapi import Body
from pydantic import BaseModel
from service import adminService
from fastapi import File
from typing import List
from util import response_code
from fastapi import Form
import asyncio

router = APIRouter()
result = dict()


class Desk(BaseModel):
    desk_id: int
    max_people: int


class Dish1(BaseModel):
    dishid: int
    dname: str
    ddesc: str
    ddetail: str
    # durl: str
    rec: int
    hot: int
    price: float


# 菜品详细信息类2，不包含菜id
class Dish2(BaseModel):
    dname: str=Form(...)
    ddesc: str=Form(...)
    ddetail: str=Form(...)
    # durl: str
    rec: int=Form(...)
    hot: int=Form(...)
    price: float=Form(...)


@router.get("/admin/homepage/search", tags=['admin'])
async def getHomePage(date: str):
    """
        该接口主要用来获取管理员的主页\n
        输入：YYYY-MM-DD\n
        输出：今日总营业额；待结算订单金额；今日有效订单数；待结算订单数
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, adminService.getHomePage, date)
    return response_code.resp(r)


@router.get("/admin/all/dish/list", tags=['admin'])
async def showAllDishsInfo():
    """
        该接口主要用来返回菜品信息\n
        输出为：[[菜品编号,菜品名称],...]
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, adminService.showDishesInfo)
    return response_code.resp(r)


@router.get("/admin/hotdish/list", tags=['admin'])
async def showHotDishes():
    """ 
        该接口用来返回热菜类别的信息\n
        输出为：热菜信息 [[菜品编号,菜品名称],...]
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, adminService.showHotDishes)
    return response_code.resp(r)


@router.get("/admin/colddish/list", tags=['admin'])
async def showColdDishes():
    """ 
        该接口用来返回凉菜类别的信息\n
        输出为：[[菜品编号,菜品名称],...]
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, adminService.showColdDishes)
    return response_code.resp(r)


@router.get("/admin/recdish/list", tags=['admin'])
async def showRecDishes():
    """ 
        该接口用来返回推荐菜类别的信息\n
        输出为：[[菜品编号,菜品名称],...]
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, adminService.showRecDishes)
    return response_code.resp(r)


@router.get("/admin/dish/search", tags=['admin'])
async def showDisheDetail(dish_id: int):
    """ 
        该接口用来返回指定菜品详细信息\n
        输出为：指定菜品详细信息，[菜品编号，菜品名字，菜品描述，菜品细节描述，图片URL，
                                是否推荐，是否为热菜，单价]
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, adminService.showDisheDetail, dish_id)
    return response_code.resp(r)

#TODO 菜品url
@router.put("/admin/change/dish", tags=['admin'])
async def changeDishDetail(dish: Dish1):
    """
        该接口用来改变菜品的具体信息\n
        输入为：dish_id(菜品id)；dname(菜名称)；ddesc(描述)\n；
                ddetail(细节)；rec(是否推荐)；hot(是否热菜)；价格(price)\n
                file(菜品图片)\n
        输出为：True / False (表示成功或者失败)
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, adminService.changeDishesDetail, dish.dishid,
                                    dish.dname, dish.ddesc, dish.ddetail, 
                                    dish.rec, dish.hot, dish.price)
    return response_code.resp(r)


@router.put("/admin/add/dish", tags=['admin'])
async def addDish(file: bytes = File(...),
                  dname: str=Form(...),
                  ddesc: str=Form(...),
                  ddetail: str=Form(...),
                  rec: int=Form(...),
                  hot: int=Form(...),
                  price: float = Form(...)
               ):
    """
        该接口用于管理员添加新的菜品\n
        输入为：dname(菜名称)；ddesc(描述)；ddetail(细节)；\n
                rec(是否推荐)；hot(是否热菜)；价格(price)\n
                file(菜品图片)
        输出为 True / False
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, adminService.addDish, dname,
                                    ddesc, ddetail, rec,
                                    hot, price,file)
    return response_code.resp(r)


@router.delete("/admin/delete/dish", tags=['admin'])
async def deleteDish(dishid: int=Body(...)):
    """
        该接口用来删除菜品\n
        输入：需要删除的菜品id\n
        输出：True / False
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, adminService.deleteDish, dishid)
    return response_code.resp(r)


@router.get("/admin/table/status/list", tags=['admin'])
async def getTableStatus():
    """
        该接口主要用来获取所有餐桌状态\n
        输出为：桌号；最大人数；当前人数；是否占用
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, adminService.getTableStatus)
    return response_code.resp(r)


@router.put("/admin/add/table", tags=['admin'])
async def addTable(maxpeople: int = Body(...)):
    """
        创建新桌子\n
        输入为：最大容纳人数\n
        输出为：True / False
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, adminService.addTable, maxpeople)
    return response_code.resp(r)


@router.delete("/admin/delete/table", tags=['admin'])
async def deleteTable(deskid: int = Body(...)):
    """
        删除桌子\n
        输入为：餐桌ID\n
        输出为：True / False
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, adminService.deleteTable, deskid)
    return response_code.resp(r)


@router.put("/admin/change/desk", tags=['admin'])
async def changeDesk(desk: Desk):
    """
        修改桌子最大人数，输入为桌子id以及修改后的最大人数
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, adminService.tableChange, desk.desk_id,
                                    desk.max_people)
    return response_code.resp(r)


@router.delete("/admin/delete/stuff", tags=['admin'])
async def delStuff(uid: str=Body(...)):
    """
        删除员工，输入为员工uid
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, adminService.stuffDelete, uid)
    return response_code.resp(r)


@router.get("/admin/year/earning/serach", tags=['admin'])
async def getYearEarn(date: str=Body(...)):
    """
        输入年份 YYYY\n
        返回近三年每年的收入，和订单数，两个数组\n
        比如输入2021 返回21、20、19年收入和订单数\n
        返回 [[2021收入,2020月收入,2019月收入],[2021订单数,2020订单数,2019订单数]]
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, adminService.getYearEarning, date)
    return response_code.resp(r)


@router.get("/admin/month/earning/search", tags=['admin'])
async def getMonthEarn(date: str=Body(...)):
    """
        输入年份和月份 YYYY-MM\n
        返回近三月每月的收入，和订单数，两个数组\n
        比如输入2021-05 返回3、4、5月份收入和订单数\n
        返回 [[5月收入,4月收入,3月收入],[5月订单数,4月订单数,3月订单数]]
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, adminService.getMonthEarning, date)
    return response_code.resp(r)


@router.post("/admin/change/stuff/info",tags=["admin"])
async def addStuff(stype: str = Body(...), name: str = Body(...),
                    uid: str = Body(...), pwd: str = Body(...),
                    file: bytes = File(...)):
    """
        修改员工信息 若不存在则新建员工\n
        stype:员工类型\n
        name:员工姓名\n
        uid:员工账户\n
        pwd:账户密码\n
        file:选择员工头像
        返回头像url
    """
    imgName = uid+".jpg"
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, adminService.addStuff, stype, name,
                                uid, pwd, file, imgName)
    return r


@router.get("/admin/get/all/stuff/by/name",tags=['admin'])
async def GetAllStuffByName():
    """
        获取所有员工的信息
    """
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None,adminService.getAllStuff)
    return response_code.resp(r)
