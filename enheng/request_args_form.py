from flask import Flask, request

app = Flask(__name__)

@app.route('/search', methods=['POST', 'GET'])
def search():
    # 从 URL 查询字符串中获取参数
    query = request.args.get('q')
    if query:
        return f"搜索关键词: {query}"
    else:
        return "请输入搜索关键词"

if __name__ == '__main__':
    app.run(debug=True)