# 测试MySQL连接
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pymysql
import os
from config.config import MYSQL_CONFIG

try:
    # 尝试连接MySQL，使用密码123456，不指定数据库
    print("正在连接MySQL...")
    conn_config = MYSQL_CONFIG.copy()
    conn_config['password'] = '123456'  # 使用用户提供的密码
    conn_config.pop('database', None)  # 移除database参数
    conn = pymysql.connect(**conn_config)
    print("MySQL连接成功！")
    
    # 检查smart_edu数据库是否存在
    with conn.cursor() as cursor:
        cursor.execute("SHOW DATABASES LIKE 'smart_edu'")
        result = cursor.fetchone()
        if result:
            print("smart_edu数据库已存在")
        else:
            print("smart_edu数据库不存在，需要创建")
            # 创建数据库
            cursor.execute("CREATE DATABASE smart_edu CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("smart_edu数据库创建成功")
    
    # 导入SQL文件
    print("正在导入SQL文件...")
    sql_file_path = os.path.join(os.path.dirname(__file__), 'data', 'raw', 'edu.sql')
    if os.path.exists(sql_file_path):
        # 使用pymysql执行SQL文件
        print(f"正在读取SQL文件: {sql_file_path}")
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # 连接到smart_edu数据库
        conn_config = MYSQL_CONFIG.copy()
        conn_config['password'] = '123456'
        conn_config['database'] = 'smart_edu'
        with pymysql.connect(**conn_config) as conn:
            with conn.cursor() as cursor:
                # 执行SQL语句（按分号分割）
                sql_statements = sql_content.split(';')
                for stmt in sql_statements:
                    stmt = stmt.strip()
                    if stmt:
                        try:
                            cursor.execute(stmt)
                        except Exception as e:
                            print(f"执行SQL语句失败: {e}")
                            print(f"语句: {stmt[:100]}...")
                conn.commit()
        print("SQL文件导入成功！")
    else:
        print("SQL文件不存在，跳过导入")
    
    conn.close()
except Exception as e:
    print(f"MySQL连接失败: {e}")
