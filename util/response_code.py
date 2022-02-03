from fastapi import status
from fastapi.responses import JSONResponse, Response  # , ORJSONResponse
from typing import Union


def resp(res):
    if res:
        return resp_200(res)
    return resp_400(res)
         
#操作失败返回信息
def resp_400(res) -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'code': 400,
            'message': "failure",
            'data': res,
        }
    )
    

#操作成功返回
def resp_200(res) -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': 200,
            'message': "Success",
            'data': res,
        }
    )
