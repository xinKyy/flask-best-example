from flask import Flask, render_template, jsonify, request
from userService import add_user, get_user_data, delete_user, update_user, get_paginated_user_data
import pymysql


app = Flask(__name__)

db_config = {
    'host': '8.136.233.221',
    'user': 'root',
    'password': 'hackeryoumotherboom',
    'db': 'user_test_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


app = Flask(__name__)


def create_response(result, result_code=200, result_message="请求成功"):
    response = {
        "result": result,
        "resultCode": result_code,
        "resultMessage": result_message
    }
    return jsonify(response)


@app.route('/addUser', methods=['POST'])
def add_user():
    # data = request.form
    data = request.get_json()
    name = data.get('name')
    gender = data.get('gender')
    add_user(name, gender)
    response = create_response(True)
    return response


@app.route('/delUser', methods=['POST'])
def del_user():
    # data = request.form
    data = request.get_json()
    id = data.get('id')
    delete_user(id)
    response = create_response(True)
    return response

@app.route('/saveUser', methods=['POST'])
def save_user():
    data = request.get_json()
    id = data.get('id')
    name = data.get('name')
    gender = data.get('gender')
    update_user(id, name, gender)
    response = create_response(True)
    return response

@app.route("/getUserList")
def get_user_list():
    response = create_response(get_user_data())
    return response


@app.route('/getUsers', methods=['GET'])
def get_paginated_users():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    user_data = get_paginated_user_data(page, per_page)

    response = {
        'records': user_data,
        'current':page,
        'total':len(user_data),
    }

    return jsonify(response)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello'



if __name__ == '__main__':
    app.run()
