"""
从ip.cn中获取电话号码是否为骚扰号码

防止恶意使用软件
:TODO
建立数据库记录骚扰号码，针对恶意添加正常号码的用户，进行降权处理
"""
from requests_html import HTMLSession

phone = input('Phone: ')

domian = 'https://ip.cn/'
basic_url = 'db.php?num={}'.format(phone)

session = HTMLSession()

r = session.get(domian + basic_url)

# 找城市
try:
    city = r.html.search('所在城市: {}<br />')[0]
except TypeError:
    city = None

# 找号码
try:
    phone_type = r.html.search('：{}（仅供参考）')[0]
except TypeError:
    try:
        adv_url = r.html.search('基础数据库中无相关记录，请尝试<a href="{}">高级搜索</a>')[0]
    except TypeError:
        adv_url = None

    # 再找
    r = session.get(domian + adv_url)
    try:
        phone_type = r.html.search('：{}（仅供参考）')[0]
    except TypeError:
        phone_type = None

print(city)
print(phone_type)