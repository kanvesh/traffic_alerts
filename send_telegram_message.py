import requests

def send_message(text='hello', chat_id= '6220958701', bot_token='7685380393:AAEymOd4aieB8tz-krxOLJi_Y2UfWJh-TeI'):
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
        print("Message sent successfully!")
        return 0
    else:
        print("Failed to send message:", response.text)
        return 1


send_message('success')


