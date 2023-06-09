import pymssql


class Database:
    def __init__(self, server, user, password, database):
        """
        初始化DataBase实例
        :param server: 服务器
        :param user: 用户名
        :param password: 密码
        :param database: 数据库名称
        """
        self.server = server
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None
        self.database_name = 'UserSettings'
        self.query_all_sql = 'SELECT * FROM ' + self.database_name
        self.query_id_sql = 'SELECT Id FROM ' + self.database_name + ' WHERE UserName = %s'
        self.delete_sql = 'DELETE FROM ' + self.database_name + ' WHERE Id = %s'
        self.update_sql = 'UPDATE ' + self.database_name + ' SET R = %s, G = %s, B = %s, brightness = %s, current_index = %s, cold_warm_value = %s WHERE Id = %s'
        self.insert_sql = 'INSERT INTO ' + self.database_name + ' (UserName, R, G, B, brightness, Id, current_index, cold_warm_value) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

    def connect(self):
        """
        连接数据库
        :return:
        """
        # 建立数据库连接
        self.conn = pymssql.connect(server=self.server, user=self.user, password=self.password, database=self.database,
                                    charset='utf8')
        # 获取游标
        self.cursor = self.conn.cursor()

    def query_user_id(self, UserName):
        """
        查询用户名的用户id
        :param UserName: 用户名
        :return: 用户id
        """
        self.cursor.execute(self.query_id_sql, UserName)
        return self.cursor.fetchall()

    def query_all_user(self, params=None):
        """
        查询数据库
        :param params: 可选参数
        :return: 结果集
        """
        self.cursor.execute(self.query_all_sql, params)
        return self.cursor.fetchall()

    def query(self, sql, params=None):
        """
        查询数据库
        :param sql:查询语句
        :param params: 可选参数
        :return: 结果集
        """
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def delete(self, user_id):
        """
        删除数据
        :param user_id: 用户id
        """
        self.cursor.execute(self.delete_sql, user_id)
        self.conn.commit()

    def update(self, R, G, B, brightness, current_index, cold_warm_value, user_id):
        """
        更新数据
        :param cold_warm_value: 冷暖色调值
        :param current_index: 选色模式
        :param brightness: 亮度等级
        :param R: 数据值
        :param G: 数据值
        :param B: 数据值
        :param user_id: 用户id
        """
        self.cursor.execute(self.update_sql, (R, G, B, brightness, current_index, cold_warm_value, user_id))
        self.conn.commit()

    def insert(self, name, R, G, B, brightness, Id, current_index, cold_warm_value):
        """
        插入数据
        :param cold_warm_value: 冷暖色调值
        :param current_index: 选色模式
        :param Id: 用户Id
        :param brightness: 亮度等级
        :param name: 数据名称
        :param R: 数据值
        :param G: 数据值
        :param B: 数据值
        """
        encoded_sql = self.insert_sql.encode('cp936')
        self.cursor.execute(encoded_sql, (name, R, G, B, brightness, Id, current_index, cold_warm_value))
        self.conn.commit()

    def close(self):
        """
        关闭数据库连接
        """
        self.cursor.close()
        self.conn.close()
