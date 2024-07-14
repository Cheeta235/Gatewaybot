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
        f"𝐔𝐑𝐋: {results['url']}\n"
        f"𝐏𝐀𝐘𝐌𝐄𝐍𝐓 𝐆𝐀𝐓𝐄𝐖𝐀𝐘𝐒: {', '.join(results['payment_gateways']) if results['payment_gateways'] else 'None'}\n"
        f"𝐂𝐀𝐏𝐓𝐂𝐇𝐀: {'Yes' if results['captcha'] else 'No'}\n"
        f"𝐂𝐋𝐎𝐔𝐃𝐅𝐋𝐀𝐑𝐄: {'Yes' if results['cloudflare'] else 'No'}\n"
        f"𝐆𝐑𝐀𝐏𝐇𝐐𝐋 𝐃𝐄𝐓𝐄𝐂𝐓𝐄𝐃: {'Yes' if results['graphql'] else 'No'}\n"
        f"𝐏𝐋𝐀𝐓𝐅𝐎𝐑𝐌: {results['platform'] or 'Unknown'}\n"
        f"𝐇𝐓𝐓𝐏 𝐒𝐓𝐀𝐓𝐔𝐒: {results['http_status']}\n"
        f"𝐂𝐎𝐔𝐍𝐓𝐑𝐘: {results['country']}\n"
        f"⚠️ 𝐄𝐑𝐑𝐎𝐑: {results['error'] or 'None'}\n"
    )
    return analysis

# Command handlers
def handle_url_command(chat_id, text):
    if 'url_list' in context_data:
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(analyze_and_send, context_data['url_list'], [chat_id] * len(context_data['url_list']))
    else:
        send_message(chat_id, '⚠️ No URLs have been uploaded. Please upload a .txt file with URLs first.')

def handle_start_command(chat_id):
    send_message(chat_id, '👋 Hi! I am your Website Analyzer Bot. Send me a .txt file with URLs, and then use /url to start analyzing. 🕵️‍♂️')

def handle_file(chat_id, file_content):
    urls = file_content.decode('utf-8').splitlines()
    context_data['url_list'] = [url.strip() for url in urls if url.strip()]
    send_message(chat_id, "✅ URLs have been uploaded. Reply with /url to start the analysis.")

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
                            handle_url_command(chat_id, text)
                    elif document:
                        file_id = document['file_id']
                        file_info = requests.get(URL + 'getFile', params={'file_id': file_id}).json()
                        file_path = file_info['result']['file_path']
                        file_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
                        file_content = requests.get(file_url).content
                        handle_file(chat_id, file_content)

        time.sleep(1)

if __name__ == '__main__':
    main()
        if any(marker in response_text.lower() for marker in markers):
            return platform.capitalize()

    return None

# Function to format the analysis results
def format_analysis_results(results):
    analysis = (
        f"🔍 𝐒𝐈𝐓𝐄 𝐀𝐍𝐀𝐋𝐘𝐒𝐈𝐒 𝐑𝐄𝐒𝐔𝐋𝐓𝐒:\n"
        f"𝐔𝐑𝐋: {results['url']}\n"
        f"𝐏𝐀𝐘𝐌𝐄𝐍𝐓 𝐆𝐀𝐓𝐄𝐖𝐀𝐘𝐒: {', '.join(results['payment_gateways']) if results['payment_gateways'] else 'None'}\n"
        f"𝐂𝐀𝐏𝐓𝐂𝐇𝐀: {'Yes' if results['captcha'] else 'No'}\n"
        f"𝐂𝐋𝐎𝐔𝐃𝐅𝐋𝐀𝐑𝐄: {'Yes' if results['cloudflare'] else 'No'}\n"
        f"𝐆𝐑𝐀𝐏𝐇𝐐𝐋 𝐃𝐄𝐓𝐄𝐂𝐓𝐄𝐃: {'Yes' if results['graphql'] else 'No'}\n"
        f"𝐏𝐋𝐀𝐓𝐅𝐎𝐑𝐌: {results['platform'] or 'Unknown'}\n"
        f"𝐇𝐓𝐓𝐏 𝐒𝐓𝐀𝐓𝐔𝐒: {results['http_status']}\n"
        f"𝐂𝐎𝐔𝐍𝐓𝐑𝐘: {results['country']}\n"
        f"⚠️ 𝐄𝐑𝐑𝐎𝐑: {results['error'] or 'None'}\n"
    )
    return analysis

# Command handlers
def handle_url_command(chat_id, text):
    if 'url_list' in context_data:
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(analyze_and_send, context_data['url_list'], [chat_id] * len(context_data['url_list']))
se:
        send_message(chat_id, '⚠️ No URLs have been uploaded. Please upload a .txt file with URLs first.')

def handle_start_command(chat_id):
    send_message(chat_id, '👋 Hi! I am your Website Analyzer Bot. Send me a .txt file with URLs, and then use /url to start analyzing. 🕵️‍♂️')

def handle_file(chat_id, file_content):
    urls = file_content.decode('utf-8').splitlines()
    context_data['url_list'] = [url.strip() for url in urls if url.strip()]
    send_message(chat_id, "✅ URLs have been uploaded. Reply with /url to start the analysis.")

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
