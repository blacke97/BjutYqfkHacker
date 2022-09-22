import requests
import re
import logging
import json
import os
import sys

token = ''
cookie = ''
username = ''
password = ''
postData = ''

def writeDate(fileName, content):
    with open(fileName, 'w', encoding='utf-8') as f:
        json.dump(content,f, ensure_ascii=False)

def readData(fileName):
    with open(fileName, 'r', encoding= 'utf-8') as f:
        res = json.load(f)
    return res


yqfkSession = requests.sessions.session()
itsappSession = requests.sessions.session()
casSession = requests.sessions.session()

yqfkHeaders = {
    'Host': 'yqfk.bjut.edu.cn',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)  Mobile/15E148 wxwork/4.0.16 MicroMessenger/7.0.1 Language/zh ColorScheme/Light',
    'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    #'Cookie': 'XSRF-TOKEN=eyJpdiI6IkNsNitWdGJsbksyS3lNUEhML2syM3c9PSIsInZhbHVlIjoieXF1Y3BNMzVEN0JlRjlSUXNNdU9KVlhhVHlDVXVJdHRKUFdNb0R6WHNmVGtERExGcWRsRjVtejdJWXQ0TWdrZnlwbXE0bkplRVZaNzhwbVJoRkllTFIwUDhHbVM1N1R1eUFDMGxseGpLemhXbEM1b0tzaTRhTmhJVXdraWFmTmsiLCJtYWMiOiI4MjEzOWM3N2YxMGM4MGMzNTNkYTVhMjc3ODIxOGUyMmYyMzkzOWQ1Yjc2ODFkYmFhY2E0MzUxNzAyYmI5MTU3In0%3D; _session=eyJpdiI6IkFnZVdZL1I2UjJ3dUNDNGlRd1VIc0E9PSIsInZhbHVlIjoiaTFYeWNkdEY3bXBVTlV5MktncVk2WWJwWU80TFJSV21oUEVQV3Z5Si9WREQvSjJvcm5idjc0NnlMb05JUWFpU1FnOE9RMGw5ZEp3OWxMYnF5cmlybFlxSFphQ28vcytDYndDSDBnNzBKdi9HNlJjVGEzdXhETG1IK2YvcnJnVlEiLCJtYWMiOiJhNWZhZjFhNjZkMDMxZDA5YjcwMjI3YTQ4OTk1ZTM1ZTNmNzQ1NzcyNjgwNzU0NTRhY2Q4ODU4ZGE4Nzk0NTJiIn0=',
    'Connection': 'keep-alive',
    'Sec-Fetch-Mode': 'navigate'
}

itsappHeaders = {
    'Host': 'itsapp.bjut.edu.cn',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive',
    #Cookie: UUkey=6ff5b197a75aa2553fe6de98d870f5e3; eai-sess=emk5qar3f8mk51povfg4pcl627
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)  Mobile/15E148 wxwork/4.0.16 MicroMessenger/7.0.1 Language/zh ColorScheme/Light',
    'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
    'Referer': 'https://yqfk.bjut.edu.cn/',
    'Accept-Encoding': 'gzip, deflate, br'
}

casHeaders = {
    'Host': 'cas.bjut.edu.cn',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive',
    #Cookie: _7da9a=c1a85815ecde0964
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)  Mobile/15E148 wxwork/4.0.16 MicroMessenger/7.0.1 Language/zh ColorScheme/Light',
    'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
    'Referer': 'https://yqfk.bjut.edu.cn/',
    'Accept-Encoding': 'gzip, deflate, br'
}

yqfkSession.headers = yqfkHeaders
casSession.headers = casHeaders
itsappSession.headers = itsappHeaders

def changeCurrentPath():

    myLogger = logging.getLogger('myLogger.info')

    paths = sys.path
    current_file = os.path.basename(__file__)
    for path in paths:
        try:
            if current_file in os.listdir(path):
                current_path = path
                os.chdir(current_path)
                myLogger.info("Current work path : " + os.getcwd())
                break
        except (FileExistsError,FileNotFoundError) as e:
            print(e)


