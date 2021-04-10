
from django.conf import settings
from functools import wraps
from django.http.response import JsonResponse,HttpResponse
import jwt
import json,datetime


def set_token(data):
    access_token_payload = {
        'data':data,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
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
                print("request.COOKIES",request.COOKIES)             
                if "Authorization" in request.headers:
                    access_token = request.headers.get('Authorization')
                elif "access_token" in request.COOKIES:
                    access_token=request.COOKIES.get("access_token")
                else:
                    raise Exception("did not received token")
                print("access_token",access_token)
                # payload = jwt.decode(access_token, settings.PUBLIC_KEY, algorithms=['RS256'])
                payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
                return view_func(request, payload,*args, **kwargs) 
                
            except jwt.ExpiredSignatureError:
                status = {
                    "status": "access_token expired",
                    "msg_type": "error"
                }
            except IndexError:
                status = {
                    "status": "Token prefix missing",
                    "msg_type": "error"
                }
            except Exception as e:
                print(str(e))
                status = {
                    "status": "Unknown error",
                    "msg_type": "error"
                }
            return JsonResponse(status)

        return validator
    return decorator