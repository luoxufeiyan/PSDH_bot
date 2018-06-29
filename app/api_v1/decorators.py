""" api 装饰器 """

from functools import wraps
from time import time
from flask import g, request, Response, make_response
from app import redis_store

# http://blog.wongxinjie.com/2016/03/26/简洁Flask-RESTful-API设计/
# 此装饰器版权归上述网址作者所有
# Modified by Paul
def ratelimit(requests=100, window=60, by="ip"):
    """
    api接口请求限制

    Args:
        request     单位时间内限制总请求次数
        window      单位时间长度（秒）
        by          用来区分用户信息的keyID

    Return: 返回请求频率限制的装饰器
    """
    if not callable(by):
        by = {'ip': lambda: request.remote_addr}[by]

    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            key = ":".join(["ratelimit", by()])
            try:
                remaining = requests - int(redis_store.get(key))
            except (ValueError, TypeError):
                remaining = requests
                redis_store.set(key, 0)

            ttl = redis_store.ttl(key)
            if ttl < 0:
                # ttl = -2, ttl = -1
                redis_store.expire(key, window)
                ttl = window

            g.view_limits = (requests, remaining - 1, time() + ttl)

            if remaining > 0:
                redis_store.incr(key, 1)
                return func(*args, **kwargs)
            else:
                return Response("请求太过频繁", 429)
        return wrapped
    return decorator


def cors(func):
    """ 这里是cors的装饰器，没什么可注释的 """
    @wraps(func)
    def wrapper_func(*args, **kwargs):

        r = make_response(func(*args, **kwargs))
        
        r.headers['Access-Control-Allow-Origin'] = '*'
        r.headers['Access-Control-Allow-Methods'] = 'HEAD, OPTIONS, GET, POST, DELETE, PUT'

        allow_headers = "Referer, Accept, Origin, User-Agent, X-Requested-With, Content-Type"
        r.headers['Access-Control-Allow-Headers'] = allow_headers

        if request.method == 'OPTIONS':
            return r
        return r
    return wrapper_func