import pymysql


def getAllDish():
    # 获得所有菜品信息
    # 输出依次为：菜名，描述，价格，图片URL
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select dish_id, dname, ddesc, price, durl from dish order by dish_id"
    cursor.execute(sql)
    ret = cursor.fetchall()
    return ret


def getDishesByCategory(category: str):
    if category == "RecommendDish":
        return getRecDishesInfo()
    elif category == "HotDish":
        return getHotDishesInfo()
    else:
        return getColdDishesInfo()


def getRecDishesInfo():
    # 获得推荐菜信息，其他同上
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select dish_id, dname, ddesc, price, durl from dish where recommend = 1 order by dish_id"
    cursor.execute(sql)
    ret = cursor.fetchall()
    return ret


def getHotDishesInfo():
    # 获得热菜信息，其他同上
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select dish_id, dname, ddesc, price, durl from dish where hot = 1 order by dish_id"
    cursor.execute(sql)
    ret = cursor.fetchall()
    return ret


def getColdDishesInfo():
    # 获得凉菜信息，其他同上
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select dish_id, dname, ddesc, price, durl from dish where hot = 0 order by dish_id"
    cursor.execute(sql)
    ret = cursor.fetchall()
    return ret

# 通过uid查询uid对应的用户的类别和密码


def getWaiterAllOrder(sid: str):
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    # 获得给定服务员的订单，从给出的参数开始往后的四条,不足五条就显示剩下的
    # 输出依次为：订单号，桌号，起始时间，结束时间，总金额，
    # 是否开始烹饪，是否完成烹饪，是否付款，服务员编号，厨师编号
    sql = "select * from ord where waiter_id = %s order by start_time desc"
    cursor.execute(sql, sid)
    ret = cursor.fetchall()
    return ret


# 获取所有桌子的状态信息
def getTableStatus():
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    # 获得桌子状态，从给出的参数开始往后的8条，不足就显示剩下的
    # 输出依次为：桌号，最大人数，当前人数，是否占用
    sql = "select * from desk order by desk_id"
    cursor.execute(sql)
    ret = cursor.fetchall()
    return ret

# 获取模糊搜索的结果


def searchDishInfo(key: str):
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    # 菜品模糊查询，如果没有结果返回False，其他同上
    sql = "select dish_id, dname, ddesc, price, durl from dish where dname like %s order by dish_id"
    key = '%'+key+'%'
    cursor.execute(sql,key)
    ret = cursor.fetchall()
    if len(ret) == 0:
        return False
    else :
        return ret


# 服务员选择桌号和顾客
def selectTable(table_num, guest_num):
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    # 选择桌号和顾客人数，如果桌不存在或无法容纳顾客，返回False
    #否则返回True, 改变桌状态
    sql = "select max_people from desk where desk_id = %s and used = 0"
    cursor.execute(sql, table_num)
    ret = cursor.fetchall()
    if len(ret) == 0:
        return False
    elif ret[0][0] < int(guest_num):
        return False
    else:
        sql = "update desk set used = 1, now_people = %s where desk_id = %s"
        data = [guest_num, table_num]
        cursor.execute(sql, data)
        conn.commit()
        return True


