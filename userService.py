import pymysql
import time
import random

db_config = {
    'host': '8.136.233.221',
    'user': 'root',
    'password': 'hackeryoumotherboom',
    'db': 'user_test_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}



#新增用户
def add_user(name, gender):
    connection = pymysql.connect(**db_config)
    simple_snowflake = SimpleSnowflake()
    generated_id = simple_snowflake.generate_id()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO user_table (id, name, gender) VALUES (%s, %s, %s)"
            cursor.execute(sql, (generated_id, name, gender))
            connection.commit()
    finally:
        connection.close()


#删除用户
def delete_user(user_id):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM user_table WHERE id = %s"
            cursor.execute(sql, (user_id,))
            connection.commit()
    finally:
        connection.close()


#修改用户
def update_user(user_id, name, gender):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE user_table SET name = %s, gender = %s WHERE id = %s"
            cursor.execute(sql, (name, gender, user_id))
            connection.commit()
    finally:
        connection.close()


#获取用户列表
def get_user_data():
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM user_table"
            cursor.execute(sql)
            result = cursor.fetchall()
            user_list = list(result)
            return user_list
    finally:
        connection.close()

#分页查询
def get_paginated_user_data(page, per_page):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # Calculate the OFFSET based on the page and per_page
            offset = (page - 1) * per_page

            # SQL query to select paginated records from the user_table
            sql = f"SELECT * FROM user_table LIMIT {per_page} OFFSET {offset}"

            cursor.execute(sql)
            result = cursor.fetchall()
            user_list = list(result)
            return user_list
    finally:
        connection.close()




#生成ID
class SimpleSnowflake:
    def __init__(self):
        self.sequence = 0
        self.last_timestamp = -1

    def _current_timestamp(self):
        return int(time.time() * 1000)

    def generate_id(self):
        timestamp = self._current_timestamp()

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 0xFFF
            if self.sequence == 0:
                # 如果在同一毫秒内计数器溢出，则等待下一毫秒
                timestamp = self._wait_for_next_millisecond()
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        # 合并时间戳和计数器，生成 12 位的 ID
        snowflake_id = (timestamp << 12) | self.sequence

        return snowflake_id

    def _wait_for_next_millisecond(self):
        timestamp = self._current_timestamp()
        while timestamp <= self.last_timestamp:
            timestamp = self._current_timestamp()
        return timestamp