from config import get_config
from features.base import feature_factory
from map import Map, FeatureStatus, Permission, DatabaseCollectionMap
from api.linebot_helper import LineBotHelper
from utils.error_handler import handle_exception
from flask import Blueprint, request, abort, current_app
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import (
    MessageEvent,
    PostbackEvent,
    FollowEvent,
    UnfollowEvent,
    TextMessageContent
)
from linebot.v3.messaging import TextMessage

linebot_app = Blueprint('linebot_app', __name__)

config = get_config()
configuration = config.configuration
line_handler = config.handler
firebaseService = config.firebaseService


@linebot_app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    current_app.logger.info("Request body: " + body)
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        current_app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

@line_handler.add(FollowEvent)
def handle_follow(event):
    try:
        LineBotHelper.show_loading_animation_(event)

        welcome_message = "歡迎使用本系統！"
        messages = [
            TextMessage(text=welcome_message)
        ]
        LineBotHelper.reply_message(event, messages)
    except Exception as e:
        handle_exception(e, admin_notification=True, event=event)

@line_handler.add(UnfollowEvent)
def handle_unfollow(event):
    try:
        pass
    except Exception as e:
        handle_exception(e, admin_notification=True, event=event)

@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    try:
        user_msg = event.message.text
        feature = Map.FEATURE.get(user_msg)

        if feature:
            LineBotHelper.show_loading_animation_(event)
            feature_status = config.feature.get(feature)

            match feature_status:
                case FeatureStatus.DISABLE:
                    return LineBotHelper.reply_message(event, [TextMessage(text='此功能尚未開放，敬請期待！')])
                case FeatureStatus.MAINTENANCE:
                    return LineBotHelper.reply_message(event, [TextMessage(text='此功能維護中，請見諒！')])
            feature_instance = feature_factory.get_feature(feature)
            if feature_instance:
                feature_instance.execute_message(event, request=request)
        
    except Exception as e:
        handle_exception(e, admin_notification=True, event=event)

@line_handler.add(PostbackEvent)
def handle_postback(event):
    try:
        postback_data = event.postback.data
        if 'richmenu' in postback_data:
            return
        LineBotHelper.show_loading_animation_(event)
        
        params = event.postback.params or {}
        if '=' in postback_data:
            params.update(dict(param.split('=') for param in postback_data.split('&')))
        feature_instance = feature_factory.get_feature(params.get('task'))
        if feature_instance:
            feature_instance.execute_postback(event, params=params)
    except Exception as e:
        handle_exception(e, admin_notification=True, event=event)