# -*- coding:utf-8 -*-

# 省配置
CHINA_CITY_E2C= {
    'heilongjiang': u'黑龙江',
    'jilin': u'吉林',
    'liaoning': u'辽宁',
    'hainan': u'海南',
    'neimenggu': u'内蒙古',
    'xinjiang': u'新疆',
    'xizang': u'西藏',
    'qinghai': u'青海',
    'ningxia': u'宁夏',
    'gansu': u'甘肃',
    'hebei': u'河北',
    'henan': u'河南',
    'hubei': u'湖北',
    'hunan': u'湖南',
    'shandong': u'山东',
    'jiangsu': u'江苏',
    'anhui': u'安徽',
    'shanxi': u'山西',
    'sanxi': u'陕西',
    'sichuan': u'四川',
    'yunnan': u'云南',
    'guizhou': u'贵州',
    'zhejiang': u'浙江',
    'fujian': u'福建',
    'jiangxi': u'江西',
    'guangdong': u'广东',
    'guangxi': u'广西',
    'beijing': u'北京',
    'tianjin': u'天津',
    'shanghai': u'上海',
    'chongqing': u'重庆',
    'xianggang': u'香港',
    'aomen': u'澳门',
    'taiwan': u'台湾',
    'xisha': u'西沙',
    'nanshadao': u'南沙',
    'diaoyudao': u'钓鱼岛',
}

CHINA_CITY_C2E= {
    u'黑龙江': u'heilongjiang',
    u'吉林': u'jilin',
    u'辽宁': u'liaoning',
    u'海南': u'hainan',
    u'内蒙古': u'neimenggu',
    u'新疆': u'xinjiang',
    u'西藏': u'xizang',
    u'青海': u'qinghai',
    u'宁夏': u'ningxia',
    u'甘肃': u'gansu',
    u'河北': u'hebei',
    u'河南': u'henan',
    u'湖北': u'hubei',
    u'湖南': u'hunan',
    u'山东': u'shandong',
    u'江苏': u'jiangsu',
    u'安徽': u'anhui',
    u'山西': u'shanxi',
    u'陕西': u'sanxi',
    u'四川': u'sichuan',
    u'云南': u'yunnan',
    u'贵州': u'guizhou',
    u'浙江': u'zhejiang',
    u'福建': u'fujian',
    u'江西': u'jiangxi',
    u'广东': u'guangdong',
    u'广西': u'guangxi',
    u'北京': u'beijing',
    u'天津': u'tianjin',
    u'上海': u'shanghai',
    u'重庆': u'chongqing',
    u'香港': u'xianggang',
    u'澳门': u'aomen',
    u'台湾': u'taiwan',
    u'西沙': u'xisha',
    u'南沙': u'nanshadao',
    u'钓鱼岛': u'diaoyudao',
}

CHINA_CITY_C2E_CAPITAL = {
    u'黑龙江':u'哈尔滨',
    u'吉林':u'长春',
    u'辽宁':u'沈阳',
    u'海南':u'海口',
    u'内蒙古':u'呼和浩特',
    u'新疆':u'乌鲁木齐',
    u'西藏':u'拉萨',
    u'青海':u'西宁',
    u'宁夏':u'银川',
    u'甘肃':u'兰州',
    u'河北':u'石家庄',
    u'河南':u'郑州',
    u'湖北':u'武汉',
    u'湖南':u'长沙',
    u'山东':u'济南',
    u'江苏':u'南京',
    u'安徽':u'合肥',
    u'山西':u'太原',
    u'陕西':u'西安',
    u'四川':u'成都',
    u'云南':u'昆明',
    u'贵州':u'贵阳',
    u'浙江':u'杭州',
    u'福建':u'福州',
    u'江西':u'南昌',
    u'广东':u'广州',
    u'广西':u'南宁',
    u'北京':u'北京',
    u'天津':u'天津',
    u'上海':u'上海',
    u'重庆':u'重庆',
    u'香港':u'香港',
    u'澳门':u'澳门',
    u'台湾':u'台北',
    u'西沙':u'西沙',
    u'南沙':u'南沙',
    u'钓鱼岛':u'钓鱼岛',
}

