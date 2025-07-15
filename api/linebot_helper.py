from config import get_config
from map import DatabaseCollectionMap
from utils.utils import replace_variable
from linebot.v3.messaging import (
    ApiClient,
    ApiException,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
    MulticastRequest,
    PushMessageRequest,
    RichMenuRequest,
    URIAction,
    MessageAction,
    PostbackAction,
    RichMenuSwitchAction,
    CreateRichMenuAliasRequest,
    QuickReply,
    QuickReplyItem,
    ShowLoadingAnimationRequest,
    ValidateMessageRequest,
    SetWebhookEndpointRequest,
    RichMenuBulkLinkRequest,
    RichMenuBulkUnlinkRequest,
    RichMenuBatchRequest,
    RichMenuBatchLinkOperation,
    RichMenuBatchUnlinkOperation,
    RichMenuBatchUnlinkAllOperation
)
import requests
import json

config = get_config()
configuration = config.configuration
firebaseService = config.firebaseService

class LineBotHelper:
    @staticmethod
    def get_user_info(user_id: str) -> dict:
        """獲取指定用戶的個人資料資訊。
        
        Args:
            user_id (str): LINE 用戶的 ID
            
        Returns:
            dict: 包含用戶資訊的字典
        """
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            return line_bot_api.get_profile(user_id).to_dict()
    
    @staticmethod
    def show_loading_animation_(event, time: int=10):
        """
        顯示載入動畫
        """
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.show_loading_animation(
                ShowLoadingAnimationRequest(chatId=event.source.user_id, loadingSeconds=time)
            )
        
    @staticmethod
    def reply_message(event, messages: list):
        """
        回覆多則訊息
        """
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            # 為了避免回覆訊息時發生錯誤（通常是Flex string解析異常），先檢查訊息是否合法
            line_bot_api.validate_reply(ValidateMessageRequest(messages=messages))
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=messages
                )
            )

    @staticmethod
    def multicast_message(user_ids: list, messages: list):
        """
        推播多則訊息給多位user
        """
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.multicast_with_http_info(
                MulticastRequest(
                    to=user_ids,
                    messages=messages
                )
            )

    @staticmethod
    def push_message(user_id: str, messages: list):
        """
        推播多則訊息給一位user
        """
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.push_message_with_http_info(
                PushMessageRequest(
                    to=user_id,
                    messages=messages
                )
            )
    
    @staticmethod
    def create_action(action: dict):
        """Returns
        Action: action 物件
        """
        if action['type'] == 'uri':
            return URIAction(uri=action.get('uri'))
        elif action['type'] == 'message':
            return MessageAction(text=action.get('text'), label=action.get('label'))
        elif action['type'] == 'postback':
            return PostbackAction(data=action.get('data'), label=action.get('label'), display_text=action.get('displayText'))
        elif action['type'] == 'richmenuswitch':
            return RichMenuSwitchAction(
                rich_menu_alias_id=action.get('richMenuAliasId'),
                data=action.get('data')
            )
        else:
            raise ValueError('Invalid action type')

class WebhookHelper:
    @staticmethod
    def get_webhook_url():
        """
        取得 LINE Bot 的 Webhook URL
        """
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            response = line_bot_api.get_webhook_endpoint()
            return response.endpoint
    
    @staticmethod
    def set_webhook_url(webhook_url: str):
        """
        設定 LINE Bot 的 Webhook URL
        """
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            try:
                line_bot_api.set_webhook_endpoint(
                    SetWebhookEndpointRequest(
                        endpoint=webhook_url
                    )
                )
            except ApiException as e:
                raise ValueError(f"Failed to set webhook URL: {e}")
    
    @staticmethod
    def test_webhook_url():
        """
        測試 LINE Bot 的 Webhook URL 是否有效
        """
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            try:
                return line_bot_api.test_webhook_endpoint().to_dict()
            except ApiException as e:
                raise ValueError(f"Webhook URL test failed: {e}")

