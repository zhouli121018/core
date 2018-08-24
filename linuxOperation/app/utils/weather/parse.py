# -*- coding:utf-8 -*-
import json
from . import online
from django_redis import get_redis_connection
from urllib import quote

WEATHER_STAT_KEY = "linux-webvue:core:views:welcome:weather:stat"

def set_weather(city_pingying, subcity, delete=False):
    redis = get_redis_connection()
    subcity_quote = quote(subcity.encode("utf-8"))
    key = "linux-webvue:core:views:welcome:weather:{}".format(subcity_quote)
    if delete:
        redis.delete(key)
        return None
    d = online.get_weather(redis, city_pingying, subcity)
    if not d:
        return {"has_weather": False}
    j = json.dumps({
        "has_weather": True,
        "data": d
    })
    ( redis.pipeline()
      .set(key, j)
      .expire(key, 3600*12)
      .execute())
