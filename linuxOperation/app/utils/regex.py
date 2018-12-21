# -*- coding: utf-8 -*-
import re


def path_sub(url):
    if re.search(r'(\/\d+?\/)', url):
        url = re.sub(r'(\/\d+?\/)', '/modify/', url)
    return url

pure_digits_regex = lambda s: re.compile('^\d+$').match(s)
pure_english_regex = lambda s: re.compile('^[\.\_\-A-Za-z0-9_]+$').match(s)
pure_english_regex2 = lambda s: re.compile('^[A-Za-z_]+$').match(s)
pure_email_regex = lambda s: re.compile('^(\w|[-+=.])+@\w+([-.]\w+)*\.(\w+)$').match(s)
pure_ip_regex = lambda s: re.compile('^(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)$').match(s)
pure_ipaddr_regex = lambda s: re.compile('^(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\/(\d+)$').match(s)
pure_tel_regex = lambda s: re.compile('^1[3456789]\d{9}$').match(s)
pure_upper_regex = lambda s: re.compile('^[A-Z]+$').match(s)
pure_lower_regex = lambda s: re.compile('^[a-z]+$').match(s)

pure_upper_regex2 = lambda s: re.compile('[A-Z]+').search(s)
pure_lower_regex2 = lambda s: re.compile('[a-z]+').search(s)
pure_digits_regex2 = lambda s: re.compile('\d+').search(s)

if __name__ == "__main__":
    print pure_tel_regex("19829799823")
    print pure_tel_regex("19929799823")
