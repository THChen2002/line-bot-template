from config import get_config
from map import DatabaseCollectionMap, Permission, LIFF
from flask import Blueprint, request, render_template, jsonify
from utils.error_handler import handle_exception

admin_app = Blueprint('admin_app', __name__)

config = get_config()
firebaseService = config.firebaseService

@admin_app.route('/auth', methods=['POST'])
def check_admin():
    """驗證 admin 身份"""
    try:
        user_id = request.json.get('userId')
        if not user_id:
            return jsonify({'success': False, 'message': '缺少 userId'}), 400
        
        user = firebaseService.get_data(DatabaseCollectionMap.USER, user_id)
        if user and user.get('permission') >= Permission.LEADER:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': '權限不足'}), 403
            
    except Exception as e:
        return handle_exception(e)

@admin_app.route('/', methods=['GET'])
def admin():
    liff_id = LIFF.ADMIN.value

    return render_template('admin/index.html', **locals())
