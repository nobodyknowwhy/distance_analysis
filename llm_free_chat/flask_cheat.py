import json
import re
import time

from flask import Flask, Response, stream_with_context

app = Flask(__name__)


def generate_stream(text):
    data_list = [
        {
            "event_data": "{\"message_id\":\"3656738361447938\",\"local_message_id\":\"504e2b40-1e81-11f0-a646-c9047f10b2d1\",\"conversation_id\":\"477572727965698\",\"section_id\":\"3459422669359874\",\"message_index\":809,\"conversation_type\":4}",
            "event_id": "0", "event_type": 2002},
        {
            "event_data": "{\"type\":\"seed_intention\",\"seed_intention\":{\"intention\":\"multi_agent\",\"detail\":\"Agent-Code\"}}",
            "event_id": "1", "event_type": 2010},
        {"event_data": "{\"type\":\"multi_agents_jump_to_agent\",\"agent_to_skill\":{\"skill_type\":16}}",
         "event_id": "2", "event_type": 2010},
        {
            "event_data": "{\"message\":{\"content_type\":2071,\"content\":\"{\\\"text\\\":\\\"不太明确你说的“1”具体代表\\\"}\"},\"message_id\":\"3656738361448962\",\"local_message_id\":\"504e2b40-1e81-11f0-a646-c9047f10b2d1\",\"conversation_id\":\"477572727965698\",\"section_id\":\"3459422669359874\",\"reply_id\":\"3656738361447938\",\"is_delta\":true,\"status\":4,\"input_content_type\":2001,\"message_index\":810,\"bot_id\":\"7338286299411103781\"}",
            "event_id": "3", "event_type": 2001},
        {
            "event_data": "{\"message\":{\"content_type\":2071,\"content\":\"{\\\"text\\\":\\\"什么意思。是对之前流式返回\\\"}\"},\"message_id\":\"3656738361448962\",\"local_message_id\":\"504e2b40-1e81-11f0-a646-c9047f10b2d1\",\"conversation_id\":\"477572727965698\",\"section_id\":\"3459422669359874\",\"reply_id\":\"3656738361447938\",\"is_delta\":true,\"status\":4,\"input_content_type\":2001,\"message_index\":810,\"bot_id\":\"7338286299411103781\"}",
            "event_id": "4", "event_type": 2001},
        {
            "event_data": "{\"message\":{\"content_type\":2071,\"content\":\"{\\\"text\\\":\\\"内容还有疑问，还是有新\\\"}\"},\"message_id\":\"3656738361448962\",\"local_message_id\":\"504e2b40-1e81-11f0-a646-c9047f10b2d1\",\"conversation_id\":\"477572727965698\",\"section_id\":\"3459422669359874\",\"reply_id\":\"3656738361447938\",\"is_delta\":true,\"status\":4,\"input_content_type\":2001,\"message_index\":810,\"bot_id\":\"7338286299411103781\"}",
            "event_id": "5", "event_type": 2001},
        {
            "event_data": "{\"message\":{\"content_type\":2071,\"content\":\"{\\\"text\\\":\\\"的编程需求呢？你可以详细说明一下。\\\"}\"},\"message_id\":\"3656738361448962\",\"local_message_id\":\"504e2b40-1e81-11f0-a646-c9047f10b2d1\",\"conversation_id\":\"477572727965698\",\"section_id\":\"3459422669359874\",\"reply_id\":\"3656738361447938\",\"is_delta\":true,\"status\":4,\"input_content_type\":2001,\"message_index\":810,\"bot_id\":\"7338286299411103781\"}",
            "event_id": "6", "event_type": 2001},
        {
            "event_data": "{\"message\":{\"content_type\":2071,\"content\":\"{\\\"text\\\":\\\"哎呀，我稍微测试一下6+6666666+6+6+6+6+6+\\\"}\"},\"message_id\":\"3656738361448962\",\"local_message_id\":\"504e2b40-1e81-11f0-a646-c9047f10b2d1\",\"conversation_id\":\"477572727965698\",\"section_id\":\"3459422669359874\",\"reply_id\":\"3656738361447938\",\"is_delta\":true,\"status\":4,\"input_content_type\":2001,\"message_index\":810,\"bot_id\":\"7338286299411103781\"}",
            "event_id": "6", "event_type": 2001},
        {
            "event_data": "{\"message\":{\"content_type\":2071,\"content\":\"{\\\"text\\\":\\\" \\\"}\"},\"message_id\":\"3656738361448962\",\"local_message_id\":\"504e2b40-1e81-11f0-a646-c9047f10b2d1\",\"conversation_id\":\"477572727965698\",\"section_id\":\"3459422669359874\",\"reply_id\":\"3656738361447938\",\"is_delta\":true,\"status\":1,\"is_finish\":true,\"has_suggest\":true,\"message_action_bar\":{},\"input_content_type\":2001,\"message_index\":810,\"bot_id\":\"7338286299411103781\",\"tts_content\":\"不太明确你说的“1”具体代表什么意思。是对之前流式返回内容还有疑问，还是有新的编程需求呢？你可以详细说明一下。 \"}",
            "event_id": "7", "event_type": 2001},
        {
            "event_data": "{\"message\":{\"content_type\":2002,\"content\":\"{\\\"suggest\\\":\\\"如何在后端代码中实现流式返回数据？\\\",\\\"suggestions\\\":[\\\"如何在后端代码中实现流式返回数据？\\\"]}\",\"id\":\"11a4ea64-605e-46cd-ace8-68986cde20f0\"},\"message_id\":\"3656738361448962\",\"local_message_id\":\"504e2b40-1e81-11f0-a646-c9047f10b2d1\",\"conversation_id\":\"477572727965698\",\"section_id\":\"3459422669359874\",\"reply_id\":\"3656738361447938\",\"is_delta\":true,\"status\":1,\"input_content_type\":2001,\"message_index\":810,\"bot_id\":\"7338286299411103781\"}",
            "event_id": "8", "event_type": 2001},
        {
            "event_data": "{\"message\":{\"content_type\":2002,\"content\":\"{\\\"suggest\\\":\\\"前端如何接收和处理流式返回的数据？\\\",\\\"suggestions\\\":[\\\"前端如何接收和处理流式返回的数据？\\\"]}\",\"id\":\"11a4ea64-605e-46cd-ace8-68986cde20f0\"},\"message_id\":\"3656738361448962\",\"local_message_id\":\"504e2b40-1e81-11f0-a646-c9047f10b2d1\",\"conversation_id\":\"477572727965698\",\"section_id\":\"3459422669359874\",\"reply_id\":\"3656738361447938\",\"is_delta\":true,\"status\":1,\"input_content_type\":2001,\"message_index\":810,\"bot_id\":\"7338286299411103781\"}",
            "event_id": "9", "event_type": 2001},
        {
            "event_data": "{\"message\":{\"content_type\":2002,\"content\":\"{\\\"suggest\\\":\\\"流式返回数据时可能会遇到哪些问题？\\\",\\\"suggestions\\\":[\\\"流式返回数据时可能会遇到哪些问题？\\\"]}\",\"id\":\"11a4ea64-605e-46cd-ace8-68986cde20f0\"},\"message_id\":\"3656738361448962\",\"local_message_id\":\"504e2b40-1e81-11f0-a646-c9047f10b2d1\",\"conversation_id\":\"477572727965698\",\"section_id\":\"3459422669359874\",\"reply_id\":\"3656738361447938\",\"is_delta\":true,\"status\":1,\"is_finish\":true,\"has_suggest\":true,\"message_action_bar\":{},\"input_content_type\":2001,\"message_index\":810,\"bot_id\":\"7338286299411103781\",\"tts_content\":\"不太明确你说的“1”具体代表什么意思。是对之前流式返回内容还有疑问，还是有新的编程需求呢？你可以详细说明一下。 \"}",
            "event_id": "10", "event_type": 2001},
        {"event_data": "{}", "event_id": "11", "event_type": 2003}
    ]

    # 模拟流式返回
    for data in data_list:

        json_data = json.dumps(data)

        yield f"data: {json_data}\n\n"
        time.sleep(0.5)  # 模拟数据生成的延迟


@app.route('/stream', methods=['POST'])
def stream():
    text = ''
    return Response(stream_with_context(generate_stream(text)), content_type='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True)
