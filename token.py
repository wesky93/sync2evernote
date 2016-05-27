#-*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# 에버노트의 토큰을 저장한 파일로 git에 포함시키지 않아 토큰 유출을 방지

def test_token():
    token = "your evernote sandbox token"
    return token

def pro_token():
    token = "your evernote production token"
    return token