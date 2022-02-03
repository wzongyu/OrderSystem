from dao import loginDao


def getUser(uid: str,pwd:str):
    user = loginDao.getUser(uid)
    if user and user[0][0]==pwd:#用户存在且密码正确 返回用户身份
        return user[0][1:]
    return False
