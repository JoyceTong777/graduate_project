import bottle
from bottle import response, route, run, static_file, redirect, request, error, post
import audit
import json
import csv
from collections import OrderedDict

bottle.debug(True)

@route('/lib/:path#.+#')
def server_static(path):
    return static_file(path, root='../lib/')

@route('/components/:path#.+#')
def server_static(path):
    return static_file(path, root='../components/')

@route('/home/home.html')
def server_static():
    return static_file('home.html', root='../home/')

@route('/project/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='../project/')

@route('/<filepath:path>')
def server_static(filepath):
    raise static_file(filepath, root='../')


@route('/')
@route('/index.html')
def index():
    raise static_file('index.html', root='../')

@post('/requestTableList/')
def show_table_list():
	table_list = audit.get_table_list()
	return json.dumps(table_list)

@post('/requestTableData/')
def get_audit_result():
    json_data = request.json
    data = json.dumps(json_data)
    data_dict = json.loads(data)
    table_name = data_dict["name"]

    audit_result = audit.get_audit_result(table_name)
    audit_result_object = audit_result.get_table_object()

    return json.dumps(audit_result_object)

@post('/upload')
def upload_file():
    file = request.files['file']
    print("Upload a new table: " + file.filename)
    file.save('./dataset/');

@post('/changeTableData/')
def change_table_data():
    json_data = request.json
    data = json.dumps(json_data)
    data_dict = json.loads(data)

    table_name = data_dict['name']
    print table_name
    table_data = data_dict['data']

    file_path = "./dataset/" + table_name
    with open(file_path, 'wb') as csv_file:
        wtr = csv.writer(csv_file)
        wtr.writerows(table_data)

# start application
run(port=8080)