class RichMenuHelper:
    @staticmethod
    def set_rich_menu_image_(rich_menu_id, image_url):
        """
        設定圖文選單的圖片
        """
        with ApiClient(configuration) as api_client:
            line_bot_blob_api = MessagingApiBlob(api_client)
            response = requests.get(image_url)
            if response.status_code != 200:
                raise ValueError('Invalid image url')
            else:
                line_bot_blob_api.set_rich_menu_image(
                    rich_menu_id=rich_menu_id,
                    body=response.content,
                    _headers={'Content-Type': 'image/png'}
                )

    @staticmethod
    def create_rich_menu_alias_(alias_id, rich_menu_id):
        """
        建立圖文選單的alias
        """
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.create_rich_menu_alias(
                CreateRichMenuAliasRequest(
                    rich_menu_alias_id=alias_id,
                    rich_menu_id=rich_menu_id
                )
            )

    @staticmethod
    def create_rich_menu_(alias_id):
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            # 設定 rich menu image
            rich_menu_str = firebaseService.get_data(
                DatabaseCollectionMap.RICH_MENU,
                alias_id
            ).get('richmenu')
            rich_menu_id = line_bot_api.create_rich_menu(
                rich_menu_request=RichMenuRequest.from_json(rich_menu_str)
            ).rich_menu_id
            rich_menu_url = firebaseService.get_data(
                DatabaseCollectionMap.RICH_MENU,
                alias_id
            ).get('image_url')
            __class__.set_rich_menu_image_(rich_menu_id, rich_menu_url)
            __class__.create_rich_menu_alias_(alias_id, rich_menu_id)
            return rich_menu_id

    #-----------------以下為設定rich menu的程式-----------------

    @staticmethod
    def set_richmenu():
        """
        設定rich menu，並將alias id為page1的rich menu設為預設
        """
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            richmenus = firebaseService.get_collection_data(DatabaseCollectionMap.RICH_MENU)
            for richmenu in richmenus:
                richmenu_id = RichMenuHelper.create_rich_menu_(richmenu.get('alias_id'))
                firebaseService.update_data(
                    DatabaseCollectionMap.RICH_MENU,
                    richmenu.get('alias_id'),
                    {'richmenu_id': richmenu_id}
                )
                if richmenu.get('alias_id') == 'page1':
                    line_bot_api.set_default_rich_menu(richmenu_id)

    @staticmethod
    def delete_all_richmenu():
        """
        刪除所有圖文選單和Alias
        """
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            richmenu_list = line_bot_api.get_rich_menu_list()
            richmenu_alias_list = line_bot_api.get_rich_menu_alias_list()
            for richmenu in richmenu_alias_list.aliases:
                line_bot_api.delete_rich_menu_alias(richmenu.rich_menu_alias_id)
            for richmenu in richmenu_list.richmenus:
                line_bot_api.delete_rich_menu(richmenu.rich_menu_id)


#         # 取消圖文選單連結使用者
#         line_bot_api.unlink_rich_menu_id_from_user("Uxxxxxxx")
#         line_bot_api.unlink_rich_menu_id_from_users(
#             RichMenuBulkUnlinkRequest(
#                 user_ids=user_ids
#             )
#         )

#         # 取得使用者的圖文選單ID
#         rich_menu_id = line_bot_api.get_rich_menu_id_of_user("Uxxxxxxx")

#         # 批次替換或取消連結圖文選單
#         line_bot_api.rich_menu_batch(
#             RichMenuBatchRequest(
#                 operations=[
#                     RichMenuBatchLinkOperation(
#                         var_from="richmenu-xxxxxxx", # 從哪個圖文選單ID
#                         to="richmenu-xxxxxxxx" # 到哪個圖文選單ID
#                     ),
#                     RichMenuBatchUnlinkOperation(
#                         var_from="richmenu-xxxxxxx", # 從哪個圖文選單ID
#                     ),
#                     RichMenuBatchUnlinkAllOperation(),
#                 ]
#             )
#         )
    
class QuickReplyHelper:
    @staticmethod
    def create_quick_reply(quick_reply_data: list[dict]):
        """Returns
        QuickReply: 快速回覆選項
        """
        return QuickReply(
            items=[QuickReplyItem(action=LineBotHelper.create_action(json.loads(item))) for item in quick_reply_data]
        )
    
class FlexMessageHelper:
    @staticmethod
    def create_carousel_bubbles(items: list[dict], line_flex_json: json):
        """ Returns 根據 items 生成並替換 carousel bubbles的變數
        json: carousel bubbles
        """
        bubbles = []
        for item in items:
            # 複製原始的 bubble
            new_bubble = line_flex_json['contents'][0].copy()
            # 在新 bubble 中進行變數替換
            new_bubble = LineBotHelper.replace_variable(json.dumps(new_bubble), item)
            
            # 將新 bubble 添加到 bubbles 中
            bubbles.append(json.loads(new_bubble))
        
        # 將生成的 bubbles 放回 line_flex_json 中
        line_flex_json['contents'] = bubbles

        return line_flex_json