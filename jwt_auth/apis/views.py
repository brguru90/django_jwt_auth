from django.conf import settings
from django.http.response import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.gzip import gzip_page

import json,datetime
from .own_middlewares import set_token,login_check,set_cookie

def test(request):
    status={
        "msg":"test success",
        "type":"success"
    }
    return JsonResponse(status)


@csrf_exempt
@ensure_csrf_cookie
def login(request):
    status={
        "msg":"no info",
        "type":"info"
    }
    access_token=None

    try:
        req_body=json.loads(request.body.decode())
        if "uname" not in req_body:
            raise Exception("uname not exists in request body")
        access_token=set_token(json.dumps({
            "uname":req_body["uname"]
        }))    
        status={
            "msg":"Login success",
            "type":"success",
            "access_token":access_token
        }

    except Exception as e:
        print(str(e))
        status={
            "msg":str(e),
            "type":"Error"
        }
    response=JsonResponse(status)
    if access_token:
        set_cookie(response,"access_token",access_token)
    return response


@login_check("decorator arg")
@gzip_page
def verify_login(request,token_data):
    status={
        "msg":"token data",
        "type":"info",
        "token_data":token_data
    }
    return JsonResponse(status)