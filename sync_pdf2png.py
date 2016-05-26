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


sync = "/Users/sinsky/Documents/Sync"  # sync의 파일이 자동 동기화 되는 폴더 절대 경로

pdflist = glob.glob("%s/*.pdf" % (sync))  # snyc의 폴더에서 pdf파일만 추출

for pdf in pdflist:
    rename = "{syncfolder}{prefix}{filename}".format(syncfolder=sync, prefix=ctime_prefix(pdf),
                                                     filename=pdf[len(sync) + 1:])
    os.rename(pdf, rename)

    # 할일 : 파일 변환을 함수로 변환# 할일 : 파일 변환을 함수로 변환
    # pdf를 png로 변환
    with Image(filename=rename, resolution=600) as pdf:
        pngname = rename[:-3] + "png"
        pdf.format = "png"
        pdf.save(filename=pngname)
        # 수정 : 파일 변환후 이전 파일이 삭제되게 수정

    os.remove(rename)