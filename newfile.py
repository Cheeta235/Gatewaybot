import requests
import time

# Replace with your bot token
TOKEN = '7040333422:AAGdjBmAzXluC2Hmg3vJfnU8B1rzhzNcfwM'
URL = f'https://api.telegram.org/bot{TOKEN}/'

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

# Functions to analyze websites
def analyze_site(url):
    result = {
        'url': url, 'payment_gateway': None, 'captcha': False, 
        'cloudflare': False, 'graphql': False, 'platform': None, 
        'http_status': None, 'content_type': None, 'cookies': {}, 
        'error': None
    }

    try:
        response = requests.get(url, timeout=10)
        headers = response.headers
        content_type = headers.get('Content-Type', '')
        response_text = response.text
        cookies = response.cookies.get_dict()

        result.update({
            'payment_gateway': check_for_payment_gateway(headers, response_text, cookies),
            'cloudflare': check_for_cloudflare(response_text),
            'captcha': check_for_captcha(response_text),
            'graphql': check_for_graphql(response_text),
            'platform': check_for_platform(response_text),
            'http_status': response.status_code,
            'content_type': content_type,
            'cookies': cookies
        })

    except requests.Timeout:
        result['error'] = '⏰ Timeout error. Unable to fetch the page within the specified time.'
    except Exception as e:
        result['error'] = f'❌ Error: {str(e)}'
    
    return result

def check_for_payment_gateway(headers, response_text, cookies):
    gateway_keywords = [
        'stripe', 'paypal', 'square', 'venmo', 'bitcoin', 'braintree', 'amazon-pay',
        'adyen', '2checkout', 'skrill', 'authorize.net', 'worldpay', 'payu', 'paytm',
        'afterpay', 'alipay', 'klarna', 'affirm', 'bluesnap', 'checkout.com', 'dwolla',
        'paddle', 'payoneer', 'sagepay', 'wechat pay', 'yandex.money', 'zelle',
        'shopify', 'buy now', 'add to cart', 'store', 'checkout', 'cart', 'shop now',
        'card', 'payment', 'gateway', 'checkout button', 'pay with'
    ]

    combined_text = response_text.lower() + str(headers).lower() + str(cookies).lower()
    
    for keyword in gateway_keywords:
        if keyword in combined_text:
            return keyword.capitalize()

    return None

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

# Main function to handle bot logic
def main():
    offset = None

    while True:
        updates = get_updates(offset)
        for update in updates.get('result', []):
            update_id = update['update_id']
            message = update.get('message', {})
            chat_id = message.get('chat', {}).get('id')
            text = message.get('text', '')

            if text.startswith('/url'):
                url = text.split(' ', 1)[-1].strip()
                if url:
                    results = analyze_site(url)
                    send_message(chat_id, format_analysis_results(results))
                else:
                    send_message(chat_id, '❓ Please provide a URL with /url <URL>.')
            elif text == '/start':
                send_message(chat_id, '👋 Hi! I am your Website Analyzer Bot. Send me a URL with /url <URL> to analyze it. 🕵️‍♂️')
            else:
                send_message(chat_id, '⚠️ Invalid command. Send /start to begin or /url <URL> to analyze a URL.')

            offset = update_id + 1

        time.sleep(1)

# Function to format the analysis results
def format_analysis_results(results):
    analysis = (
        f"🔍 Analysis Results for {results['url']}\n"
        f"---------------------------------\n"
        f"🌐 HTTP Status: {results['http_status']}\n"
        f"💳 Payment Gateway: {results['payment_gateway'] or 'None'}\n"
        f"☁ Cloudflare Detected: {'Yes' if results['cloudflare'] else 'No'}\n"
        f"🔒 Captcha Detected: {'Yes' if results['captcha'] else 'No'}\n"
        f"🔎 GraphQL Detected: {'Yes' if results['graphql'] else 'No'}\n"
        f"🛠 Platform: {results['platform'] or 'Unknown'}\n"
        f"📄 Content Type: {results['content_type']}\n"
        f"🍪 Cookies: {results['cookies']}\n"
        f"⚠️ Error: {results['error'] or 'None'}\n"
    )
    return analysis

# Run the bot
if __name__ == '__main__':
    main()
