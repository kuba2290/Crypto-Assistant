import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("Script started")

# Load environment variables
load_dotenv(find_dotenv())

# Get OpenAI API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
try:
    client = OpenAI(api_key=openai_api_key)
    print("OpenAI client created successfully")
except Exception as e:
    print(f"Error creating OpenAI client: {e}")
    exit(1)

def get_crypto_info(coin_id):
    print(f"Fetching crypto info for {coin_id}")
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if coin_id in data:
            price = data[coin_id]['usd']
            change_24h = data[coin_id]['usd_24h_change']
            return json.dumps({
                "coin": coin_id,
                "price_usd": price,
                "change_24h": round(change_24h, 2)
            })
    except requests.exceptions.RequestException as e:
        print(f"Error fetching crypto data: {e}")
    return json.dumps({"error": "Unable to fetch crypto data"})

def send_email(to_email, subject, body):
    print(f"Attempting to send email to {to_email}")
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    
    if not sender_email or not sender_password:
        print("Error: Email credentials not found in environment variables")
        return json.dumps({"error": "Email credentials not configured"})

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
        print("Email sent successfully")
        return json.dumps({"status": "Email sent successfully"})
    except Exception as e:
        print(f"Failed to send email: {e}")
        return json.dumps({"error": f"Failed to send email: {str(e)}"})

def run_conversation(messages):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_crypto_info",
                "description": "Get current price and 24h change for a cryptocurrency",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "coin_id": {
                            "type": "string",
                            "description": "The id of the cryptocurrency on CoinGecko, e.g., bitcoin",
                        },
                    },
                    "required": ["coin_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "send_email",
                "description": "Send an email with crypto information to the email address provided",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "to_email": {
                            "type": "string",
                            "description": "The recipient's email address",
                        },
                        "subject": {
                            "type": "string",
                            "description": "The subject of the email",
                        },
                        "body": {
                            "type": "string",
                            "description": "The body content of the email",
                        },
                    },
                    "required": ["to_email", "subject", "body"],
                },
            },
        },
    ]

    print("Sending request to OpenAI")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
        print("Received response from OpenAI")
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        return f"An error occurred: {e}"

    if tool_calls:
        available_functions = {
            "get_crypto_info": get_crypto_info,
            "send_email": send_email,
        }
        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            print(f"Calling function: {function_name}")
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )

        print("Sending follow-up request to OpenAI")
        try:
            second_response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
            )
            print("Received follow-up response from OpenAI")
            return second_response.choices[0].message.content
        except Exception as e:
            print(f"Error in follow-up OpenAI API call: {e}")
            return f"An error occurred in the follow-up request: {e}"
    else:
        return response_message.content

def main():
    messages = [
        {"role": "system", "content": "You are a crypto price checker assistant. You can check for the price of cryptocurrencies and send emails to addresses provided. It is okay to send emails as the user has consented to receive emails from you."}
    ]
    
    print("Welcome to the Crypto Assistant! Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Thank you for using the Crypto Assistant. Goodbye!")
            break
        
        messages.append({"role": "user", "content": user_input})
        response = run_conversation(messages)
        print("Assistant:", response)
        messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()