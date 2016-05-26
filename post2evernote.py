import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types

from evernote.api.client import EvernoteClient

client = EvernoteClient(token="S=s1:U=928b6:E=15c456b4c7e:C=154edba1d30:P=1cd:A=en-devtoken:V=2:H=f3533aa0ddd2cf91ac081d19ce0596ab",sandbox=True)
note_store = client.get_note_store()
notebooks = note_store.listhNotebooks()

note = Types.Note()
note.title = "에버노트 노트 생성 테스트"
note.content = '<?xml version="1.0" encoding="UTF-8"?>'
note.content += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
note.content += '<en-note>Here is the Evernote logo:<br/>'
note.content += '<en-media type="image/png" hash="' + hash_hex + '"/>'
note.content += '</en-note>'
created_note = note_store.createNote(note)

# 할일 : http://blog.embian.com/98를 참고하여 테스트중 테스트 완료 하기