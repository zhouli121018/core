# -*- coding:utf-8 -*-
import re
import requests
from . import C
import logging
import traceback
logger = logging.getLogger("django")

city_day_type = re.compile(ur'\<(.*?)dn="(.*?)"\>')
city_line_re = re.compile(ur"\<city(.*?)\/\>")
city_re = re.compile(ur'''cityname="(.*?)"(.*?)fontColor="(.*?)"(.*?)pyName="(.*?)"(.*?)state1="(.*?)"(.*?)state2="(.*?)"(.*?)stateDetailed="(.*?)"(.*?)tem1="(.*?)"(.*?)tem2="(.*?)"(.*?)temNow="(.*?)"(.*?)windState="(.*?)"(.*?)windDir="(.*?)"(.*?)windPower="(.*?)"(.*?)time="(.*?)"(.*?)url="(.*?)"''')
# <city cityX="289" cityY="107" cityname="塔城" centername="塔城" fontColor="FFFFFF" pyName="tacheng" state1="0" state2="0" stateDetailed="晴"
# tem1="34" tem2="18" temNow="21" windState="东风3-4级" windDir="东北风" windPower="1级" humidity="55%" time="09:00" url="101131101"/>

def get_weather_xml(city, timeout=3):
    url = "http://flash.weather.com.cn/wmaps/xml/{}.xml".format(city)
    r = requests.get(url, timeout=timeout)
    return r.text.encode(r.encoding).decode("utf-8")

def parse_xml(cityname, content):
    mt = city_day_type.search(content)
    if not mt:
        return None
    day_type = mt.group(2)
    if day_type=="day":
        L = C.DAY_WEATHER_STATE_LOCATION
    if day_type=="nay":
        L = C.NAY_WEATHER_STATE_LOCATION
    lst = city_line_re.findall(content)
    for item in lst:
        m = city_re.search(item)
        if m and m.group(1) == cityname:
            # ( cityname, fontColor, pyName, state1, state2, stateDetailed, tem1,
            #   tem2, temNow, windState, windDir, windPower, time, url ) = (
            #     m.group(1), m.group(3), m.group(5), m.group(7), m.group(9), m.group(11), m.group(13),
            #     m.group(15), m.group(17), m.group(19), m.group(21), m.group(23), m.group(25), m.group(27) )
            state1 = m.group(7)
            state2 = m.group(9)
            stateDetailed = m.group(11)
            imgLocation1, imgLocation2 = None, None
            if state1 in L:
                imgLocation1 = L[state1]
            if state2 in L:
                imgLocation2 = L[state2]
            return {
                "cityname": m.group(1), "fontColor":"#{}".format(m.group(3)), "pyName": m.group(5),
                "state1":state1, "state2": state2, "stateDetailed": stateDetailed,
                "imgLocation1": imgLocation1, "imgLocation2":imgLocation2,
                "temHigh": m.group(13), "temLow": m.group(15), "temNow": m.group(17),
                "windState": m.group(19), "windDir": m.group(21), "windPower": m.group(23),
                "time": m.group(25), "url": m.group(27) }
    return None

def get_weather(redis, city, cityname, timeout=3):
    try:
        key = "linux-webvue:core:views:welcome:weather:cahche:xml:{}".format(city)
        content = redis.get(key)
        if not content:
            content = get_weather_xml(city, timeout)
            (redis.pipeline()
             .set(key, content)
             .expire(key, 3600)
             .execute())
        return parse_xml(cityname, content)
    except BaseException as e:
        logger.log(logging.ERROR, traceback.format_exc())
        return None