#-*- coding: utf-8 -*-
import sys
from os.path import exists,basename,join
import shutil
import glob

# sync기기에 저장된 pdf를 작업폴더로 이동시키는 프로그램

def folder_check(path):
    result = exists(path)
    if result == False:
        print path,"가 없습니다."
        sys.exit()
    else:
        pass

def pdf_move(name):
    move_path = join(unlabelFD,basename(name))
    shutil.move(name,move_path)

# 2.7 한글 호환
reload(sys)
sys.setdefaultencoding('utf-8')

# 작업 폴더 변수
syncSD = "/Volumes/SYNCSD/SYNC/FILES/SAVED"
workFD = "/Users/sinsky/Desktop/sync 노트정리"
unlabelFD = join(workFD,"미분류 노트")
evernotFD = join(workFD,"에버노트")

# 작업 폴더 존재여부 확인
folder_check(syncSD)
folder_check(workFD)

# sync 노트를 작업폴더로 이동
pdf_list = glob.glob(syncSD+"/*")
for pdf in pdf_list:
    pdf_move(pdf)