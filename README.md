# LINE Bot Template

This project is a Flask template for building LINE Bots, featuring integration with the LINE Messaging API, LIFF (LINE Front-end Framework), and an administrative dashboard.

## Project Architecture

```
line-bot-template/
├── app.py                  # Main Application Entry
├── config.py               # Configuration Management
├── map.py                  # Constants and Enums
├── linebot_app.py          # LINE Bot Module
├── liff_app.py             # LIFF Web App Module
├── admin_app.py            # Admin Dashboard Module
├── features/               # Feature Modules Directory
│   ├── __init__.py
│   └── base.py             # Feature Base Class and Factory Pattern
├── api/                    # API Service Layer
│   ├── firebase.py         # Firebase Service
│   ├── linebot_helper.py   # LINE Bot Helper
│   ├── liff_helper.py      # LIFF Helper
│   ├── oauth_helper.py     # OAuth Authentication Helper
│   └── spreadsheet.py      # Google Sheets Service
├── utils/                  # Utility Classes
│   ├── error_handler.py    # Error Handling
│   └── utils.py            # Common Utilities
├── templates/              # Template Files
│   ├── admin/              # Admin Dashboard Templates
│   ├── app/                # Main App Templates
│   ├── liff/               # LIFF Templates
│   └── http/               # HTTP Error Page Templates
├── static/                 # Static Resources
│   ├── css/
│   └── js/
└── requirements.txt        # Python Dependencies
```

## 🚀 Core Features

### 1. LINE Bot Features
- **Event Handling**: Support for Follow, Unfollow, Message, Postback events
- **Modular Architecture**: Plugin-based feature architecture using Factory Pattern
- **Status Management**: Feature enable/disable/maintenance status control
- **Error Handling**: Unified exception handling and notification system

### 2. LIFF Web Application
- **Multi-size Support**: Compact, Tall, Full LIFF sizes
- **Dynamic Routing**: Dynamic LIFF ID loading based on size parameters

### 3. Admin Dashboard
- **Permission Management**: Multi-level permission control (USER/STAFF/LEADER/ADMIN)
- **User Management**: Firebase-based user data management
- **System Monitoring**: System status and error monitoring

### 4. Data Services
- **Firebase**: User data and system configuration storage
- **Google Sheets**: Data export and reporting functionality
- **LINE API**: Message sending and user interaction

## 🛠️ Technology Stack

- **Backend Framework**: Flask 3.0.0
- **LINE Bot SDK**: line-bot-sdk 3.17.1
- **Database**: Firebase Admin SDK 6.5.0
- **Cloud Services**: Google Sheets API (pygsheets 2.0.6)
- **Frontend**: HTML/CSS/JavaScript/jQuery (LIFF)

## 📋 Environment Requirements

### Required Environment Variables
```bash
# LINE Bot Configuration
CHANNEL_SECRET=your_channel_secret
CHANNEL_ACCESS_TOKEN=your_channel_access_token

# LIFF ID Configuration
LIFF_ID_COMPACT=your_compact_liff_id
LIFF_ID_TALL=your_tall_liff_id
LIFF_ID_FULL=your_full_liff_id
LIFF_ID_ADMIN=your_admin_liff_id

# Google Services
GDRIVE_API_CREDENTIALS=your_google_service_account_json
SPREADSHEET_URL=your_google_spreadsheet_url

# Firebase Configuration
FIREBASE_CREDENTIALS=your_firebase_service_account_json
```

### LIFF Configuration
- **Endpoint URL**: Set to `https://your-domain.com/liff/<size>` in LINE Developers Console
- **Admin Endpoint URL**: Set to `https://your-domain.com/admin/` in LINE Developers Console
- **LIFF URLs**: Configure for each size (compact/tall/full/admin) in LINE Developers Console

## 🚀 Installation and Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd line-bot-template
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

#### Option 1: Using .env file (Recommended)
Create a `.env` file in the project root:
```bash
# .env
CHANNEL_SECRET=your_channel_secret
CHANNEL_ACCESS_TOKEN=your_channel_access_token
SPREADSHEET_URL=your_google_spreadsheet_url
FIREBASE_CREDENTIALS=your_firebase_service_account_json
GDRIVE_API_CREDENTIALS=your_google_service_account_json
LIFF_ID_COMPACT=your_compact_liff_id
LIFF_ID_TALL=your_tall_liff_id
LIFF_ID_FULL=your_full_liff_id
LIFF_ID_ADMIN=your_admin_liff_id
```

Install python-dotenv:
```bash
pip install python-dotenv
```

#### Option 2: Export environment variables
```bash
export CHANNEL_SECRET="your_channel_secret"
export CHANNEL_ACCESS_TOKEN="your_channel_access_token"
# ... set other required environment variables
```

### 4. Run Application
```bash
python app.py
```

## 📁 Core Modules

### Configuration Management (`config.py`)
- Singleton pattern for global configuration management
- Environment variable validation and loading
- LINE Bot, Firebase, Google Sheets service initialization

### Feature Factory (`features/base.py`)
- Abstract base class `Feature` defines feature interface
- `FeatureFactory` implements plugin-based feature registration
- Decorator `@register_feature` simplifies feature registration

### Routing Structure
- `/` - Main page
- `/callback` - LINE Bot Webhook
- `/liff/<size>` - LIFF dynamic size pages (compact/tall/full)
- `/admin/` - Admin dashboard

### LIFF URLs
- **Admin**: `https://liff.line.me/<liff_id_admin>/admin/`
- **LIFF Pages**: `https://liff.line.me/<liff_id>/<route>` (compact/tall/full)

### Permission System
```python
class Permission(IntEnum):
    USER = 1      # Regular User
    STAFF = 2     # Staff Member
    LEADER = 3    # Team Leader
    ADMIN = 4     # Administrator
```

### Feature Status Management
```python
class FeatureStatus(Enum):
    ENABLE = 1        # Enabled
    MAINTENANCE = 2   # Under Maintenance
    DISABLE = 3       # Disabled
```

## 🔧 Development Guide

### Adding New Feature Modules
1. Create new feature class in `features/` directory
2. Inherit from `Feature` base class and implement required methods
3. Use `@register_feature` decorator to register the feature
4. Add feature mapping in `map.py` `Map.FEATURE`

### Example Feature Module
```python
from features.base import register_feature, Feature
from linebot.v3.messaging import TextMessage

@register_feature('hello')
class HelloFeature(Feature):
    def execute_message(self, event, **kwargs):
        messages = [TextMessage(text="Hello!")]
        LineBotHelper.reply_message(event, messages)
    
    def execute_postback(self, event, **kwargs):
        # Handle postback events
        pass
```

### LIFF Page Example
```python
@liff_app.route('/<size>/example', methods=['GET'])
def example_page(size):
    liff_id = get_liff_id(size)
    return render_template('liff/example.html', liff_id=liff_id)
```

### Error Handling
- Use `utils.error_handler.handle_exception()` for unified exception handling
- Support admin notification and JSON response modes
- Automatic error logging

## 📊 Database Structure

### Firebase Collections
- `users` - User data
- `rich_menu` - Rich menu configuration
- `line_flex` - Flex Message templates
- `quick_reply` - Quick reply settings

## 🔒 Security

- LINE Webhook signature verification
- Environment variable sensitive information protection
- Multi-level permission control
- Error information filtering

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

We welcome issues and pull requests to improve this project.

## 📞 Support

For questions or suggestions, please contact us through:
- Submit GitHub Issue
- Send email to project maintainers