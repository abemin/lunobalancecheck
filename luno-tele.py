###LUNO  Balance Checker ###
###By Muhaimi###
import requests
import base64
import json

#api url to retrieve balance
base_url = "https://api.luno.com/api/1/balance"
#api url to get convertion rate
conv_base_url = "https://api.luno.com/api/1/ticker"

username = "<luno_key_id>"
password = "<luno_secret>"

assets = ["XBT", "ETH", "XRP", "SOL", "LINK", "BCH"]
conv_assets = ["XBTMYR", "ETHMYR", "XRPMYR", "SOLMYR", "LINKMYR", "BCHMYR"] #using MYR conversion. Change to you currency pair.

# Encode the username and password to create the Base64 value
credentials = f"{username}:{password}"
base64_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

# Request headers
headers = {
    "Authorization": f"Basic {base64_credentials}"
}

#array to store balance value of each asset
balance_array = []

for asset in assets:
    params = {"assets": asset}
    response = requests.get(base_url, params=params, headers=headers)

    if response.status_code == 200:
        # Parse the JSON data
        data = json.loads(response.text)

        # Extract balance values
        balance_info = data["balance"][0]
        my_asset = balance_info["asset"]
        unformatted_balance = float(balance_info["balance"])
        unfloat_balance = format(unformatted_balance, ".6f")
        balance = float(unfloat_balance)
        balance_array.append(balance)

    else:
        print(f"Failed to fetch data for asset {asset}. Status code: {response.status_code}")

################################################################################################
#array to store last_trade value of each pair
last_trade_array = []

for pair in conv_assets:
    conv_params = {"pair": pair}
    response = requests.get(conv_base_url, params=conv_params, headers=headers)

    if response.status_code == 200:
        # Parse the JSON data
        conv_data = json.loads(response.text)

        # Extract last trade values
        pairs = conv_data["pair"]
        unformatted_last_trade = float(conv_data["last_trade"])
        unfloat_last_trade = format(unformatted_last_trade, ".6f")
        last_trade = float(unfloat_last_trade)
        last_trade_array.append(last_trade)

    else:
        print(f"Failed to fetch data for asset {pair}. Status code: {response.status_code}")

result_array = []

for i in range(len(balance_array)):
    result = balance_array[i] * last_trade_array[i]
    formatted_multiplied_value = format(result, ".6f")
    result_array.append(formatted_multiplied_value)

float_array = [float(value) for value in result_array]
total_sum = sum(float_array)
new_total_sum = format(total_sum, ".2f")
total_balance = float(new_total_sum)

#print("RM:", total_balance)

#-----telegram bot notification-----

# Replace with your Telegram Bot API token and chat ID
TELEGRAM_BOT_TOKEN = '<telegram_bot_token>' #use botfather to create tele bot
TELEGRAM_CHAT_ID = '<telegram_chat_id>' #Your chat id. use @rawdatabot to get id.

def send_telegram_notification(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    response = requests.post(telegram_url, data=payload)
    return response.status_code == 200

#calculate percentage
def calculate_percentage_change(total_wallet, total_balance):
    percentage_change = ((total_wallet - total_balance) / total_wallet) * 100
    return percentage_change

total_wallet = 350
percentage_change = calculate_percentage_change(total_wallet, total_balance)

if percentage_change > 0:
    message = f"You have lost {abs(percentage_change):.2f}%. Wallet balance: RM{total_balance}"
#    send_notification = send_telegram_notification(message)
elif percentage_change < 0:
    message = f"You have gained {abs(percentage_change):.2f}%. Wallet balance: RM{total_balance}"
    send_notification = send_telegram_notification(message) #send only if gained
else:
    message = "There is no change."
    send_notification = send_telegram_notification(message)
