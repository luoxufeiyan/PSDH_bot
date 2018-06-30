""" 怼骚扰电话的业务 """

# 输入电话号码，返回True or False
# 进行电话格式验证
# 进行队列任务分配
# 进行电话负载分配
# 进行随机次数控制，次数返回
# 进行呼叫频率控制

from flask import make_response

from . import api_v1
from .decorators import ratelimit, cors

@api_v1.route('/', methods=['GET', 'POST'])
@ratelimit(requests=100, window=60, by="ip")
@cors
def diss_call():
    """ 无聊的Joke """
    return 'It\'s working, tk u.'



@api_v1.after_request
def inject_rate_limit_headers(response):
    """ 将ratelimit信息写入response header """
    try:
        requests, remaining, reset = map(int, g.view_limits)
    except (AttributeError, ValueError):
        return response
    else:
        h = response.headers
        h.add('X-RateLimit-Remaining', remaining)
        h.add('X-RateLimit-Limit', requests)
        h.add('X-RateLimit-Reset', reset)
        return response