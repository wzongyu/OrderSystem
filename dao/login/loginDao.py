import pymysql

conn = None
cursor = None
sql = None


# def init():
#     global conn, cursor
#     conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
#                            user='hth', password='123456789h!', db='term_v1', port=3306)
#     cursor = conn.cursor()


def getUser(uid: str):
    conn = pymysql.connect(host='rm-bp1kz3v2eopayao5s6o.mysql.rds.aliyuncs.com',
                           user='hth', password='123456789h!', db='term_v1', port=3306)

    cursor = conn.cursor()
    # 登录，输入id,不存在则返回False,存在则返回密码MD5,员工类别,姓名和surl
    sql = "select spass, stype, name, surl from stuff where sid = %s"
    cursor.execute(sql, uid)
    ret = cursor.fetchall()
    if len(ret) == 0:
        return False
    else:
        return ret


if __name__ == '__main__':
    print(getUser("admin"))
