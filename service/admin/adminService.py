from dao import adminDao
from util import uploadFile

def tableChange(desk_id: int, max_people: int):
    Info = adminDao.changeTable(desk_id, max_people)
    return Info


def stuffDelete(uid: str):
    Info = adminDao.deleteStuff(uid)
    return Info


def getYearEarning(data: str):
    Info = adminDao.getYearEarning(data)
    #返回格式修改
    ans = []
    for item in Info:
        ans.append([item[j][0][0] for j in range(3)])
    return ans


def getMonthEarning(data: str):
    Info = adminDao.getMonthEarning(data)
    #返回格式修改
    ans = []
    for item in Info:
        ans.append([item[j][0][0] for j in range(3)])
    return ans

# 获取主页


def getHomePage(date: str):
    Info = adminDao.getHomePageInfo(date)
    return Info

# 获取管理员界面的菜品信息


def showDishesInfo():
    Info = adminDao.showAllDishesInfo()
    return Info


def showHotDishes():
    Info = adminDao.showHotDishesInfo()
    return Info

def showColdDishes():
    Info = adminDao.showColdDishesInfo()
    return Info


def showRecDishes():
    Info = adminDao.showRecDishesInfo()
    return Info


def showDisheDetail(dish_id: int):
    Info = adminDao.showDishDetail(dish_id)
    return Info


def changeDishesDetail(dishid: int, dname: str, ddesc: str, ddetail: str,  rec: int, hot: int, price: float):
    Info = adminDao.changeDishDetail(dishid, dname, ddesc,
                                     ddetail, rec,
                                     hot, price)
    return Info


def addDish(dname: str, ddesc: str, ddetail: str, rec: int, hot: int, price: float,imgFile:bytes):
    path='/usr/java/apache-tomcat-8.5.69/webapps/img/dishes/'+dname+".jpg",
    with open(path, 'wb') as f:
        f.write(imgFile)
    durl = "http://139.196.191.74:8080/img/dishes/" + dname + ".jpg"
    Info = adminDao.addDish(dname, ddesc, ddetail, durl, rec, hot, price)
    return Info


def deleteDish(dishid: int):
    Info = adminDao.deleteDish(dishid)
    return Info


def getTableStatus():
    Info = adminDao.getTableStatus()
    return Info


def addTable(maxpeople: int):
    Info = adminDao.addTable(maxpeople)
    return Info


def deleteTable(deskid: int):
    Info = adminDao.deleteTable(deskid)
    return Info

def addStuff(stype: str, name: str, sid: str, password: str, file: bytes, imgName: str):
    path='/usr/java/apache-tomcat-8.5.69/webapps/img/'+stype+"/"+imgName
    with open(path, 'wb') as f:
        f.write(file)
    durl = "http://139.196.191.74:8080/img/users/" + stype + "/" + imgName

    if stype == "waiter":
        stype = "2"
    else:
        stype = "3"

    Info = adminDao.addStuff(stype, name,sid, password, durl)
    return durl

def getAllStuff():
    Info = adminDao.getstuffbyname()
    res_process = [dict() for i in range(26)]
    # 格式大框架
    for i in range(26):
        res_process[i]['stuff'] = chr(65 + i)
        res_process[i]['members'] = list()
    # 每一类里面添加新员工
    for stuff in Info:
        sign = ord(stuff[4][0]) - 65 # ascall码
        mydict = dict()
        mydict['name'] = stuff[4]
        mydict['uid'] = stuff[1]
        mydict['stype'] = stuff[0]
        mydict['pic'] = stuff[3]
        res_process[sign]['members'].append(mydict)
    return res_process