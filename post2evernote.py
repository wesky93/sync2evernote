# -*- coding: utf-8 -*-#
from my_token import test_token, pro_token
import sys
import hashlib
import glob
import binascii
import evernote.edam.type.ttypes as Types
from os import listdir, path, remove
from evernote.api.client import EvernoteClient


# --- 노트북 조회 및 확인 ---
# 에버노트에 노트북 생성해주는 함수
def mk_notebook(nbooks, note_store):
    for nbook in nbooks:
        notebook = Types.Notebook()
        notebook.name = nbook
        note_store.createNotebook(notebook)


# 에버노트의 노트북명과 guid로 딕셔너리를 만들어주는 함수
def bookguid(note_store):
    book_guid = {}
    notebooks = note_store.listNotebooks()
    for notebook in notebooks:
        book_guid[notebook.name] = notebook.guid
    return book_guid


# 노트북 조회후 에버노트에 없는 노트북은 생성하여 노트북을 키값으로 하는 딕셔너리 반환
def match_notebooks(work_path, note_store):
    notebooks = bookguid(note_store)  # 에버노트 노트북:guid 딕셔너리
    folder_list = listdir(work_path)  # 로컬 노트북(폴더) 리스트
    nmatch_books = []  # 에버노트에 존재하지 않는 노트북 리스트

    for nbook in folder_list:  # 매칭되는 노트북 조회
        if nbook in notebooks:
            pass
        else:
            nmatch_books.append(nbook)  # 에버노트에 없는 노트북은 리스트에 추가
    mk_notebook(nmatch_books, note_store)
    return bookguid(note_store)


# --- 노트 생성,업로드 및 파일 삭제 ---
# 파일을 받아 에버노트에 올릴 리소스 객체 생성
def mk_resource(png):
    with open(png, "rb") as image:
        png = image.read()
        md5 = hashlib.md5()
        md5.update(png)
        hash = md5.digest()
        hash_hex = binascii.hexlify(hash)

        data = Types.Data()
        data.size = len(png)
        data.bodyHash = hash
        data.body = png

        resource = Types.Resource()
        resource.mime = 'image/png'
        resource.data = data
        return resource, hash_hex


def file_info(png):
    """
	파일에서 생성 날짜와 파일명을 추출해준다.
	:param png: 파일 절대경로
	:return: 제목,생성날짜(추가예정)
	"""
    file = path.basename(png)
    name = path.splitext(file)[0]
    return name


# 노트를 생성하여 에버노트에 업로드
def post_note(note_store, png, book_guid):
    """
    노트객체를 생성하여 에버노트에 업로드
    :param note_store:
    :param png: 업로드할 sync필기 이미지
    :param book_guid: 노트가 속할 노트북의 guid
    :return:
    """
    resource, hash = mk_resource(png)
    note = Types.Note()
    note.title = file_info(png)
    note.resources = [resource]
    note.notebookGuid = book_guid
    note.content = '<?xml version="1.0" encoding="UTF-8"?>'
    note.content += '<!DOCTYPE en-note SYSTEM ' \
                    '"http://xml.evernote.com/pub/enml2.dtd">'
    note.content += '<en-note>sync에서 작성한 노트입니다.<br/>'
    note.content += '<en-media type="image/png" hash="' + hash + '"/>'
    note.content += '</en-note>'
    note_store.createNote(note)


# 한글 문제 해결용 코드
reload(sys)
sys.setdefaultencoding('utf-8')

# 토큰키 보안을 위하여 git에 등록하지 않은 파일에 토큰정보 저장
# sandbox token 이용시 test_token()
# 프로덕션 token 이용시 pro_token()
auth_token = test_token()
work_path = '/Users/sinsky/Desktop/sync 노트정리/에버노트'

if auth_token == test_token():
    client = EvernoteClient(token=auth_token, sandbox=True)
elif auth_token == pro_token():
    client = EvernoteClient(token=auth_token, sandbox=False)

note_store = client.get_note_store()

# 폴더명과 노트북명을 비교하여 존재유무 확인 및 생성
notebooks = match_notebooks(work_path, note_store)

# 폴더를 순회하며 노트 생성
for notebook in listdir(work_path):
    book_path = path.join(work_path, notebook)
    if path.isdir(book_path):  # 디렉토리 인지 확인
        book_guid = notebooks[notebook]  # 노트북의 guid값
        file_list = glob.glob("%s/*.png" % (book_path))
        for png in file_list:
            post_note(note_store, png, book_guid)
            remove(png)

print "sync노트를 성공적으로 에버노트에 업로드 하였습니다."