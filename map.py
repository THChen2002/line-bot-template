from enum import Enum, IntEnum
import os

class FeatureStatus(Enum):
    """
    功能狀態
    """
    # 啟用
    ENABLE = 1
    # 維護
    MAINTENANCE = 2
    # 未開放
    DISABLE = 3

class Permission(IntEnum):
    """
    權限
    """
    # 一般使用者
    USER = 1
    # 工作人員
    STAFF = 2
    # 工作領導者
    LEADER = 3
    # 管理員
    ADMIN = 4

class LIFF(Enum):
    """
    LIFF
    """
    # Compact
    COMPACT = os.getenv('LIFF_ID_COMPACT')
    # Tall
    TALL = os.getenv('LIFF_ID_TALL')
    # Full
    FULL = os.getenv('LIFF_ID_FULL')
    # Admin
    ADMIN = os.getenv('LIFF_ID_ADMIN')

class Map:
    """
    其他Map
    """
    FEATURE = {
        
    }

class DatabaseCollectionMap:
    """
    Map資料庫Collection名稱
    """
    RICH_MENU = "rich_menu"
    LINE_FLEX = "line_flex"
    QUICK_REPLY = "quick_reply"
    USER = "users"