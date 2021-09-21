import json
import os
import logging

from common import (common_const, line, utils)
from validation.smart_register_param_check import SmartRegisterParamCheck
from smart_register.smart_register_order_info import SmartRegisterOrderInfo

import paypayopa

# 環境変数
LIFF_CHANNEL_ID = int(os.environ.get("LIFF_CHANNEL_ID"))
LIFF_URL = os.environ.get("LIFF_URL")
LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL")
PAYMENT_IMG_URL = os.environ.get("PAYMENT_IMG_URL")
CONFIRM_URL_PASS = os.environ.get("CONFIRM_URL_PASS")
                 
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

# AWSリソースの生成
order_info_table = SmartRegisterOrderInfo()


def update_orderinfo(order_id):
    """
    注文情報の更新日を更新する
    Parameters
    ----------
        order_id:string
            注文番号
    Returns
    -------
        なし
    """
    order_info_table.update_date(order_id)


def lambda_handler(event, context):
    """
    PayPay API(reserve)の通信結果を返す
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
    req_body = json.loads(event['body'])

    if req_body is None:
        error_msg_display = common_const.const.MSG_ERROR_NOPARAM
        return utils.create_error_response(error_msg_display, 400)
    # ユーザーID取得
    try:
        user_profile = line.get_profile(
            req_body['idToken'], LIFF_CHANNEL_ID)
        if 'error' in user_profile and 'expired' in user_profile['error_description']:  # noqa 501
            return utils.create_error_response('Forbidden', 403)
        else:
            req_body['userId'] = user_profile['sub']
    except Exception:
        logger.exception('不正なIDトークンが使用されています')
        return utils.create_error_response('Error')

    # パラメータバリデーションチェック
    param_checker = SmartRegisterParamCheck(req_body)
    if error_msg := param_checker.check_api_put_paypay_request():
        error_msg_disp = ('\n').join(error_msg)
        logger.error(error_msg_disp)
        return utils.create_error_response(error_msg_disp, status=400)  # noqa: E501

    domain_url = event['headers']['origin']
    order_id = req_body['orderId']
    confirm_url = LIFF_URL + CONFIRM_URL_PASS
    logger.debug('confirm_url: %s', confirm_url)

    try:
        # 注文履歴から決済金額を取得
        order_info = order_info_table.get_item(order_id)
        amount = int(order_info['amount'])
        # PayPay API通信データを用意
        body = {
            "merchantPaymentId": order_id,
            "codeType": "ORDER_QR",
            "redirectUrl": f'{confirm_url}?transactionId=999999&orderId={order_id}',
            "redirectType":"WEB_LINK",
            "orderDescription":'Use Caseストア新宿店',
            "orderItems": [ {
                "name": '購入商品', \
                "category": 'item', \
                "quantity": 1, \
                "productId": 11, \
                "unitPrice": { "amount": amount, "currency": "JPY" } \
                } ],
            "amount": {
                "amount": amount,
                "currency": "JPY"
            },
        }
        api_response = client.Code.create_qr_code(body)
        
    except Exception as e:
        logger.exception('Occur Exception: %s', e)
        return utils.create_error_response('Error')

    response = utils.create_success_response(
        json.dumps(api_response))
    return response
