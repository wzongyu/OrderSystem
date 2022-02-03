import pymysql

# 从数据库中获取所有未完成的订单


def getUnstartedOrder():
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    # 返回所有没有开始制作的订单，按时间排序,从指定的条数开始往后给四条
    # 输出依次为：订单号，桌号，起始时间，结束时间，总金额，
    #          是否开始烹饪，是否完成烹饪，是否付款，服务员编号，厨师编号
    sql = "select * from ord where start_make = 0 order by start_time desc"
    cursor.execute(sql)
    ret = cursor.fetchall()
    return ret
   
def getChefList(uid):
    #获取厨师界面所需数据，依次为[已开始但未完成订单，未开始订单，制作完成但未结账订单，已结账订单]
    list1 = getStartedOrder(uid)
    list2 = getUnstartedOrder()
    list3 = getFinishedMakeOrder(uid)
    list4 = getFinishedOrder(uid)
    chefList = [*list1, *list2, *list3, *list4]
    # print(chefList)
    return chefList

def getChefOrderDetail(uid):
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    # 获得给定厨师的订单详细信息，从给出的参数开始往后的四条,不足五条就显示剩下的
    # 输出内容按顺序：订单号，桌号，起始时间，结束时间，总金额，
    #          是否开始烹饪，是否完成烹饪，是否付款，服务员编号，厨师编号
    sql = "select * from ord where cook_id = %s order by start_time desc"
    cursor.execute(sql, uid)
    ret = cursor.fetchall()
    return ret

def getStartedOrder(cook_id):
    #返回该厨师的开始制作但没有制作完成的订单，按时间排序，越晚的订单越靠前
    #输出同上
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select * from ord where start_make = 1 and finished_make = 0 and cook_id = %s order by start_time desc"
    cursor.execute(sql,cook_id)
    ret = cursor.fetchall()
    return ret

def getFinishedMakeOrder(cook_id):
    #返回该厨师制作完成但没有结账的订单，其余同上
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select * from ord where finished_make = 1 and finished_ord = 0 and cook_id = %s order by start_time desc"
    cursor.execute(sql,cook_id)
    ret = cursor.fetchall()
    return ret

def getFinishedOrder(cook_id):
    #返回该厨师已结账的订单，其余同上
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select * from ord where finished_ord = 1 and cook_id = %s order by start_time desc"
    cursor.execute(sql, cook_id)
    ret = cursor.fetchall()
    return ret

def getOrderDetail(ord_id):
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    # 获得给定订单的菜品详细信息,依次为菜品编号，菜品数量，对应订单号
    sql = "select * from dishes where ordid_in_dishes = %s"
    cursor.execute(sql, ord_id)
    ret = cursor.fetchall()
    if len(ret) == 0:
        return False
    else:
        return ret


def startMakeOrder(ord_id, sid):
    # 更改指定订单状态为开始制作,并确定制作厨师
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)

    cursor = conn.cursor()
    sql = "select * from ord where ord_id = %s and start_make = 0"
    cursor.execute(sql, ord_id)
    ret = cursor.fetchall()
    if len(ret) == 0:
        return False
    else:
        try:
            try:
                # 更改为开始制作
                sql = "update ord set start_make = 1 where ord_id = %s"
                cursor.execute(sql, ord_id)
                conn.commit()
            except:
                conn.rollback()
                return False
            try:
                # 指定厨师
                sql = "update ord set cook_id = %s where ord_id = %s"
                data = [sid, ord_id]
                cursor.execute(sql, data)
                conn.commit()
            except:
                conn.rollback()
                return False
        except:
            conn.rollback()
            return False
        return True


def finishMakeOrder(ord_id):
    # 更改指定订单状态为完成制作
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)

    cursor = conn.cursor()
    sql = "select * from ord where ord_id = %s and start_make = 1 and finished_make = 0"
    cursor.execute(sql, ord_id)
    ret = cursor.fetchall()
    if len(ret) == 0:
        return False
    else:
        try:
            sql = "update ord set finished_make = 1 where ord_id = %s"
            cursor.execute(sql, ord_id)
            conn.commit()
        except:
            conn.rollback()
            return False
        return True


def getChefInfo(sid, date):
    # 获得厨师总订单数和今日订单数以及厨师姓名,按顺序返回三个
    # 注意这里的date涉及到模糊查询，请以YYYY-MM-DD或MM-DD格式输入,不要输入时分秒！
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select count(*) from ord where cook_id = %s"
    cursor.execute(sql, sid)
    total = cursor.fetchall()
    sql = "select count(*) from ord where cook_id = %s and start_time like %s"
    date = '%'+date+'%'
    data = [sid, date]
    cursor.execute(sql, data)
    today = cursor.fetchall()
    #返回厨师的姓名
    sql = "select name from stuff where sid = %s"
    cursor.execute(sql, sid)
    name = cursor.fetchall()
    return total, today, name
