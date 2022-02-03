from dao import waiterDao


def queryDishByCategory(category: str):
    dishes = waiterDao.getDishesByCategory(category)
    return dishes


def queryAllDish():
    allDishes = waiterDao.getAllDish()
    return allDishes

# 查询某个服务员的订单信息
def queryAllOrd(sid: str):
    Info = waiterDao.getWaiterAllOrder(sid)
    currInfo = []
    #datetime转化为str可序列化对象
    for ord in Info:
        tmpOrd=list(ord)
        tmpOrd[2] = str(tmpOrd[2])
        tmpOrd[3] = str(tmpOrd[3])
        currInfo.append(tmpOrd)
    return currInfo

# 查询所有桌子的状态信息，输出依次为：桌号，最大人数，当前人数，是否占用
def queryDesk():
    Info = waiterDao.getTableStatus()
    return Info

# 模糊搜索，如果没有结果返回False，否则返回菜品的具体信息


def fuzzyQuery(key: str):
    Info = waiterDao.searchDishInfo(key)
    return Info


# 服务员选择桌号和顾客
def selectTable(table_num: int, guest_num: int):
    Info = waiterDao.selectTable(table_num, guest_num)
    return Info

# 服务员下单
def putOrders(table_num:int,uid:str,date:str,dish_array:list,money:float):
    Info = waiterDao.orderDishes(table_num, uid, date, dish_array, money)
    return Info

#查询单个订单详情
def queryOrd(ord_id: int):
    Info = waiterDao.getOrdById(ord_id)
    return Info

# 服务员完成订单
def finishOrd(ordid:int,date:str):
    Info = waiterDao.finishOrder(ordid,date)
    return Info
