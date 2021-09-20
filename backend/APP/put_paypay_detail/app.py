import json
import os
import logging
import sys
from datetime import datetime
from dateutil.tz import gettz


from common import (common_const, line, utils, flex_message)
from validation.smart_register_param_check import SmartRegisterParamCheck
from common.channel_access_token import ChannelAccessToken
from smart_register.smart_register_order_info import SmartRegisterOrderInfo

import paypayopa
import polling

# 環境変数
LIFF_CHANNEL_ID = int(os.environ.get("LIFF_CHANNEL_ID"))
LIFF_URL = os.environ.get("LIFF_URL")
LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL")
CHANNEL_ACCESS_TOKEN_DB = os.environ.get("CHANNEL_ACCESS_TOKEN_DB")
DETAILS_PASS = os.environ.get("DETAILS_PASS")
                 
# PayPay API
PAY_PAY_API_KEY = os.environ.get("PAY_PAY_API_KEY")
PAY_PAY_API_SECRET = os.environ.get("PAY_PAY_API_SECRET")
PAY_PAY_API_MERCHANT_ID = os.environ.get("PAY_PAY_API_MERCHANT_ID")
if (os.environ.get("PAY_PAY_IS_PROD") == 'True'
    or os.environ.get("PAY_PAY_IS_PROD") == 'true'): 
    PAY_PAY_IS_PROD = True
else:
    PAY_PAY_IS_PROD = False
client = paypayopa.Client(auth=(PAY_PAY_API_KEY, PAY_PAY_API_SECRET),
                         production_mode=PAY_PAY_IS_PROD)
client.set_assume_merchant(PAY_PAY_API_MERCHANT_ID)

# ログ出力の設定
logger = logging.getLogger()
if LOGGER_LEVEL == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
# LINEリソースの宣言
OA_CHANNEL_ID = os.getenv('OA_CHANNEL_ID', None)
if OA_CHANNEL_ID is None:
    logger.error('Specify CHANNEL_ID as environment variable.')
    sys.exit(1)

# AWSリソースの生成
order_info_table = SmartRegisterOrderInfo()
accesstoken_table = ChannelAccessToken()


def send_messages(order_info, datetime_now):
    """
    OAへメッセージを送信をする
    Parameters
    ----------
        order_info:dict
            該当ユーザーの注文情報
        datetime_now:string
            決済日時
    Returns
    -------
        なし
    """
    # DBより短期チャネルアクセストークンを取得
    channel_access_token = accesstoken_table.get_item(OA_CHANNEL_ID)
    if channel_access_token is None:
        logger.error(
            'CHANNEL_ACCESS_TOKEN in Specified CHANNEL_ID: %s is not exist.',
            OA_CHANNEL_ID)
    else:
        order_id = order_info['orderId']
        details_url = LIFF_URL + DETAILS_PASS + '?orderId=' + order_id
        flex_obj = flex_message.create_receipt(
            order_info, datetime_now, details_url)

        line.send_push_message(
            channel_access_token['channelAccessToken'],
            flex_obj, order_info['userId'])

def fetch_payment_details(merchant_payment_id):
    """
    支払いの詳細を取得する
    Parameters
    ----------
    merchant_payment_id
        販売者が提供する一意の支払いトランザクションID
    Returns
    -------
    status
    """
    resp = client.Code.get_payment_details(merchant_payment_id)
    if (str(resp['data']) == 'None'):
        return {
            'error': 'true'
        }
    return resp['data']['status']

def is_correct_response(resp):
    logger.info(resp)
    return resp

def lambda_handler(event, context):
    """
    PayPay API(confirm)の通信結果を返す
    Parameters
    ----------
        event : dict
            POST時に渡されたパラメータ
        context : dict
            コンテキスト内容。
    Returns
    -------
        response : dict
            PayPay APIの通信結果
    """
    # パラメータログ
    logger.info(event)
    body = json.loads(event['body'])
    if body is None:
        error_msg_display = common_const.const.MSG_ERROR_NOPARAM
        return utils.create_error_response(error_msg_display, 400)

    # パラメータバリデーションチェック
    param_checker = SmartRegisterParamCheck(body)
    if error_msg := param_checker.check_api_put_paypay_confirm():
        error_msg_disp = ('\n').join(error_msg)
        logger.error(error_msg_disp)
        return utils.create_error_response(error_msg_disp, status=400)  # noqa: E501

    order_id = body['orderId']
    # 注文履歴から決済金額を取得
    order_info = order_info_table.get_item(order_id)

    amount = float(order_info['amount'])
    transaction_id = 999999
    currency = 'JPY'
    datetime_now = datetime.now(gettz('Asia/Tokyo'))

    try:
        polling.poll(
            lambda: fetch_payment_details(order_id) == 'COMPLETED' or fetch_payment_details(order_id) == 'FAILED',
            check_success=is_correct_response,
            step=2,
            timeout=100)
        
        api_response = client.Code.get_payment_details(order_id)
        # DB更新
        order_info_table.update_transaction(
            order_id, transaction_id, utils.get_ttl_time(datetime_now))

        # メッセージ送信処理
        send_messages(order_info,
                      datetime_now.strftime('%Y/%m/%d %H:%M:%S'))

    except Exception as e:
        logger.exception('Occur Exception: %s', e)
        return utils.create_error_response('Error')

    response = utils.create_success_response(
        json.dumps(api_response))
    logger.info('response %s', response)
    return response
