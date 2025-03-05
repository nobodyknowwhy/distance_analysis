import asyncio

async def fetch_data():
    print("Start fetching data...")
    # 模拟网络请求，异步等待2秒
    await asyncio.sleep(2)
    print("Data fetched successfully")
    return {"data": 123}

async def main():
    data = 1
    print(data)

# 启动事件循环
asyncio.run(main())