def init():
    global cookie
    global token
    global username
    global password
    global postData

    myLogger = logging.getLogger('myLogger.info')
    myLogger.setLevel(logging.INFO)
    
    fh = logging.FileHandler('./info.log', encoding='utf-8', mode='a')
    formatter = logging.Formatter('%(asctime)s-%(levelname)s : %(message)s')
    fh.setFormatter(formatter)
    
    myLogger.addHandler(fh)

    changeCurrentPath()

    res = readData('./tmp.info')
    
    cookie = res['cookie']
    token = res['token']
    username = res['username']
    password = res['password']

    postData = readData('./data.dat')


def postDailyForm(cookie,token,clear):
    
    global yqfkSession
    
    myLogger = logging.getLogger('myLogger.info')
    
    if clear is True:
        yqfkSession.cookies.clear()
        yqfkSession.headers['Cookie'] = cookie
        yqfkSession.headers['Authorization'] = 'Bearer ' + token
    
    
    url = 'https://yqfk.bjut.edu.cn/api/home/daily_form'

    # yqfkSession.headers = yqfkHeaders
    res = yqfkSession.post(url, json=postData, verify = False)
    print(res.headers)
    print(res.request.headers)
    print(res.text)

    if 'json' in res.headers['Content-Type']:
        myLogger.info(res.json())
        return res.json()
    myLogger.warning('信息可能已经失效，重新登录中...')
    print('信息可能已经失效，重新登录中...')
    return -1


