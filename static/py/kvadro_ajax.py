from browser import document as doc, ajax, html
import json


def send_ajax(data, url, method, on_complete):
    # print('send_ajax data:', data)
    req = ajax.ajax()
    req.bind('complete', on_complete)
    req.open(method.upper(), url, True)
    req.set_header('Content-type', 'application/json')
    req.send(json.dumps(data))


def get_text(ev):
    def on_complete(req):
        data = json.loads(req.text)
        # print('get_text.on_complete:', req.status, data)
        if data['code'] == 0:
            doc['error_field'].text = '%s: Успешно' % data['method']
            doc['error_field'].style = {'color': '#000000', }
            # Вывести строки
            rows_form = doc['rows_form']
            rows_form.clear()
            for r in data['result']:
                row = html.DIV(r['id'],
                               id='row_%s' % r['id'],
                               style={'border-bottom': 'solid 1px black'},
                               Class='text_row')
                row_id = html.INPUT(type='checkbox', name='delete_%s' % r['id'], style={'display': 'inline'})
                row_content = html.P(r['text'][:40], style={'display': 'inline'})
                row <= row_id
                row <= row_content
                rows_form <= row
        else:
            pass
            doc['error_field'].text = data['error']
            doc['error_field'].style = {'color': '#FF7777', }

    # print('get_text')
    send_ajax(data={}, url='/api/gettext/', method='get', on_complete=on_complete)


def delete_selected(ev):
    def on_complete(req):
        data = json.loads(req.text)
        # print('delete_selected.on_complete:', req.status, data)
        if data['code'] == 0:
            doc['error_field'].text = '%s: Успешно' % data['method']
            doc['error_field'].style = {'color': '#000000', }
            # Удалить элементы
            for r in data['deleted']:
                doc.getElementById('row_%s' % r).remove()
        else:
            # Вывести ошибку
            doc['error_field'].text = data['error']
            doc['error_field'].style = {'color': '#FF5555', }

    # print('delete_selected')
    delete_list = [int(elt.name.split('_')[1]) for elt in doc.get(selector='input[type="checkbox"]') if elt.checked]
    # print(delete_list)
    send_ajax(data={'delete': delete_list}, url='/api/deleterows/', method='delete', on_complete=on_complete)


def upload_text(ev):
    def on_complete(req):
        data = json.loads(req.text)
        # print('upload_text.on_complete:', req.status, data)
        if data['code'] == 0:
            doc['text_field'].value = ''
            doc['error_field'].text = '%s: Успешно' % data['method']
            doc['error_field'].style = {'color': '#000000', }
            rows_form = doc['rows_form']
            row = html.DIV(data['id'],
                           id='row_%s' % data['id'],
                           style={'border-bottom': 'solid 1px black'},
                           Class='text_row')
            row_id = html.INPUT(type='checkbox', name='delete_%s' % data['id'], style={'display': 'inline'})
            row_content = html.P(data['text'][:40], style={'display': 'inline'})
            row <= row_id
            row <= row_content
            rows_form <= row
        else:
            doc['error_field'].text = data['error']
            doc['error_field'].style = {'color': '#FF5555', }

    # print('upload_text')
    if doc['text_field'].value:
        send_ajax(data={'txt': doc['text_field'].value, }, url='/api/uploadtext/', method='post', on_complete=on_complete)
    else:
        doc['error_field'].text = 'post: Вы забыли ввести текст.'
        doc['error_field'].style = {'color': '#FF5555', }


# bindings
doc['get_text'].bind('click', get_text)
doc['delete_selected'].bind('click', delete_selected)
doc['upload_text'].bind('click', upload_text)
