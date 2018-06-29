""" 怼骚扰电话的业务 """

from flask import make_response

from . import api_v1
from .decorators import ratelimit, cors

@api_v1.route('/', methods=['GET', 'POST'])
@ratelimit(requests=100, window=60, by="ip")
@cors
def diss_call():
    """ 无聊的Joke """
    return 'It\'s working, tk u.'