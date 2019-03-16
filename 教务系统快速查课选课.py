import re
from selenium import webdriver
import requests

# 这里是需要你去输入的
stuId = '这里是账号，自己输入'
password = '这里是密码'
xkkz_id = '这里是xkkz_id，需要找到然后输入'
userData = {
    # 'kkbm_id_list[0]': 110,  # 开课学院，默认不要这一行
    # 'kclb_id_list[0]': '02',  # 课程类别，例如公共选修课，默认不要这一行
    # 'kcxzdm_list[0]': 21,  # 课程性质，默认不要这一行
    # 'jg_id_list[0]': '',  # 学院，默认不要这一行
    # 'jxms_list[0]': 2,  # 教学模式，默认不要这一行
    # 'kcgs_list[0]': 1,  # 课程归属，也就是人文啊之类的，默认不要这一行
    # 'sksj_list[0]': 5,  # 周几开课，默认不要这一行
    # 'skjc_list[0]': 8,  # 上课节数，默认不要这一行
    # 'cxbj_list[0]': 1,  # 是否重修，不要选这个
    'yl_list[0]': '1',  # 余量
    'rwlx': '2',
    'xkly': '0',
    'bklx_id': '0',
    'xh_id': stuId,  # 学号
    'xqh_id': '1',
    'jg_id': '201',  # 学院
    'zyh_id': '0409',  # 专业号id
    'zyfx_id': 'wfx',
    'njdm_id': '2016',
    'bh_id': '04091601',
    'xbm': '1',  # 性别名(不敢确定)
    'xslbdm': 'wlb',
    'ccdm': '3',  # 需要获取，暂时不知道是什么
    'xsbj': '4294967296',
    'sfkknj': '0',  # 暂定为是否开课年级
    'sfkkzy': '0',  # 暂定为是否开课专业
    'sfznkx': '0',  # 暂定为是否开课年级
    'zdkxms': '0',
    'sfkxq': '1',
    'sfkcfx': '0',
    'kkbk': '0',
    'kkbkdj': '0',
    'sfkgbcx': '0',
    'sfrxtgkcxd': '0',
    'tykczgxdcs': '0',  # 体育课操作更新的参数
    'xkxnm': '2018',  # 哪一年的就用那一年的咯
    'xkxqm': '12',
    'kklxdm': '10',
    'rlkz': '0',
    'kspage': '1',
    'jspage': '50',  # 每加10往后一页
    'jxbzb': ''
}

# 这下面就是代码区域了

driver = webdriver.Chrome()
session = requests.session()
headers = {
    'cookie': None,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
}
ClassListData = {}


def get_cookie():
    driver.get('http://10.0.10.184/jwglxt/xtgl/login_slogin.html')
    driver.find_element_by_id('yhm').send_keys(stuId)
    driver.find_element_by_id('mm').send_keys(password)
    driver.find_element_by_id('dl').click()
    cook = driver.get_cookies()
    for item in cook:
        cookie = item['name'] + '=' + item['value']
    return cookie


def get_http(cookie):
    url = 'http://10.0.10.184/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su=' + stuId
    http = session.get(url, headers=headers)
    return http.text


def getClassList(cookie):
    url = 'http://10.0.10.184/jwglxt/xsxk/zzxkyzb_cxZzxkYzbPartDisplay.html?gnmkdm=N253512&su=' + stuId
    global ClassListData
    # 这一段要获取的
    data = userData
    # 到这里结束
    ClassListData = data
    http = requests.post(url, headers=headers, data=data)
    return(http.text)


def printClassList(cookie):
    str = getClassList(cookie)
    kcrow = re.findall('kcrow":"([0-9]{1,2})', str)
    classNameId = re.findall('jxbmc":"(.+?)"', str)
    classId = re.findall('kch":"([0-9]+?)"', str)
    jxb_id = re.findall('jxb_id":"(.+?)"', str)
    xf = re.findall('xf":"(.+?)"', str)
    className = re.findall('kcmc":"(.+?)"', str)
    data = {
        'No.': kcrow,
        '课程：': classNameId,
        '课程名称：': className,
        '课程id：': classId,
        '教学班id：': jxb_id,
        '学分：': xf
    }
    i = 0
    while(i < len(data['No.'])):
        for key in data:
            print(key + data[key][i])
        print()
        i += 1
    return data


def getClassNo():
    try:
        n = eval(input('输入你要抢课的No号：'))
        return n
    except:
        print('不要输入空字符啊，会导致下一次输入出错，继续输入就是了')
        getClassNo()


def getClass1(list, cookie):
    try:
        jude = 'n'
        while (jude != 'y'):
            n = getClassNo()
            print()
            for key in list:
                print(key + list[key][n - 1])
            jude = input('\n即将抢这门课程,是否继续？(y/n)')
            if(jude == 'y'):
                getClass2(list, n, cookie)
            else:
                print('取消抢课')
    except:
        print('出错了,再来一次吧')
        getClass1(list, cookie)


def getClass2(list, n, cookie):
    url = 'http://10.0.10.184/jwglxt/xsxk/zzxkyzb_xkBcZyZzxkYzb.html?gnmkdm=N253512&su=' + stuId
    kcmc = '(' + list['课程id：'][n - 1] + ')' + \
        list['课程名称：'][n - 1] + ' - ' + list['学分：'][n - 1] + ' 学分'
    datas = {
        'jxb_ids': list['教学班id：'][n - 1],
        'kch_id': list['课程id：'][n - 1],
        'kcmc': kcmc,
        'rwlx': ClassListData['rwlx'],
        'rlkz': ClassListData['rwlx'],
        'rlzlkz': '1',
        'sxbj': '1',
        'xxkbj': '0',
        'qz': '0',
        'cxbj': '0',
        'xkkz_id': xkkz_id,
        'njdm_id': ClassListData['njdm_id'],  # 年级代码
        'zyh_id': ClassListData['zyh_id'],
        'kklxdm': ClassListData['kklxdm'],
        'xklc': '2',                        # 第几轮
        'xkxnm': ClassListData['xkxnm'],
        'xkxqm': ClassListData['xkxqm']
    }
    for key in datas:
        print('\'' + key + '\':\'' + datas[key] + '\',')
    requests.post(url, headers=headers, data=datas)


if __name__ == '__main__':
    cookie = get_cookie()
    headers['cookie'] = cookie
    get_http(cookie)
    list = printClassList(cookie)
    getClass1(list, cookie)
