# Crypto Assistant

Crypto Assistant is a Python-based conversational AI tool that provides cryptocurrency price information and can send email updates about crypto prices. It uses the OpenAI API for natural language processing and the CoinGecko API for fetching cryptocurrency data.

## Features

- **Real-time Cryptocurrency Price Checking**: Get current prices and 24-hour price changes for various cryptocurrencies.
- **Email Notifications**: Send email updates with cryptocurrency information.
- **Conversational Interface**: Interact with the assistant using natural language.
- **Multi-function Capability**: The assistant can perform multiple tasks in a single conversation.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- An OpenAI API key
- A Gmail account (for sending emails)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/crypto-assistant.git
   cd crypto-assistant
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables by creating a `.env` file in the project root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   SENDER_EMAIL=your_gmail_address@gmail.com
   SENDER_PASSWORD=your_gmail_app_password
   ```

   Replace the placeholders with your actual OpenAI API key, Gmail address, and Gmail App Password.

## Setting up Gmail App Password

To use the email functionality, you need to set up an App Password for your Gmail account:

1. Go to your Google Account settings.
2. Navigate to the Security section.
3. Under "Signing in to Google," select 2-Step Verification (turn it on if not already).
4. At the bottom of the page, select App passwords.
5. Choose "Mail" and "Other (Custom name)" from the dropdowns.
6. Enter a name for the app (e.g., "Crypto Assistant") and click "Generate".
7. Use the generated 16-character password as your `SENDER_PASSWORD` in the `.env` file.

## Usage

To start the Crypto Assistant, run:

```
python crypto_assistant.py
```

Once started, you can interact with the assistant using natural language. For example:

- "What's the current price of Bitcoin?"
- "Can you send me an email with the latest prices of Ethereum and Dogecoin?"
- "Check the 24-hour change for Cardano and email it to me at user@example.com"

To exit the assistant, simply type 'exit'.

## Security Notes

- Never share your `.env` file or its contents publicly.
- Keep your OpenAI API key and Gmail App Password confidential.
- Regularly update your passwords and API keys for security.

## Contributing

Contributions to the Crypto Assistant project are welcome. Please feel free to submit a Pull Request.


## Acknowledgments

- OpenAI for providing the GPT model API
- CoinGecko for their cryptocurrency data API
