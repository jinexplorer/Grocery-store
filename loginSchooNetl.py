from urllib import request, parse
from time import sleep
from json import loads

post_addr = "http://172.19.1.9:8080/eportal/InterFace.do?method=login"
# 构造头部信息
post_header = {
    "Host": "172.19.1.9:8080",
    "Content-Length": "644",
    "Connection": "close",
    "Origin": "http://172.19.1.9:8080",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "http://172.19.1.9:8080/eportal/index.jsp?wlanuserip=beefd37236ad24b372def63e48efb960&wlanacname=29185648f4390d7911ef4b72391e17a9&ssid=&nasip=07e38f2323f330cd5ffcc3a203a63100&snmpagentip=&mac=76a76aa0d9af97790e57660bec3057d9&t=wireless-v2&url=7a093a207aab0e95932eb67bccf785d20fe9aa859a2b111f&apmac=&nasid=29185648f4390d7911ef4b72391e17a9&vid=0b48d4743b10aedb&port=a9ab84ca008a26fd&nasportid=ac41d60d7f1382084fc1d18ad6536cc7df9fae47b5358e4fce545d52bf5a53e4",
    "Cookie": "EPORTAL_COOKIE_OPERATORPWD=; EPORTAL_COOKIE_DOMAIN=false; EPORTAL_COOKIE_SAVEPASSWORD=true; EPORTAL_AUTO_LAND=; EPORTAL_COOKIE_SERVER=Internet; EPORTAL_COOKIE_SERVER_NAME=%E6%A0%A1%E5%9B%AD%E7%BD%91; EPORTAL_USER_GROUP=%E5%AD%A6%E7%94%9F%E7%BB%84; JSESSIONID=BE64245CE15AE48CFDBD4AB1401C4A8A; JSESSIONID=DFB1AE53EBB7772C90410CACE0EACA87",
}
# 构造登录数据
post_data = {
    "operatorPwd": "",
    "operatorUserId": "",
    "validcode": "",
    "password": "自己的密码",
    "passwordEncrypt": "false",
    "queryString": "wlanuserip%3D86f694a5007920906ea2537d99e09590%26wlanacname%3D29185648f4390d7911ef4b72391e17a9%26ssid%3D%26nasip%3D07e38f2323f330cd5ffcc3a203a63100%26snmpagentip%3D%26mac%3D553f3ca4d9c59eb75b7a4c12b5a5d6b7%26t%3Dwireless-v2%26url%3D795c649bdeb10f4d128564e205ba1187cd9b30eea35f80ae%26apmac%3D%26nasid%3D29185648f4390d7911ef4b72391e17a9%26vid%3Dc582ca585e3d05d4%26port%3D4326a7ab1ebddb5c%26nasportid%3Dac41d60d7f1382088c220df2f2050e37891284c528e29206d80a6890c845ae12",
    "service": "Internet",
    "userId": "自己的用户名",
}
# 此处为了重复发送数据包，来源是自己需要使用teamviewer，但是校园网崩溃。所以
# 这个函数就不停发送数据包，知道连上网为止。
def wait(time):
    for i in range(time, 0, -1):
        print("\r", i, "s后重新发送数据包", end="")
        sleep(1)
    print("")


def main():
    # 将要发送的数据格式化
    params = parse.urlencode(post_data).encode(encoding="UTF8")
    # 发送post请求登录网页
    req = request.Request(post_addr, headers=post_header, data=params)
    while True:
        try:
            with request.urlopen(req) as f:
                # 返回码不是200，应该就是校园网不通
                if f.status == 200:
                    print("Status:", f.status, f.reason)
                    data = f.read()
                    data_json = loads(data)
                    print(data_json["message"])
                    if data_json["result"] == "success":
                        break
                else:
                    print("校园网崩溃了")
                # 登陆失败就等一分钟再登录
                wait(60)
        except:
            print("我连不上网了")
            wait(60)


if __name__ == "__main__":
    main()

