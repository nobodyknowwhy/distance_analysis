# import subprocess
#
# # 定义命令和参数
# command = [
#     "sqlacodegen",
#     # "postgresql+psycopg2://user_2024009:Hs%66pm58!!4wHmD@tdb.wushifj.com:55432/wushi_2024009",
#     # "--schema", "public",
#     # "--tables", "ws_data_source",
#     # "--outfile", "D:/gs/desti.py"
# ]
#
# # 运行命令
# try:
#     subprocess.run(command, check=True)
#     print("模型代码生成成功！")
# except subprocess.CalledProcessError as e:
#     print(f"模型代码生成失败：{e}")

import psycopg2

# 数据库连接参数
conn_string = "postgresql+psycopg2://user_2024009:Hs%66pm58!!4wHmD@tdb.wushifj.com:55432/wushi_2024009"

try:
    # 尝试建立连接
    conn = psycopg2.connect(conn_string)
    print("连接成功！")

    conn.close()
except psycopg2.Error as e:
    print("连接失败：", e)