CHINA_CITY_EN = ('heilongjiang', 'jilin', 'liaoning', 'hainan', 'neimenggu', 'xinjiang', 'xizang', 'qinghai', 'ningxia', 'gansu', 'hebei', 'henan', 'hubei', 'hunan', 'shandong', 'jiangsu', 'anhui', 'shanxi', 'sanxi', 'sichuan', 'yunnan', 'guizhou', 'zhejiang', 'fujian', 'jiangxi', 'guangdong', 'guangxi', 'beijing', 'tianjin', 'shanghai', 'chongqing', 'xianggang', 'aomen', 'taiwan', 'xisha', 'nanshadao', 'diaoyudao')
CHINA_CITY_ZH = (u'黑龙江', u'吉林', u'辽宁', u'海南', u'内蒙古', u'新疆', u'西藏', u'青海', u'宁夏', u'甘肃', u'河北', u'河南', u'湖北', u'湖南', u'山东', u'江苏', u'安徽', u'山西', u'陕西', u'四川', u'云南', u'贵州', u'浙江', u'福建', u'江西', u'广东', u'广西', u'北京', u'天津', u'上海', u'重庆', u'香港', u'澳门', u'台湾', u'西沙', u'南沙', u'钓鱼岛',)


# http://www.weather.com.cn/pub/legend.shtml
DAY_WEATHER_STATE_LOCATION = {
    u"0": u"-0px -0px", # 晴
    u"1": u"-80px -0px", # 多云
    u"2": u"-160px -0px",# 阴
    u"3": u"-240px -0px",# 阵雨
    u"4": u"-320px -0px", # 雷阵雨
    u"5": u"-400px -0px", # 雷阵雨伴有冰雹
    u"6": u"-480px -0px", # 雨夹雪
    u"7": u"-560px -0px",  # 小雨
    u"8": u"-640px -0px", # 中雨

    u"9": u"-0px -80px", # 大雨
    u"10": u"-80px -80px", # 暴雨
    u"11": u"-160px -80px", # 大暴雨
    u"12": u"-240px -80px", # 特大暴雨
    u"13": u"-320px -80px", # 阵雪
    u"14": u"-400px -80px", # 小雪
    u"15": u"-480px -80px", # 中雪
    u"16": u"-560px -80px", # 大雪
    u"17": u"-640px -80px", # 暴雪


    u"18": u"-0px -160px", # 雾
    u"19": u"-80px -160px", # 冻雨
    u"20": u"-160px -160px", # 沙尘暴
    u"21": u"-240px -160px", # 小到中雨
    u"22": u"-320px -160px", # 中到大雨
    u"23": u"-400px -160px", # 大到暴雨
    u"24": u"-480px -160px", # 暴雨到大暴雨
    u"25": u"-560px -160px", # 大暴雨到特大暴雨
    u"26": u"-640px -160px", # 小到中雪

    u"27": u"-0px -240px", # 中到大雪
    u"28": u"-80px -240px", # 大到暴雪
    u"29": u"-160px -240px", # 浮尘
    u"30": u"-240px -240px", # 扬沙
    u"31": u"-320px -240px", # 强沙尘暴
    u"32": u"-400px -240px", # 雨
    u"33": u"-480px -240px", # 雪
    u"53": u"-560px -240px", # 霾
}