def loginAndPostDailyForm():

    myLogger = logging.getLogger('myLoger.info')

    # 有返回值的redirect方向  302
    url = 'https://yqfk.bjut.edu.cn/'
    res1 = yqfkSession.get(url ,verify = False)

    # print(res.text)
    # print(res.headers)
    # 302 有redirect方向，在Html内容中
    url2 = 'https://yqfk.bjut.edu.cn/api/login?url_back=pages/index/index'
    res2 = yqfkSession.get(url2 ,verify = False, allow_redirects=False)

    # print(res.text)
    # print(res.history)
    # print(res.headers)


    # 302 无返回值内容
    #url3 = 'https://itsapp.bjut.edu.cn/uc/api/oauth/index?redirect=http://yqfk.bjut.edu.cn/api/login/pages-index-index?login=1&appid=200220501233430304&state=STATE'
    url3 = res2.headers['Location']

    pattern2 = '&appid=(.*?)&state'
    myComp2 = re.compile(pattern2)
    appId = myComp2.findall(url3)[0]
    myLogger.info('appId={}'.format(appId))

    res3 = itsappSession.get(url3, verify = False, allow_redirects=False)

    # print(res3.text)
    # print(res3.request.headers)
    # print(res3.history)
    # print(res3.headers)

    # 302 无返回值
    # url4 = 'https://itsapp.bjut.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fitsapp.bjut.edu.cn%2Fuc%2Fapi%2Foauth%2Findex%3Fredirect%3Dhttp%3A%2F%2Fyqfk.bjut.edu.cn%2Fapi%2Flogin%2Fpages-index-index%3Flogin%3D1%26appid%3D200220501233430304%26state%3DSTATE'
    url4 = res3.headers['Location']
    res4 = itsappSession.get(url4, verify = False, allow_redirects = False)

    # 302 有redirect方向
    # url5 = 'https://itsapp.bjut.edu.cn/a_bjut/api/sso/index?redirect=https%3A%2F%2Fitsapp.bjut.edu.cn%2Fuc%2Fapi%2Foauth%2Findex%3Fredirect%3Dhttp%3A%2F%2Fyqfk.bjut.edu.cn%2Fapi%2Flogin%2Fpages-index-index%3Flogin%3D1%26appid%3D200220501233430304%26state%3DSTATE&from=wap'
    url5 = res4.headers['Location']
    res5 = itsappSession.get(url5, verify = False, allow_redirects = False)


    # 这个有可能直接调用就好了 200 统一身份认证接口
    #url6 = 'https://cas.bjut.edu.cn/login?service=https%3A%2F%2Fitsapp.bjut.edu.cn%2Fa_bjut%2Fapi%2Fsso%2Findex%3Fredirect%3Dhttps%253A%252F%252Fitsapp.bjut.edu.cn%252Fuc%252Fapi%252Foauth%252Findex%253Fredirect%253Dhttp%253A%252F%252Fyqfk.bjut.edu.cn%252Fapi%252Flogin%252Fpages-index-index%253Flogin%253D1%2526appid%253D200220501233430304%2526state%253DSTATE%26from%3Dwap'
    url6 = res5.headers['Location']

    res6 = casSession.get(url6,  verify = False)
    # print(res.request.headers)
    # print(res.text)
    # print(res.headers)

    text = res6.text
    pattern = '''<div style="display: none;">\n                <input name="type" value="username_password"/><input name="execution" value="(.*?)"/><input name="_eventId" value="submit"/></div>'''
    myComp = re.compile(pattern)
    execution = myComp.findall(text)[0]
    myLogger.info('execution={}'.format(execution))
    global username
    global password
    submit = '登录'
    _eventId = 'submit'

    myParams = {
        
        'username':username,
        'password':password,
        'submit':submit,
        'type':'username_password',
        'execution':execution,
        '_eventId':_eventId
    }


    loginUrl = 'https://cas.bjut.edu.cn/login'
    res7 = casSession.post(loginUrl, data = myParams, allow_redirects = False, verify = False)

    # https://itsapp.bjut.edu.cn/a_bjut/api/sso/index?redirect=https%3A%2F%2Fitsapp.bjut.edu.cn%2Fuc%2Fapi%2Foauth%2Findex%3Fredirect%3Dhttp%3A%2F%2Fyqfk.bjut.edu.cn%2Fapi%2Flogin%2Fpages-index-index%3Flogin%3D1%26appid%3D200220501233430304%26state%3DSTATE&from=wap&ticket=ST-212376-PSiNendCM0fJK2-Y2fRIZbaftGobc8e4494d89c
    url7 = res7.headers['Location']
    res8 = itsappSession.get(url7, allow_redirects = False, verify = False)

    # https://itsapp.bjut.edu.cn/a_bjut/api/sso/index?redirect=https%3A%2F%2Fitsapp.bjut.edu.cn%2Fuc%2Fapi%2Foauth%2Findex%3Fredirect%3Dhttp%3A%2F%2Fyqfk.bjut.edu.cn%2Fapi%2Flogin%2Fpages-index-index%3Flogin%3D1%26appid%3D200220501233430304%26state%3DSTATE&from=wap
    url8 = res8.headers['Location']
    res9 = itsappSession.get(url8, allow_redirects = False, verify = False)

    # https://itsapp.bjut.edu.cn/uc/api/oauth/index?redirect=http://yqfk.bjut.edu.cn/api/login/pages-index-index?login=1&appid=200220501233430304&state=STATE
    url9 = res9.headers['Location']
    res10 = itsappSession.get(url9,  allow_redirects = False, verify = False)

    # https://yqfk.bjut.edu.cn/api/login/pages-index-index?login=1&code=bd1e2d1d4cfaad348677d454e165b9d5&state=STATE
    url10 = res10.headers['Location']
    pattern3 = '&code=(.*?)&state'
    myComp3 = re.compile(pattern3)
    code = myComp3.findall(url10)[0]
    myLogger.info('code={}'.format(code))
    res11 = yqfkSession.get(url10, verify = False)

    url11 = 'https://yqfk.bjut.edu.cn/api/code?code='+code
    res12 = yqfkSession.get(url11)
    # print(res12.text)

    print(res12.json()['token'])

    newToken = res12.json()['token']
    myLogger.info('token={}'.format(newToken))

    myDic = dict()
    myDic['username'] = username
    myDic['password'] = password
    myDic['token'] = newToken
    myDic['cookie'] = yqfkSession.headers['Cookie']
    writeDate('./tmp.info', myDic)
    myLogger.info('保存基本信息成功')

    info = postDailyForm('', '', False)
    return info

if __name__ == '__main__':
    init()

    info = postDailyForm(cookie, token, True)
    # {'code': 40001, 'data': [], 'message': '今日已经填写', 'success': '', 'error': True}
    # {'code': 40001, 'data': [], 'message': '请填写相关内容', 'success': '', 'error': True}
    # 
    if info != -1:
        print(info)
    else:
        loginAndPostDailyForm()


