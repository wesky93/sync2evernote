# -*- coding: utf-8 -*-

import sys
import os
import datetime
import glob
from wand.image import Image


# 할일 : 폴더 내의 폴더(노트북 폴더)의 파일도 정상적으로 변경이 되는지 확인 필요

def ctime_prefix(name):
    """
    파일 생성 시간을 취득하여 prefix를 생성해주는 함수
    :param path: 파일 절대경로
    :return: 파일 생성시간 prefix (str)
    """
    ctime = os.path.getmtime(name)
    ctime = str(ctime) + "_"
    return ctime


def pdf2png(rename):
    """
    pdf를 png로 변환
    :param pdf: pdf파일의 절대 경로
    :return: 변환된 png파일명
    """
    with Image(filename=rename, resolution=600) as pdf:
        pngname = rename[:-3] + "png"
        pdf.format = "png"
        pdf.save(filename=pngname)
        return pngname


def convert_pdf(pdflist):
    '''
	각 폴더의 파일 리스트를 넘겨받아 pdf의 이름과 확장자를 변경
	'''
    ea = len(pdflist)
    count = 0
    for pdf in pdflist:
        # prefix추가된 파일명
        rename = os.path.join(os.path.dirname(pdf), ctime_prefix(pdf) + os.path.basename(pdf))
        os.rename(pdf, rename)  # prefix추가된 파일명으로 변환
        pngname = pdf2png(rename)  # pdf를 png로 변환
        count += 1
        print rename, "을 ", pngname, "으로 변환했습니다."
        os.remove(rename)  # pdf 삭제
        print rename, "을 삭제하였습니다"
        print ea, "개중 ", count, "개가 완료되었습니다"


# 2.7한글 호환
reload(sys)
sys.setdefaultencoding('utf-8')

# 분류된 파일이 위치한 절대경로
work_dir = "/Users/sinsky/Documents/Sync"
os.chdir(work_dir)

nbook_list = os.listdir(work_dir)

# 각 폴더(노트북)의 pdf파일 이름과 확장자 변경
for notebook in nbook_list:
    notebook = os.path.join(work_dir, notebook)
    pdflist = glob.glob("%s/*.pdf" % (notebook))  # 각 폴더의 pdf파일 추출
    convert_pdf(pdflist)

print "파일 변환이 완료되었습니다. 에버노트로 업로드를 시작합니다"
import post2evernote
