from dao import chefDao


def getChefList(uid):
    #获取厨师主页所需订单
    Info = chefDao.getChefList(uid)
    currInfo = []
    #datetime转化为str可序列化对象
    for ord in Info:
        tmpOrd=list(ord)
        tmpOrd[2] = str(tmpOrd[2])
        tmpOrd[3] = str(tmpOrd[3])
        currInfo.append(tmpOrd)
    return currInfo

# 厨师获取所有未开始的订单信息
def getUnstartedOrder():
    Info = chefDao.getUnstartedOrder()
    return Info

# 某个厨师自己的订单信息
def getChefOrdDetail(uid: str):
    Info = chefDao.getChefOrderDetail(uid)
    return Info

# 获取单个订单的详情
def getOrdDetail(ordid: int):
    Info = chefDao.getOrderDetail(ordid)
    return Info


def chefStart(ord_id: int, uid: str):
    Info = chefDao.startMakeOrder(ord_id, uid)
    return Info


def chefFinish(ord_id: int):
    Info = chefDao.finishMakeOrder(ord_id)
    return Info


def chefInfo(uid: str, date: str):
    Info = chefDao.getChefInfo(uid, date)
    return Info
