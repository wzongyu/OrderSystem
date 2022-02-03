import pymysql


#这四个函数用来辅助获取主页所需要的全部信息
def getIncomeDaily(date: str):
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    # 获得指定日期营业额
    sql = "select sum(money) from ord where start_time like %s and finished_ord = 1"
    date = '%'+date+'%'
    cursor.execute(sql, date)
    ret = cursor.fetchall()
    return ret


def getUnfinishedOrderMoney():
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    # 获得待结算订单总金额
    sql = "select sum(money) from ord where finished_ord = 0"
    cursor.execute(sql)
    ret = cursor.fetchall()
    return ret


def getValidOrderNumToday(date):
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    # 获得今日有效订单数
    sql = "select count(*) from ord where start_time like %s and finished_ord = 1"
    date = '%'+date+'%'
    cursor.execute(sql, date)
    ret = cursor.fetchall()
    return ret


def getUnfinishedOrderNum():
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    # 获得待结算订单数
    sql = "select count(*) from ord where finished_ord = 0"
    cursor.execute(sql)
    ret = cursor.fetchall()
    return ret


def getHomePageInfo(date: str):
    """
        该函数需要调用其它函数，上面四个函数分别用来
        获取主页四个信息
    """
    info = []
    info.extend(getIncomeDaily(date))
    info.extend(getUnfinishedOrderMoney())
    info.extend(getValidOrderNumToday(date))
    info.extend(getUnfinishedOrderNum())
    return info


def showAllDishesInfo():
    # 返回菜品信息，从指定的位置开始,给8个
    # 信息包含菜品编号和菜品名称
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select dish_id, dname from dish order by dish_id"
    cursor.execute(sql)
    ret = cursor.fetchall()
    return ret


def showHotDishesInfo():
    # 返回热菜信息，从指定位置开始，给8个
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select dish_id, dname from dish where hot = 1 order by dish_id"
    cursor.execute(sql)
    ret = cursor.fetchall()
    return ret


def showColdDishesInfo():
    # 返回凉菜信息，从指定位置开始，给8个
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select dish_id, dname from dish where hot = 0 order by dish_id"
    cursor.execute(sql)
    ret = cursor.fetchall()
    return ret


def showRecDishesInfo():
    # 返回推荐菜信息，从指定位置开始，给8个
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select dish_id, dname from dish where recommend = 1 order by dish_id"
    cursor.execute(sql)
    ret = cursor.fetchall()
    return ret


def showDishDetail(dish_id):
    # 返回指定菜品详细信息
    # 输出依次为：菜品编号，菜品名字，菜品描述，菜品细节描述，图片URL，
    #            是否推荐，是否为热菜，单价
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select * from dish where dish_id = %s"
    cursor.execute(sql, dish_id)
    ret = cursor.fetchall()
    return ret


def changeDishDetail(dish_id, dname, ddesc, ddetail, rec, hot, price):
    # 修改指定菜品详细信息，这里的输入顺序和上一个函数输出顺序一样
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select * from dish where dish_id = %s"
    cursor.execute(sql, dish_id)
    ret = cursor.fetchall()
    if len(ret) == 0:
        return False
    else:
        sql = "update dish set dname=%s,ddesc=%s,ddetail=%s,recommend=%s,hot=%s,price=%s where dish_id = %s"
        data = [dname, ddesc, ddetail, rec, hot, price, dish_id]
        cursor.execute(sql, data)
        conn.commit()
        return True


def addDish(dname, ddesc, ddetail, durl, rec, hot, price):
    # 增加菜品，除了没有菜品编号，输入顺序同上
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select * from dish where dname = %s"
    cursor.execute(sql, dname)
    ret = cursor.fetchall()
    if len(ret) != 0:
        return False
    else:
        try:
            sql = "insert into dish(dname,ddesc,ddetail,durl,recommend,hot,price) values(%s,%s,%s,%s,%s,%s,%s)"
            data = [dname, ddesc, ddetail, durl, rec, hot, price]
            cursor.execute(sql, data)
            conn.commit()
        except:
            conn.rollback()
            return False
        return True


def deleteDish(dish_id):
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select * from dish where dish_id = %s"
    cursor.execute(sql, dish_id)
    ret = cursor.fetchall()
    if len(ret) == 0:
        return False
    else:
        try:
            # 存在外键限制，先删除所有相应订单
            sql = "delete from dishes where dishid_in_dishes = %s"
            cursor.execute(sql, dish_id)
            conn.commit()
        except:
            conn.rollback()
            return False
        try:
            # 删除菜品
            sql = "delete from dish where dish_id = %s"
            cursor.execute(sql, dish_id)
            conn.commit()
        except:
            conn.rollback()
            return False
        return True


