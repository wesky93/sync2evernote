# -*- coding: utf-8 -*-#
from my_token import test_token, pro_token
import sys
import hashlib
import binascii
import evernote.edam.type.ttypes as Types
from os import listdir
from evernote.api.client import EvernoteClient


# 에버노트에 노트북 생성해주는 함수
def mk_notebook(nbooks, note_store):
    for nbook in nbooks:
        notebook = Types.Notebook()
        notebook.name = nbook
        cre_notebook = note_store.createNotebook(notebook)


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


'''
# 할일 : sync폴더에서 png파일만 추출
# 할일 : 이미지 파일명에서 파일명, 노트북, 작성날짜 추출하여 딕셔너리로 전달하는 함수 추가
# 할일 : 딕셔너리의 정보로 노트명, 업로드될 노트북 위치, 노트에 들어갈 내용으로 노트를 업로드 하는 함수 추가
# 할일 : 노트 생성 함수에서 에버노트에 원하는 노트북의 존재 여부를 확인하고 없을시 자동으로 생성해주는 함수 추가
# To create a new note, simply create a new Note object and fill in
# attributes such as the note's title.
note = Types.Note()
note.title = "sync파일 업로드 테스트"

# To include an attachment such as an image in a note, first create a Resource
# for the attachment. At a minimum, the Resource contains the binary attachment
# data, an MD5 hash of the binary data, and the attachment MIME type.
# It can also include attributes such as filename and location.

# 할일 : 이미지 속성값을 수집하고 리소스를 생성해주는 함수를 추가하여 가독성을 키우자
image = open('/Users/sinsky/Documents/Sync/2016-05-12_남원춘향제00003.png', 'rb').read()
md5 = hashlib.md5()
md5.update(image)
hash = md5.digest()

data = Types.Data()
data.size = len(image)
data.bodyHash = hash
data.body = image

resource = Types.Resource()
resource.mime = 'image/png'
resource.data = data

# Now, add the new Resource to the note's list of resources
note.resources = [resource]

# To display the Resource as part of the note's content, include an <en-media>
# tag in the note's ENML content. The en-media tag identifies the corresponding
# Resource using the MD5 hash.
hash_hex = binascii.hexlify(hash)

# The content of an Evernote note is represented using Evernote Markup Language
# (ENML). The full ENML specification can be found in the Evernote API Overview
# at http://dev.evernote.com/documentation/cloud/chapters/ENML.php
note.content = '<?xml version="1.0" encoding="UTF-8"?>'
note.content += '<!DOCTYPE en-note SYSTEM ' \
    '"http://xml.evernote.com/pub/enml2.dtd">'
note.content += '<en-note>Here is the Evernote logo:<br/>'
note.content += '<en-media type="image/png" hash="' + hash_hex + '"/>'
note.content += '</en-note>'

# Finally, send the new note to Evernote using the createNote method
# The new Note object that is returned will contain server-generated
# attributes such as the new note's unique GUID.
created_note = note_store.createNote(note)

print "Successfully created a new note with GUID: ", created_note.guid
'''
