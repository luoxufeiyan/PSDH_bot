""" 怼骚扰电话的业务 """

# 进行电话格式验证 Done
# 进行队列任务分配
# 进行电话负载分配
# 进行随机次数控制，次数返回
# 进行呼叫频率控制

from flask import make_response

from . import api_v1
from .decorators import ratelimit, cors
from .call import get_validated_phone_num

@api_v1.route('/', methods=['GET', 'POST'])
@ratelimit(requests=100, window=60, by="ip")
@cors
def diss_call():
    """ 无聊的Joke """
    return 'It\'s working, tk u.'



# 在Response Header中注入ratelimit信息
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