def orderDishes(table_num, sid, date, dish_array, money):
    # 提交点餐信息，如果当前桌不存在未完成的订单，则新建订单，否则在订单上增加菜品
    # 输入：桌号，服务员号，当前时间， 格式 YYYY-MM-DD HH:MM:SS
    #      菜品列表，表中每个元素为菜品编号和数量组成的二元组，
    #      金额，提供已计算出的结果，
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select ord_id from ord where deskid_in_ord = %s and finished_ord = 0"
    cursor.execute(sql, table_num)
    ret = cursor.fetchall()
    if len(ret) == 0:
        # 此时创建新订单
        try:
            try:
                # 在ord中加入新订单
                sql = "insert into ord (deskid_in_ord, start_time, money, waiter_id, start_make, finished_make, finished_ord) values(%s,%s,%s,%s,0,0,0)"
                data = [table_num, date, money, sid]
                cursor.execute(sql, data)
                conn.commit()
            except:
                conn.rollback()
                return False
            try:
                # 找到加入的订单的订单号
                sql = "select ord_id from ord where deskid_in_ord = %s and finished_ord = 0"
                cursor.execute(sql, table_num)
                ret = cursor.fetchall()
            except:
                conn.rollback()
                return False
            try:
                # 在dishes中加入相应菜品
                sql = "insert into dishes (dishid_in_dishes, dish_num, ordid_in_dishes) values(%s,%s,%s)"
                data = []
                for item in dish_array:
                    data.append([item[0], item[1], ret])
                cursor.executemany(sql, data)
                conn.commit()
                return ret
            except:
                conn.rollback()
                return False
        except:
            conn.rollback()
            return False
    else:
        # 此时在原有订单上加钱加菜
        try:
            try:
                # 改变总金额
                sql = "update ord set money = money + %s where deskid_in_ord = %s and finished_ord = 0"
                data = [money, table_num]
                cursor.execute(sql, data)
            except:
                conn.rollback()
                return False
            try:
                # 加菜品
                for item in dish_array:
                    sql = "select * from dishes where dishid_in_dishes = %s and ordid_in_dishes = %s"
                    data = [item[0], ret]
                    cursor.execute(sql, data)
                    ret1 = cursor.fetchall()
                    #如果原订单有对应菜品，则增加其数量；如果没有，则新增对应内容
                    if len(ret1) == 0:
                        sql = "insert into dishes (dishid_in_dishes, dish_num, ordid_in_dishes) values(%s,%s,%s)"
                        data = [item[0], item[1], ret]
                        cursor.execute(sql, data)
                    else:
                        sql = "update dishes set dish_num = dish_num + %s where dishid_in_dishes = %s and ordid_in_dishes = %s"
                        data = [item[1], item[0], ret]
                        cursor.execute(sql, data)
                conn.commit()
            except:
                conn.rollback()
                return False
            try:
                # 新提交了菜品，设置订单为未完成
                sql = "update ord set finished_make = 0 where ord_id = %s"
                cursor.execute(sql, ret)
                conn.commit()
            except:
                conn.rollback()
                return False
        except:
            conn.rollback()
            return False
    return True



def getOrdById(ord_id):
    #获得给定订单的菜品详细信息,依次为菜品名称，菜品数量，对应订单号
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor=conn.cursor()
    sql = "select * from dishes where ordid_in_dishes = %s"
    cursor.execute(sql,ord_id)
    ret = cursor.fetchall()
    if len(ret) == 0 :
        return False
    else :
        ret1 = list(ret)
        ret2 = []
        for item in ret1:
            item = list(item)
            sql = "select dname from dish where dish_id = %s"
            cursor.execute(sql,item[0])
            ret3 = cursor.fetchall()
            ret2.append([ret3[0][0],item[1],item[2]])
        return ret2



def finishOrder(ordid, date):
    # 结账，输入账单id，改变账单状态为已结账
    # date格式： YYYY-MM-DD HH:MM:SS
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)
    cursor = conn.cursor()
    sql = "select * from ord where ord_id = %s and finished_ord = 0 and finished_make = 1"
    cursor.execute(sql,ordid)
    ret = cursor.fetchall()
    if len(ret) == 0:
        return False
    else :
        try :
            try :
                # 更改订单信息为已完成
                sql = "update ord set finished_ord = 1 where ord_id = %s"
                cursor.execute(sql, ordid)
                conn.commit()
            except :
                conn.rollback()
                return False
            try :
                #写上结束时间
                sql = "update ord set end_time = %s where ord_id = %s"
                data = [date,ordid]
                cursor.execute(sql,data)
                conn.commit()
            except :
                conn.rollback()
                return False
            try :
                #更改桌状态为空闲,当前人数为0
                sql = "select deskid_in_ord from ord where ord_id = %s"
                cursor.execute(sql,ordid)
                ret = cursor.fetchall()
                if len(ret) == 0:
                    return False
                else :
                    sql = "update desk set used = 0, now_people = 1 where desk_id = %s"
                    cursor.execute(sql,ret)
                    conn.commit()
            except :
                conn.rollback()
                return False
        except :
            conn.rollback()
            return False
        return True