NAY_WEATHER_STATE_LOCATION = {
    u"0": u"-0px -320px", # 晴
    u"1": u"-80px -320px", # 多云
    u"2": u"-160px -320px",# 阴
    u"3": u"-240px -320px",# 阵雨
    u"4": u"-320px -320px", # 雷阵雨
    u"5": u"-400px -320px", # 雷阵雨伴有冰雹
    u"6": u"-480px -320px", # 雨夹雪
    u"7": u"-560px -320px",  # 小雨
    u"8": u"-640px -320px", # 中雨

    u"9": u"-0px -400px", # 大雨
    u"10": u"-80px -400px", # 暴雨
    u"11": u"-160px -400px", # 大暴雨
    u"12": u"-240px -400px", # 特大暴雨
    u"13": u"-320px -400px", # 阵雪
    u"14": u"-400px -400px", # 小雪
    u"15": u"-480px -400px", # 中雪
    u"16": u"-560px -400px", # 大雪
    u"17": u"-640px -400px", # 暴雪


    u"18": u"-0px -480px", # 雾
    u"19": u"-80px -480px", # 冻雨
    u"20": u"-160px -480px", # 沙尘暴
    u"21": u"-240px -480px", # 小到中雨
    u"22": u"-320px -480px", # 中到大雨
    u"23": u"-400px -480px", # 大到暴雨
    u"24": u"-480px -480px", # 暴雨到大暴雨
    u"25": u"-560px -480px", # 大暴雨到特大暴雨
    u"26": u"-640px -480px", # 小到中雪

    u"27": u"-0px -560px", # 中到大雪
    u"28": u"-80px -560px", # 大到暴雪
    u"29": u"-160px -560px", # 浮尘
    u"30": u"-240px -560px", # 扬沙
    u"31": u"-320px -560px", # 强沙尘暴
    u"32": u"-400px -560px", # 雨
    u"33": u"-480px -560px", # 雪
    u"53": u"-560px -560px", # 霾
}

