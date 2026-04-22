"""
导入课程数据到 MySQL
"""
import pymysql
import re

# 读取 SQL 文件
with open('data/raw/edu.sql', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取 course_info 的 INSERT 语句
pattern = r"INSERT INTO\s+`course_info`\s+VALUES\s+([^;]+)"
matches = re.findall(pattern, content, re.IGNORECASE)

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    database='smart_edu',
    charset='utf8mb4'
)
cursor = conn.cursor()

# 清空表
cursor.execute('TRUNCATE TABLE course_info')
print("已清空 course_info 表")

# 解析并插入数据
count = 0
for match in matches:
    # 提取每个值组 (处理括号嵌套)
    # 找到所有以 ( 开头，) 结尾的组
    depth = 0
    start = -1
    rows = []
    for i, char in enumerate(match):
        if char == '(' and depth == 0:
            start = i
            depth = 1
        elif char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
            if depth == 0 and start != -1:
                rows.append(match[start+1:i])
                start = -1
    
    for row in rows:
        try:
            # 使用更安全的解析方式
            # 找到所有用单引号包围的字符串和其他值
            values = []
            i = 0
            while i < len(row):
                if row[i] == "'":
                    # 找到字符串结束
                    end = row.find("'", i+1)
                    if end == -1:
                        break
                    values.append(row[i+1:end])
                    i = end + 1
                    # 跳过逗号和空格
                    while i < len(row) and row[i] in ', ':
                        i += 1
                else:
                    # 找到下一个逗号
                    end = row.find(',', i)
                    if end == -1:
                        end = len(row)
                    val = row[i:end].strip()
                    if val:
                        values.append(val)
                    i = end + 1
            
            if len(values) >= 12:
                try:
                    cursor.execute('''
                        INSERT INTO course_info (id, course_name, course_introduce, subject_id, teacher, actual_price)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE course_name=VALUES(course_name)
                    ''', (
                        values[0],  # id
                        values[1],  # course_name
                        values[11] if len(values) > 11 else '',  # course_introduce
                        values[4],  # subject_id
                        values[5],  # teacher
                        values[8]   # actual_price
                    ))
                    count += 1
                    if count % 10 == 0:
                        print(f"已导入 {count} 条数据...")
                except Exception as e:
                    print(f"插入失败: {e}, 数据: {values[:3]}")
                    continue
        except Exception as e:
            continue

conn.commit()
cursor.execute('SELECT COUNT(*) FROM course_info')
result = cursor.fetchone()[0]
print(f"\n成功导入 {result} 条课程数据")

# 显示前5条
cursor.execute('SELECT id, course_name, teacher FROM course_info LIMIT 5')
print("\n前5个课程:")
for row in cursor.fetchall():
    print(f"  - ID:{row[0]} {row[1]} (讲师:{row[2]})")

conn.close()
print("\n完成！")
