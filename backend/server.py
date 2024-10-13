from bottle import *
import os
import requests
import json
import mysql.connector
from datetime import datetime

app = Bottle()

def store_response_in_db(user_prompt, system_response):
    try:
        cnx = mysql.connector.connect(
            user='root',
            password='',
            host='localhost',
            database='cmpe'
        )

        cursor = cnx.cursor()
        insert_query = """
            INSERT INTO gpt_history (role, message, time)
            VALUES (%s, %s, %s)
        """

        current_time = datetime.now()
        data = [
            ('user', user_prompt, current_time),
            ('assistant', system_response, current_time)
        ]

        cursor.executemany(insert_query, data)
        cnx.commit()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()


def get_history():
    try:
        cnx = mysql.connector.connect(
            user='root',
            password='',
            host='localhost',
            database='cmpe'
        )
        cursor = cnx.cursor(dictionary=True)

        select_query = """
            SELECT role, message, time
            FROM gpt_history
            ORDER BY time ASC
        """

        cursor.execute(select_query)
        records = cursor.fetchall()

        messages = []
        for record in records:
            if record['role'] and record['message']:
                messages.append({
                    'role': record['role'],
                    'content': record['message']
                })

        return messages
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()


def get_chatgpt_response(user_prompt):

    api_key = os.getenv('OPENAI_API_KEY')
    chatgpt_api_endpoint = 'https://api.openai.com/v1/chat/completions'

    tax_prompt = (
        "You were hired as part of Deloitte Auditor team that specializes in development of Audit for commercial companies and individuals. "
        "As part of the auditor's day to day job, they need to study US Tax law to file appropriate tax deductions to benefit the clients. "
        "You should help auditor in their day-to-day job. Give them clear and precise answers for all queries. "
        "Queries should be only regarding tax law. If something else is asked, return a warning message to limit prompts only to Tax related questions. "
        f"User prompt is: {user_prompt}"
    )

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    messages = get_history()
    messages.append({'role': 'user', 'content': tax_prompt})

    data = {
        'model': 'gpt-3.5-turbo',
        'max_tokens': 1024,
        'temperature': 0.7,
        'messages': messages
    }

    response = requests.post(chatgpt_api_endpoint, headers=headers, json=data)
    
    if response.status_code == 200:
        response_json = response.json()
        message = response_json['choices'][0]['message']['content']
        store_response_in_db(user_prompt, message)
        return message
    else:
        return f"Error: {response.status_code} - {response.text}"


@hook('after_request')
def enable_cors():
    print("enable_cors called")
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@route('/tax-chat', method=['OPTIONS', 'POST'])
def handle_prompt():
    if request.method == 'OPTIONS':
        response.status = 200
        return ''

    data = request.body.read()
    
    try:
        data_str = data.decode('utf-8')
        data_dict = json.loads(data_str)
    except json.JSONDecodeError as e:
        response.status = 400
        return {"error": "Invalid JSON"}
    
    user_prompt = data_dict['userPrompt']
    if not user_prompt:
        response.status = 400
        return {"error": "No prompt provided"}

    chatgpt_response = get_chatgpt_response(user_prompt)
    return {"response": chatgpt_response}


if __name__ == '__main__': 
    run(host='0.0.0.0', port='8888')    
