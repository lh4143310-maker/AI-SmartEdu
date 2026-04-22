"""
导入章节数据到 MySQL
"""
import pymysql
import re

# 读取 SQL 文件
with open('data/raw/edu.sql', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取 chapter_info 的 INSERT 语句 (处理多行格式)
pattern = r"insert into\s+`chapter_info`\s+values\s+(.+?)(?=;|/\*!)"
matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)

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
cursor.execute('TRUNCATE TABLE chapter_info')
print("已清空 chapter_info 表")

# 解析并插入数据
count = 0
for match in matches:
    # 提取每个值组
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
            # 简单解析值
            values = []
            i = 0
            while i < len(row):
                if row[i] == "'":
                    end = row.find("'", i+1)
                    if end == -1:
                        break
                    values.append(row[i+1:end])
                    i = end + 1
                    while i < len(row) and row[i] in ', ':
                        i += 1
                else:
                    end = row.find(',', i)
                    if end == -1:
                        end = len(row)
                    val = row[i:end].strip()
                    if val:
                        values.append(val)
                    i = end + 1
            
            if len(values) >= 5:
                try:
                    cursor.execute('''
                        INSERT INTO chapter_info (id, course_id, chapter_name, create_time)
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE chapter_name=VALUES(chapter_name)
                    ''', (
                        values[0],  # id
                        values[1],  # course_id
                        values[2],  # chapter_name
                        values[4] if len(values) > 4 else None  # create_time
                    ))
                    count += 1
                    if count % 100 == 0:
                        print(f"已导入 {count} 条数据...")
                except Exception as e:
                    continue
        except Exception as e:
            continue

conn.commit()
cursor.execute('SELECT COUNT(*) FROM chapter_info')
result = cursor.fetchone()[0]
print(f"\n成功导入 {result} 条章节数据")

# 显示前5条
cursor.execute('SELECT id, course_id, chapter_name FROM chapter_info LIMIT 5')
print("\n前5个章节:")
for row in cursor.fetchall():
    print(f"  - ID:{row[0]} 课程ID:{row[1]} {row[2]}")

conn.close()
print("\n完成！")
