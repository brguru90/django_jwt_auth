
from django.conf import settings
from functools import wraps
from django.http.response import JsonResponse,HttpResponse
from .models import tokenBlackList
from django.db.models import Q
import jwt
import json,datetime,random,sys
from inspect import currentframe, getframeinfo



class MyException(Exception):
    pass


def set_token(data,uname):
    access_token_payload = {
        'data':data,
        'uname':uname,
        'token_id':str(random.randint(1,1000))+"_"+str(datetime.datetime.utcnow().timestamp()),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=settings.JWT_TOKEN_EXPIRE),
        'iat': datetime.datetime.utcnow(),
    }
    # access_token = jwt.encode(access_token_payload,
    #                         settings.PRIVATE_KEY, algorithm='RS256').decode('utf-8')
    access_token = jwt.encode(access_token_payload,
                            settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    return access_token

def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
        domain=settings.SESSION_COOKIE_DOMAIN,
        secure=settings.SESSION_COOKIE_SECURE or None,
        httponly=True
    )


def login_check(param1=None):
    def decorator(view_func):
        @wraps(view_func)
        def validator(request, *args, **kwargs):   
            status = {
                "status": "no info",
                "msg_type": "info"
            }        
            try:  
                if "Authorization" in request.headers:
                    access_token = request.headers.get('Authorization')
                elif "access_token" in request.COOKIES:
                    access_token=request.COOKIES.get("access_token")
                else:
                    raise MyException("did not received token")
                # payload = jwt.decode(access_token, settings.PUBLIC_KEY, algorithms=['RS256'])
                payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
                block_listed=tokenBlackList.objects.filter(Q(userid=payload["uname"]) & (Q(block_token=payload["token_id"]) | Q(block_until_date__gt=datetime.datetime.fromtimestamp(payload["iat"])))  ).count()
                if block_listed>0:
                    raise MyException("User logged out")

                return view_func(request, payload,*args, **kwargs) 
                
            except jwt.ExpiredSignatureError:
                status = {
                    "status": "Token expired",
                    "msg_type": "error"
                }
            except IndexError:
                status = {
                    "status": "Token prefix missing",
                    "msg_type": "error"
                }

            except MyException as e:
                status = {
                    "status": str(e),
                    "msg_type": "error"
                }
            except Exception as e:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__,getframeinfo(currentframe()).filename, e)
                status = {
                    "status": "Unknown error",
                    "msg_type": "error"
                }
            return JsonResponse(status)

        return validator
    return decorator


LOGOUT_ERR=["success","fail","exception"]

def black_list_token(token_payload):
    try:
        token_black_list=tokenBlackList()
        token_black_list.userid=token_payload["uname"]
        token_black_list.block_token=token_payload["token_id"]
        token_black_list.save()
        if token_black_list != None:
            return LOGOUT_ERR[0]
        else:
            return LOGOUT_ERR[1]
    except:
        return LOGOUT_ERR[2]


def black_list_tokens_from(token_payload,block_list_token_created_from_date):
    try:
        token_black_list=tokenBlackList()
        token_black_list.userid=token_payload["uname"]
        token_black_list.block_until_date=block_list_token_created_from_date
        token_black_list.save()
        if token_black_list != None:
            return LOGOUT_ERR[0]
        else:
            return LOGOUT_ERR[1]
    except:
        return LOGOUT_ERR[2]
