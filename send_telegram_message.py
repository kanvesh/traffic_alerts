import requests

def send_message(text='script is running', chat_id= '-4812253274', bot_token='7852722952:AAFeGz4HET5UQTNbobGbv0VlV9v9Qh1Ke48'):
    BOT_TOKEN = bot_token
    CHAT_ID = chat_id
    MESSAGE = text

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": MESSAGE
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print(text)
        return 0
    else:
        print("Failed to send message:", response.text)
        return 1





