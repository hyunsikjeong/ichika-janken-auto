#!/usr/bin/env python3

import hashlib
import json
import random
import re
import requests
import sys
import urllib.parse


DOMAIN = 'https://p.eagate.573.jp/'
LOGIN_URL = urllib.parse.urljoin(DOMAIN, 'gate/p/login.html')
LOGIN_AUTH_URL = urllib.parse.urljoin(DOMAIN, 'gate/p/common/login/api/login_auth.html')
LOGIN_RESRV_URL = urllib.parse.urljoin(DOMAIN, 'gate/p/login_complete.html')
CAPTCHA_URL = urllib.parse.urljoin(DOMAIN, 'gate/p/common/login/api/kcaptcha_generate.html')
JANKEN_URL = urllib.parse.urljoin(DOMAIN, 'game/bemani/bjm2020/janken/index.html')
CARD_URL = urllib.parse.urljoin(DOMAIN, 'game/bemani/wbr2020/01/card.html')
CARD_SUBMIT_URL = urllib.parse.urljoin(DOMAIN, 'game/bemani/wbr2020/01/card_save.html')


def get_picture_md5(url):
    with s.get(url, stream=True) as r:
        hasher = hashlib.md5()
        for d in r.iter_content(1024):
            hasher.update(d)
        return hasher.hexdigest()


def get_captcha_result(captcha_data):
    captcha_dict = json.load(open('captcha.json', 'r'))

    kcsess = captcha_data['kcsess']
    correct_md5 = get_picture_md5(captcha_data['correct_pic'])
    choice_md5 = captcha_dict[correct_md5]['choice_md5']

    keys = ['' for _ in range(5)]
    for choice in captcha_data['choicelist']:
        if not choice['attr']:
            continue

        idx = int(choice['attr'][1])
        md5_result = get_picture_md5(choice['img_url'])

        if md5_result in choice_md5:
            keys[idx] = choice['key']

    return f'k_{kcsess}_{keys[0]}_{keys[1]}_{keys[2]}_{keys[3]}_{keys[4]}'


def try_login(s):
    _ = s.get(LOGIN_URL)
    r = s.get(CAPTCHA_URL)

    captcha_data = json.loads(r.text)['data']
    captcha = get_captcha_result(captcha_data)

    file_name = sys.argv[1] if len(sys.argv) > 1 else 'logindata.json'
    login_data = json.load(open(file_name, 'r'))
    login_data = {
        **login_data,
        'otp': '',
        'resrv_url': LOGIN_RESRV_URL,
        'captcha': captcha
    }

    r = s.post(LOGIN_AUTH_URL, data=login_data, allow_redirects=False)
    login_result = json.loads(r.text)
    fail_code, href = login_result["fail_code"], login_result["href"]

    if fail_code != 0 or href != "https://p.eagate.573.jp/gate/p/login_complete.html":
        return False
    return True


def janken(s):
    r = s.get(JANKEN_URL)
    preg = re.compile(r'/game/bemani/bjm2020/janken/exe.html\?form_type=[0-2]&chara_id=[0-9]&token_val=[0-9a-f]{16,32}')
    janken_urls = list(map(lambda url: urllib.parse.urljoin(DOMAIN, url), preg.findall(r.text)))

    if janken_urls:
        choice = random.choice(janken_urls)
        _ = s.get(choice)
        print("[Janken] Done!")
        return True
    else:
        print("[Janken] Already done, or an error occured", file=sys.stderr)
        return False


def card(s):
    r = s.get(CARD_URL)
    preg = re.compile(r'<input id="id_initial_token" type="hidden" value="([0-9a-f]{20,32})">')
    tokens = list(preg.findall(r.text))

    if len(tokens) != 1:
        print("[Card] Too many tokens are found")
        return False

    card_data = {
        "c_type": 0,
        "c_id": str(random.randint(0, 2)),
        "t_id": tokens[0]
    }

    _ = s.post(CARD_SUBMIT_URL, data=card_data)
    print("[Card] Done!")
    return True


if __name__ == "__main__":
    # 1. Login
    s = requests.Session()

    while not try_login(s):
        pass

    # 2. Janken
    janken_result = janken(s)

    # 3. Card
    card_result = card(s)

    if janken_result and card_result:
        exit(0)
    else:
        exit(1)