"""
url = "http://flash.weather.com.cn/wmaps/xml/china.xml"
r = requests.get(url)
c = r.text.encode(r.encoding)
print c

<china dn="day">
<city quName="黑龙江" pyName="heilongjiang" cityname="哈尔滨" state1="4" state2="1" stateDetailed="雷阵雨转多云" tem1="27" tem2="17" windState="西北风转东南风微风级"/>
<city quName="吉林" pyName="jilin" cityname="长春" state1="0" state2="1" stateDetailed="晴转多云" tem1="29" tem2="17" windState="西北风转南风微风级"/>
<city quName="辽宁" pyName="liaoning" cityname="沈阳" state1="0" state2="0" stateDetailed="晴" tem1="34" tem2="20" windState="东北风微风级"/>
<city quName="海南" pyName="hainan" cityname="海口" state1="11" state2="10" stateDetailed="大暴雨转暴雨" tem1="29" tem2="26" windState="西北风5-6级转西南风4-5级"/>
<city quName="内蒙古" pyName="neimenggu" cityname="呼和浩特" state1="7" state2="9" stateDetailed="小雨转大雨" tem1="28" tem2="18" windState="南风3-4级"/>
<city quName="新疆" pyName="xinjiang" cityname="乌鲁木齐" state1="0" state2="0" stateDetailed="晴" tem1="33" tem2="24" windState="微风"/>
<city quName="西藏" pyName="xizang" cityname="拉萨" state1="7" state2="7" stateDetailed="小雨" tem1="21" tem2="11" windState="微风"/>
<city quName="青海" pyName="qinghai" cityname="西宁" state1="1" state2="0" stateDetailed="多云转晴" tem1="28" tem2="13" windState="东风转西北风微风级"/>
<city quName="宁夏" pyName="ningxia" cityname="银川" state1="4" state2="1" stateDetailed="雷阵雨转多云" tem1="24" tem2="20" windState="微风"/>
<city quName="甘肃" pyName="gansu" cityname="兰州" state1="3" state2="1" stateDetailed="阵雨转多云" tem1="31" tem2="19" windState="微风"/>
<city quName="河北" pyName="hebei" cityname="石家庄" state1="4" state2="4" stateDetailed="雷阵雨" tem1="33" tem2="25" windState="东北风转北风微风级"/>
<city quName="河南" pyName="henan" cityname="郑州" state1="1" state2="1" stateDetailed="多云" tem1="35" tem2="27" windState="东北风微风级"/>
<city quName="湖北" pyName="hubei" cityname="武汉" state1="1" state2="1" stateDetailed="多云" tem1="38" tem2="28" windState="东风微风级"/>
<city quName="湖南" pyName="hunan" cityname="长沙" state1="1" state2="1" stateDetailed="多云" tem1="37" tem2="29" windState="北风转东北风微风级"/>
<city quName="山东" pyName="shandong" cityname="济南" state1="1" state2="1" stateDetailed="多云" tem1="35" tem2="27" windState="东北风转东南风微风级"/>
<city quName="江苏" pyName="jiangsu" cityname="南京" state1="1" state2="1" stateDetailed="多云" tem1="36" tem2="27" windState="东风3-4级"/>
<city quName="安徽" pyName="anhui" cityname="合肥" state1="1" state2="1" stateDetailed="多云" tem1="37" tem2="27" windState="东风微风级"/>
<city quName="山西" pyName="shanxi" cityname="太原" state1="7" state2="7" stateDetailed="小雨" tem1="30" tem2="20" windState="东南风微风级"/>
<city quName="陕西" pyName="sanxi" cityname="西安" state1="3" state2="3" stateDetailed="阵雨" tem1="39" tem2="26" windState="东南风3-4级"/>
<city quName="四川" pyName="sichuan" cityname="成都" state1="3" state2="7" stateDetailed="阵雨转小雨" tem1="32" tem2="23" windState="微风"/>
<city quName="云南" pyName="yunnan" cityname="昆明" state1="3" state2="3" stateDetailed="阵雨" tem1="24" tem2="17" windState="微风"/>
<city quName="贵州" pyName="guizhou" cityname="贵阳" state1="3" state2="1" stateDetailed="阵雨转多云" tem1="28" tem2="19" windState="东北风微风级"/>
<city quName="浙江" pyName="zhejiang" cityname="杭州" state1="0" state2="0" stateDetailed="晴" tem1="36" tem2="27" windState="东风微风级"/>
<city quName="福建" pyName="fujian" cityname="福州" state1="1" state2="1" stateDetailed="多云" tem1="37" tem2="25" windState="微风"/>
<city quName="江西" pyName="jiangxi" cityname="南昌" state1="1" state2="1" stateDetailed="多云" tem1="37" tem2="29" windState="东北风转北风微风级"/>
<city quName="广东" pyName="guangdong" cityname="广州" state1="9" state2="4" stateDetailed="大雨转雷阵雨" tem1="33" tem2="26" windState="微风转东风微风级"/>
<city quName="广西" pyName="guangxi" cityname="南宁" state1="3" state2="3" stateDetailed="阵雨" tem1="35" tem2="26" windState="东北风微风级"/>
<city quName="北京" pyName="beijing" cityname="北京" state1="1" state2="4" stateDetailed="多云转雷阵雨" tem1="33" tem2="25" windState="南风转东南风微风级"/>
<city quName="天津" pyName="tianjin" cityname="天津" state1="1" state2="2" stateDetailed="多云转阴" tem1="34" tem2="28" windState="东南风微风级"/>
<city quName="上海" pyName="shanghai" cityname="上海" state1="0" state2="2" stateDetailed="晴转阴" tem1="36" tem2="28" windState="东风转东北风微风级"/>
<city quName="重庆" pyName="chongqing" cityname="重庆" state1="1" state2="7" stateDetailed="多云转小雨" tem1="35" tem2="26" windState="微风"/>
<city quName="香港" pyName="xianggang" cityname="香港" state1="10" state2="10" stateDetailed="暴雨" tem1="31" tem2="26" windState="东南风3-4级转4-5级"/>
<city quName="澳门" pyName="aomen" cityname="澳门" state1="10" state2="10" stateDetailed="暴雨" tem1="31" tem2="26" windState="东南风4-5级转5-6级"/>
<city quName="台湾" pyName="taiwan" cityname="台北" state1="0" state2="0" stateDetailed="晴" tem1="31" tem2="26" windState="北风转西风微风级"/>
<city quName="西沙" pyName="xisha" cityname="西沙" state1="4" state2="4" stateDetailed="雷阵雨" tem1="29" tem2="27" windState="西南风5-6级"/>
<city quName="南沙" pyName="nanshadao" cityname="南沙" state1="4" state2="4" stateDetailed="雷阵雨" tem1="29" tem2="26" windState="西南风4-5级"/>
<city quName="钓鱼岛" pyName="diaoyudao" cityname="钓鱼岛" state1="0" state2="0" stateDetailed="晴" tem1="33" tem2="28" windState="北风转西北风3-4级"/>
</china>
"""