def getTableStatus():
    # 获得桌子状态，从给出的参数开始往后的8条，不足就显示剩下的
    # 输出依次为：桌号，最大人数，当前人数，是否占用
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select * from desk order by desk_id"
    cursor.execute(sql)
    ret = cursor.fetchall()
    return ret


def addTable(max_people):
    # 创建新桌子，输入最大容纳人数
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    try:
        sql = "insert into desk(max_people,now_people,used) values(%s,%s,%s)"
        data = [max_people, "0", "0"]
        cursor.execute(sql, data)
        conn.commit()
    except:
        conn.rollback()
        return False
    return True


def deleteTable(desk_id):
    #输入桌号，删除对应桌子,如果桌子不存在，或该桌子正在被使用，不能删除该桌子
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select * from desk where desk_id = %s and used = 0"
    cursor.execute(sql,desk_id)
    ret = cursor.fetchall()
    if len(ret) == 0 :
        return False
    else :
        try :
            sql = "delete from desk where desk_id = %s"
            cursor.execute(sql,desk_id)
            conn.commit()
            return True
        except :
            conn.rollback()
            return False


def changeTable(desk_id, max_people):
    # 改变对应桌号的最大接待人数
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select * from desk where desk_id = %s and now_people <= %s"
    data = [desk_id,max_people]
    cursor.execute(sql,data)
    ret = cursor.fetchall()
    if len(ret) == 0 :
        return False
    else :
        try :
            sql = "update desk set max_people = %s where desk_id = %s"
            data = [max_people,desk_id]
            cursor.execute(sql,data)
            conn.commit()
            return True
        except :
            conn.rollback()
            return False


def addStuff(stype, name,sid, password, surl):
    # 添加员工，如果存在就修改员工信息
    # 输入依次为员工类别，员工姓名，员工名,密码MD5,图片URL
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select * from stuff where sid = %s"
    cursor.execute(sql, sid)
    ret = cursor.fetchall()
    if len(ret) == 0:
        # 如果原来不存在，创建新的
        try:
            sql = "insert into stuff(stype,name,sid,spass,surl) values(%s,%s,%s,%s,%s)"
            data = [stype, name, sid, password, surl]
            cursor.execute(sql, data)
            conn.commit()
            return True
        except:
            conn.rollback()
            return False
    else:
        # 原来已存在，修改密码和图片和名字
        try:
            sql = "update stuff set spass = %s, surl = %s, name = %s where sid = %s"
            data = [password, surl, name, sid]
            cursor.execute(sql, data)
            conn.commit()
            return True
        except:
            conn.rollback()
            return False


def deleteStuff(sid):
    # 删除员工
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select * from stuff where sid = %s and stype > 1"
    cursor.execute(sql, sid)
    ret = cursor.fetchall()
    if len(ret) == 0:
        return False
    else:
        try:
            sql = "delete from stuff where sid = %s"
            cursor.execute(sql, sid)
            conn.commit()
            return True
        except:
            conn.rollback()
            return False


def getYearEarning(date):
    # 输入年份 YYYY
    # 返回近三年每年的收入，和订单数，两个数组
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    income = []
    order = []
    for i in range(3):
        sql = "select sum(money) from ord where start_time like %s"
        cursor.execute(sql, '%'+date+'%')
        ret = cursor.fetchall()
        income.append(ret)
        sql = "select count(*) from ord where start_time like %s"
        cursor.execute(sql, '%'+date+'%')
        ret = cursor.fetchall()
        order.append(ret)
        date = str(int(date) - 1)
    return income, order


def getMonthEarning(date):
    # 输入月份 YYYY-MM
    # 返回近三月每月的收入，和订单数，两个数组
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    income = []
    order = []
    for i in range(3):
        print(date)
        sql = "select sum(money) from ord where start_time like %s"
        cursor.execute(sql, '%' + date + '%')
        ret = cursor.fetchall()
        income.append(ret)
        sql = "select count(*) from ord where start_time like %s"
        cursor.execute(sql, '%' + date + '%')
        ret = cursor.fetchall()
        order.append(ret)
        temp = date.split('-')
        if int(temp[1]) != 1:
            temp[1] = str(int(temp[1])-1)
            if int(temp[1]) < 10:
                date = temp[0]+'-0'+temp[1]
            else:
                date = temp[0] + '-' + temp[1]
        else:
            temp[0] = str(int(temp[0])-1)
            date = temp[0]+'-12'
    return income, order

def getstuffbyname():
    #获取所有信息
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',user='hth',password='123456789h!',db='term_v1',port=3306) 
    cursor = conn.cursor()
    sql = "select * from stuff order by name"
    cursor.execute(sql)
    ret = cursor.fetchall()
    return ret
