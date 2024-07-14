import requests
import time
from datetime import datetime, timedelta
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
import random
import string

# Replace with your bot token
TOKEN = '7040333422:AAE_WUPYhjauw0VA5Ms7V5IA8OgtxjOCqv0'
URL = f'https://api.telegram.org/bot{TOKEN}/'
MAX_MESSAGE_LENGTH = 4096

# Functions to interact with Telegram API
def get_updates(offset=None):
    url = URL + 'getUpdates'
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(url, params=params)
    return response.json()

def send_message(chat_id, text):
    url = URL + 'sendMessage'
    params = {'chat_id': chat_id, 'text': text}
    requests.get(url, params=params)

def split_message(text):
    """Splits a long message into smaller parts to fit within Telegram's limits."""
    return [text[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(text), MAX_MESSAGE_LENGTH)]

# Functions to analyze websites
def analyze_site(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    result = {
        'url': url, 'payment_gateways': [], 'captcha': False, 
        'cloudflare': False, 'graphql': False, 'platform': None, 
        'http_status': None, 'content_type': None, 'cookies': {}, 
        'error': None, 'country': None
    }

    try:
        response = requests.get(url, timeout=10)
        headers = response.headers
        content_type = headers.get('Content-Type', '')
        response_text = response.text
        cookies = response.cookies.get_dict()
        country = headers.get('CF-IPCountry', 'Unknown')

        result.update({
            'payment_gateways': check_for_payment_gateways(headers, response_text, cookies),
            'cloudflare': check_for_cloudflare(response_text),
            'captcha': check_for_captcha(response_text),
            'graphql': check_for_graphql(response_text),
            'platform': check_for_platform(response_text),
            'http_status': f"{response.raw.version} {response.status_code} {response.reason}",
            'content_type': content_type,
            'cookies': cookies,
            'country': country
        })

    except requests.Timeout:
        result['error'] = '⏰ Timeout error. Unable to fetch the page within the specified time.'
    except Exception as e:
        result['error'] = f'❌ Error: {str(e)}'
    
    return result

def check_for_payment_gateways(headers, response_text, cookies):
    gateway_keywords = [
        'stripe', 'paypal', 'square', 'venmo', 'bitcoin', 'braintree', 'amazon-pay',
        'adyen', '2checkout', 'skrill', 'authorize.net', 'worldpay', 'payu', 'paytm',
        'afterpay', 'alipay', 'klarna', 'affirm', 'bluesnap', 'checkout.com', 'dwolla',
        'paddle', 'payoneer', 'sagepay', 'wechat pay', 'yandex.money', 'zelle',
        'shopify', 'buy now', 'add to cart', 'store', 'checkout', 'cart', 'shop now',
        'card', 'payment', 'gateway', 'checkout button', 'pay with'
    ]

    combined_text = response_text.lower() + str(headers).lower() + str(cookies).lower()
    detected_gateways = [keyword.capitalize() for keyword in gateway_keywords if keyword in combined_text]

    return detected_gateways

def check_for_cloudflare(response_text):
    cloudflare_markers = ['checking your browser', 'cf-ray', 'cloudflare']
    return any(marker in response_text.lower() for marker in cloudflare_markers)

def check_for_captcha(response_text):
    captcha_markers = ['recaptcha', 'g-recaptcha']
    return any(marker in response_text.lower() for marker in captcha_markers)

def check_for_graphql(response_text):
    graphql_markers = ['graphql', 'application/graphql']
    return any(marker in response_text.lower() for marker in graphql_markers)

def check_for_platform(response_text):
    platform_markers = {
        'woocommerce': ['woocommerce', 'wc-cart', 'wc-ajax'],
        'magento': ['magento', 'mageplaza'],
        'shopify': ['shopify', 'myshopify'],
        'prestashop': ['prestashop', 'addons.prestashop'],
        'opencart': ['opencart', 'route=common/home'],
        'bigcommerce': ['bigcommerce', 'stencil'],
        'wordpress': ['wordpress', 'wp-content'],
        'drupal': ['drupal', 'sites/all'],
        'joomla': ['joomla', 'index.php?option=com_']
    }

    for platform, markers in platform_markers.items():
        if any(marker in response_text.lower() for marker in markers):
            return platform.capitalize()

    return None

# Function to format the analysis results
def format_analysis_results(results):
    analysis = (
        f"🔍 𝐒𝐈𝐓𝐄 𝐀𝐍𝐀𝐋𝐘𝐒𝐈𝐒 𝐑𝐄𝐒𝐔𝐋𝐓𝐒:\n"
        f"𝐎𝐰𝐧𝐞𝐫: @cheetax1\n"
        f"𝐔𝐑𝐋: {results['url']}\n"
        f"𝐏𝐀𝐘𝐌𝐄𝐍𝐓 𝐆𝐀𝐓𝐄𝐖𝐀𝐘𝐒: {', '.join(results['payment_gateways']) if results['payment_gateways'] else 'None'}\n"
        f"𝐂𝐀𝐏𝐓𝐂𝐇𝐀: {'Yes' if results['captcha'] else 'No'}\n"
        f"𝐂𝐋𝐎𝐔𝐃𝐅𝐋𝐀𝐑𝐄: {'Yes' if results['cloudflare'] else 'No'}\n"
        f"𝐆𝐑𝐀𝐏𝐇𝐐𝐋 𝐃𝐄𝐓𝐄𝐂𝐓𝐄𝐃: {'Yes' if results['graphql'] else 'No'}\n"
        f"𝐏𝐋𝐀𝐓𝐅𝐎𝐑𝐌: {results['platform'] or 'Unknown'}\n"
        f"𝐇𝐓𝐓𝐏 𝐒𝐓𝐀𝐓𝐔𝐒: {results['http_status']}\n"
        f"𝐂𝐎𝐔𝐍𝐓𝐑𝐘: {results['country']}\n"
        f"𝐄𝐑𝐑𝐎𝐑: {results['error'] or 'None'}\n"
    )
    return analysis

# Command handlers
def handle_url_command(chat_id, text):
    if text.startswith('/url '):
        url = text.split(' ', 1)[1]
        analyze_and_send(url, chat_id)
    elif 'url_list' in context_data:
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(analyze_and_send, context_data['url_list'], [chat_id] * len(context_data['url_list']))
        send_message(chat_id, '𝙖𝙡𝙡 𝙪𝙧𝙡𝙨 𝙝𝙖𝙫𝙚 𝙗𝙚𝙚𝙣 𝙘𝙝𝙚𝙘𝙠𝙚𝙙. 𝙛𝙤𝙧 𝙢𝙤𝙧𝙚 𝙗𝙤𝙩 𝙪𝙥𝙙𝙖𝙩𝙚𝙨, 𝙟𝙤𝙞𝙣 https://t.me/+T1NZ5uF968I2YTU1.')
    else:
        send_message(chat_id, '⚠️ 𝙉𝙊 𝙐𝙍𝙇𝙎 𝙃𝘼𝙑𝙀 𝘽𝙀𝙀𝙉 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿. 𝙋𝙇𝙀𝘼𝙎𝙀 𝙐𝙋𝙇𝙊𝘼𝘿 𝘼 .𝙏𝙓𝙏 𝙁𝙄𝙇𝙀 𝙒𝙄𝙏𝙃 𝙐𝙍𝙇𝙎 𝙁𝙄𝙍𝙎𝙏.')

def handle_start_command(chat_id):
    send_message(chat_id, '👋 𝙃𝙄! 𝙄 𝘼𝙈 𝙔𝙊𝙐𝙍 𝙒𝙀𝘽𝙎𝙄𝙏𝙀 𝘼𝙉𝘼𝙇𝙔𝙕𝙀𝙍 𝘽𝙊𝙏. 𝙎𝙀𝙉𝘿 𝙈𝙀 𝘼 .𝙏𝙓𝙏 𝙁𝙄𝙇𝙀 𝙒𝙄𝙏𝙃 𝙐𝙍𝙇𝙎, 𝘼𝙉𝘿 𝙏𝙃𝙀𝙉 𝙐𝙎𝙀 /𝙐𝙍𝙇 𝙏𝙊 𝙎𝙏𝘼𝙍𝙏 𝘼𝙉𝘼𝙇𝙔𝙕𝙄𝙉𝙂. 🕵️‍♂️')

def handle_file(chat_id, file_content):
    urls = file_content.decode('utf-8').splitlines()
    context_data['url_list'] = [url.strip() for url in urls if url.strip()]
    send_message(chat_id, "✅  𝙐𝙍𝙇𝙎 𝙃𝘼𝙑𝙀 𝘽𝙀𝙀𝙉 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿. 𝙍𝙀𝙋𝙇𝙔 𝙒𝙄𝙏𝙃 /𝙐𝙍𝙇 𝙏𝙊 𝙎𝙏𝘼𝙍𝙏 𝙏𝙃𝙀 𝘼𝙉𝘼𝙇𝙔𝙎𝙄𝙎.")

def handle_cmds_command(chat_id):
    commands = (
        "/url - To Analyze URLs from the uploaded .txt file or analyze a single URL if provided as /url <link>.\n"
        "/cmds - available commands and their descriptions."
    )
    send_message(chat_id, commands)

def analyze_and_send(url, chat_id):
    result = analyze_site(url)
    analysis = format_analysis_results(result)
    messages = split_message(analysis)
    for message in messages:
        send_message(chat_id, message)

# Initialize context and user data
context_data = {}

# Main loop to process updates
def main():
    offset = None
    while True:
        updates = get_updates(offset)
        if 'result' in updates:
            for update in updates['result']:
                offset = update['update_id'] + 1
                if 'message' in update:
                    message = update['message']
                    chat_id = message['chat']['id']
                    text = message.get('text')
                    document = message.get('document')

                    if text:
                        if text.startswith('/start'):
                            handle_start_command(chat_id)
                        elif text.startswith('/url'):
                            handle_url_command(chat_id,
                            text)
                        elif text.startswith('/cmds'):
                            handle_cmds_command(chat_id)
                    elif document:
                        file_id = document['file_id']
                        file_url = URL + f'getFile?file_id={file_id}'
                        file_path = requests.get(file_url).json()['result']['file_path']
                        file_content = requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{file_path}').content
                        handle_file(chat_id, file_content)

if __name__ == '__main__':
    main()
