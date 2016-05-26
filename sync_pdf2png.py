import os
import datetime
import glob
from wand.image import Image


def ctime_prefix(name):
    """
    파일 생성 시간을 취득하여 prefix를 생성해주는 함수
    :param path: 파일 절대경로
    :return: 파일 생성시간 prefix (str)
    """
    ctime = os.path.getmtime(name)  # 파일 생성시간 취득
    ctime = "/" + str(datetime.datetime.fromtimestamp(ctime))[:10] + "_"
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

sync = "/Users/sinsky/Documents/Sync"  # sync의 파일이 자동 동기화 되는 폴더 절대 경로

pdflist = glob.glob("%s/*.pdf" % (sync))  # snyc의 폴더에서 pdf파일만 추출

for pdf in pdflist:
    # prefix추가된 파일명
    # 수정 : 하드코딩 대신 os.path.basename 과 os.path.dirname을 이용하기
    # 수정 : os.path.join사용하기
    rename = "{syncfolder}{prefix}{filename}".format(syncfolder=os.path.dirname(pdf), prefix=ctime_prefix(pdf),
                                                     filename=os.path.basename(pdf))
    os.rename(pdf, rename)      # prefix추가된 파일명으로 변환
    pngname = pdf2png(rename)   # pdf를 png로 변환
    print(rename, "을 ",pngname,"으로 변환했습니다.")
    os.remove(rename)           # pdf 삭제
    print(rename,"을 삭제하였습니다")