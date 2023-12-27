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


def create_response(result, result_code=200, result_message="successfully"):
    response = {
        "result": result,
        "resultCode": result_code,
        "resultMessage": result_message
    }
    return jsonify(response)


@app.route('/add_user', methods=['POST'])
def add_user_route():
    # data = request.form
    data = request.get_json()
    name = data.get('name')
    gender = data.get('gender')
    add_user(name, gender)
    response = create_response(True)
    return response

@app.route('/edit_user', methods=['POST'])
def save_user():
    data = request.get_json()
    id = data.get('id')
    name = data.get('name')
    gender = data.get('gender')
    update_user(id, name, gender)
    response = create_response(True)
    return response


@app.route('/get_user_list', methods=['GET'])
def get_paginated_users():
    page = int(request.args.get('page_num', 1))
    page_size = int(request.args.get('page_size', 10))

    user_data, total_records = get_paginated_user_data(page, page_size)

    response_data = {
        'records': user_data,
        'current': page,
        'total': total_records,
    }
    res = create_response(response_data)
    return res


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello'



if __name__ == '__main__':
    app.run()
