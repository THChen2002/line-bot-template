from config import get_config
from map import LIFF
from flask import Blueprint, request, render_template, jsonify, abort
from utils.error_handler import handle_exception

liff_app = Blueprint('liff_app', __name__)

config = get_config()
firebaseService = config.firebaseService

def get_liff_id(size: str, default_to_tall: bool = True) -> str:
    """
    Get LIFF ID based on size parameter
    Args:
        size (str): LIFF size (FULL, TALL, COMPACT)
        default_to_tall (bool): If True, returns TALL size when invalid. If False, raises 404
    Returns:
        str: LIFF ID
    """
    if size.upper() in [liff_type.name for liff_type in LIFF]:
        return getattr(LIFF, size.upper()).value
    if default_to_tall:
        return LIFF.TALL.value
    abort(404)

# ----------------LIFF 動態尺寸跳轉用頁面 Start----------------

@liff_app.route('/<size>', methods=['GET'])
def liff_size(size):
    liff_id = get_liff_id(size, default_to_tall=False)
    return render_template('liff/liff.html', liff_id=liff_id)

# -----------------LIFF 動態尺寸跳轉用頁面 End------------------

# -------------LIFF 頁面(根據需求設定不同大小) Start-------------

# -------------------------範例 Start-------------------------
# @liff_app.route('/<size>/example', methods=['GET'])
# def example(size):
#     liff_id = get_liff_id(size)
#     return render_template('liff/example.html', **locals())

# @liff_app.route('/example', methods=['POST'])
# def example_post():
#     try:
#         data = request.form.to_dict()

#         return jsonify({'success': True, 'message': '處理成功'})
#     except Exception as e:
#         return handle_exception(e, admin_notification=True, return_json=True)
# --------------------------範例 End--------------------------

# --------------LIFF 頁面(根據需求設定不同大小) End--------------
