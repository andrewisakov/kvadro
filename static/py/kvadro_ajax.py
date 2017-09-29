from browser import document as doc, ajax
import json


def send_ajax(data, url, method, on_complete):
    print('send_ajax data:', data)
    req = ajax.ajax()
    req.bind('complete', on_complete)
    req.open(method.upper(), url, True)
    req.set_header('Content-type', 'application/json')
    req.send(json.dumps(data))


def get_text(ev):
    def on_complete(req):
        data = json.loads(req.text)
        print('get_text.on_complete:', req.status, data)
        if data['code'] == 0:
            doc['error_field'].style = {'display': 'hidden', }
            # Вывести строки
        else:
            pass
            doc['error_field'].text = data['error']
            doc['error_field'].style = {'display': 'visible', 'backgroind': '#FF7777', }

    print('get_text')
    send_ajax(data={}, url='/api/gettext/', method='get', on_complete=on_complete)


def delete_selected(ev):
    def on_complete(req):
        data = json.loads(req.text)
        print('delete_selected.on_complete:', req.status, data)
        if data['code'] == 0:
            doc['error_field'].style = {'display': 'hidden', }
            # Вывести оставшиеся строки
        else:
            # Вывести ошибку
            doc['error_field'].text = data['error']
            doc['error_field'].style = {'display': 'visible', 'backgroind': '#FF7777', }

    print('delete_selected')
    send_ajax(data={'delete': (1, 2, )}, url='/api/deleterows/', method='delete', on_complete=on_complete)


def upload_text(ev):
    def on_complete(req):
        data = json.loads(req.text)
        print('upload_text.on_complete:', req.status, data)
        if data['code'] == 0:
            doc['text_field'].value = ''
            doc['error_field'].style = {'display': 'hidden', }
        else:
            doc['error_field'].text = data['error']
            doc['error_field'].style = {'display': 'visible', 'backgroind': '#FF7777', }

    # print('upload_text')
    if doc['text_field'].value:
        send_ajax(data={'txt': doc['text_field'].value, }, url='/api/uploadtext/', method='post', on_complete=on_complete)


# bindings
doc['get_text'].bind('click', get_text)
doc['delete_selected'].bind('click', delete_selected)
doc['upload_text'].bind('click', upload_text)
