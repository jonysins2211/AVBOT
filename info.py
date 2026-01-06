import re
from os import environ, getenv
from typing import Set, Optional, List, Dict
from Script import script  # Custom script file with caption & other settings

# 🚀 Bot Session and Token Information
SESSION = environ.get('SESSION', 'Webavbot')  # Pyrogram client session name

API_ID = int(environ.get('API_ID', '16013849'))  # Telegram API ID
API_HASH = environ.get('API_HASH', 'c8686adc1a0c7cd17f2201c40123ce91')  # Telegram API Hash
BOT_TOKEN = environ.get('BOT_TOKEN', '672782:AAE3VrD2SewKmu6ytwU4H1vRtfc')  # Telegram Bot Token

# 👑, Channels & Logs
BIN_CHANNEL = int(environ.get("BIN_CHANNEL", '-1003062906567'))  # File storage channel
LOG_CHANNEL = int(environ.get("LOG_CHANNEL", '-1003062906567'))  # General log channel
PREMIUM_LOGS = int(environ.get("PREMIUM_LOGS", '-1003062906567'))  # Premium user actions log
VERIFIED_LOG = int(environ.get('VERIFIED_LOG', '-1003062906567'))  # Verified user actions log
SUPPORT_GROUP = int(environ.get("SUPPORT_GROUP", "-1003062906567"))

# add admin IDs 11111 2222 3333 and add auth channel IDs -100XXX -100XXX -100XXX
ADMINS = list(map(int, environ.get('ADMINS', '949657126').split()))  # List of admin user IDs
AUTH_CHANNEL = list(map(int, environ.get("AUTH_CHANNEL", "-1001547011153").split()))  # Allowed channels for authorization

# username add without @
OWNER_USERNAME = environ.get("OWNER_USERNAME", 'MLADMINBOT')  # Owner's username
BOT_USERNAME = environ.get("BOT_USERNAME", 'MLFILETOLINKBOT')  # Bot's username

# 🔗 Channel & Support Links
CHANNEL = environ.get('CHANNEL', 'https://t.me/MOVIE_LOVERZZ')  # Updates channel
SUPPORT = environ.get('SUPPORT', 'https://t.me/AV_SUPRT_GROUP')  # Support group
HOW_TO_VERIFY = environ.get('HOW_TO_VERIFY', 'https://t.me/ML_FILES/17')  # Verification guide link
HOW_TO_OPEN = environ.get('HOW_TO_OPEN', 'https://t.me/ML_FILES/17')  # File access guide link

# ✅ Feature Toggles (True/False)
VERIFY = environ.get("VERIFY", True)  # Enable user verification
FSUB = environ.get("FSUB", True)  # Force Subscribe feature
ENABLE_LIMIT = environ.get("ENABLE_LIMIT", True)  # Enable file limits
BATCH_VERIFY = environ.get("BATCH_VERIFY", True)  # Verify files in batch
IS_SHORTLINK = bool(environ.get('IS_SHORTLINK', False))  # Enable channel shortlink creation
MAINTENANCE_MODE = environ.get("MAINTENANCE_MODE", False)  # Put bot in maintenance
PROTECT_CONTENT = environ.get('PROTECT_CONTENT', False)  # Enable content protection
PUBLIC_FILE_STORE = environ.get('PUBLIC_FILE_STORE', False)  # Public or private file visibility
BATCH_PROTECT_CONTENT = environ.get('BATCH_PROTECT_CONTENT', False)  # Batch file protection

# 🔗 Shortlink Configuration
SHORTLINK_URL = environ.get('SHORTLINK_URL', 'arolinks.com')  # Shortener site
SHORTLINK_API = environ.get('SHORTLINK_API', 'b45f8f81a9b97173588484df25715cb97b4d3fb1')  # API key for shortlink

# 💾 MongoDB Connection Information
DB_URL = environ.get('DATABASE_URI', "mongodb+srv://primebaby11220:TuGa0I5ZsiC8mp5A@cluster0.df4rivj.mongodb.net/?retryWrites=true&w=majority")  # MongoDB connection URI
DB_NAME = environ.get('DATABASE_NAME', "primebaby11220")  # MongoDB database name

# 📸 all Media (Images)
QR_CODE = environ.get('QR_CODE', 'https://i.ibb.co/Vcktd8h4/photo-2026-01-06-15-59-03-7592278796548440092.jpg')  # QR Code image
VERIFY_IMG = environ.get("VERIFY_IMG", "https://graph.org/file/1669ab9af68eaa62c3ca4.jpg")  # Verify success image
AUTH_PICS = environ.get('AUTH_PICS', 'https://envs.sh/AwV.jpg')  # Auth step image
PICS = environ.get('PICS', 'https://graph.org/file/a319f6b9ce3b993c6e22f.jpg')  # Default info image
FILE_PIC = environ.get('FILE_PIC', 'https://graph.org/file/a319f6b9ce3b993c6e22f.jpg') # file image 

# 📝 File Captions
FILE_CAPTION = environ.get('FILE_CAPTION', f"{script.CAPTION}")  # Caption for single file
BATCH_FILE_CAPTION = environ.get('BATCH_FILE_CAPTION', f"{script.CAPTION}")  # Caption for batch files
CHANNEL_FILE_CAPTION = environ.get('CHANNEL_FILE_CAPTION', f"{script.CAPTION}")  # Caption for channel posts

# ⏱️ Time & Rate Limit Settings
PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # Ping interval in seconds (20 minutes)
SLEEP_THRESHOLD = int(getenv('SLEEP_THRESHOLD', '60'))  # Threshold for sleep delay
RATE_LIMIT_TIMEOUT = int(environ.get("RATE_LIMIT_TIMEOUT", "600"))  # Rate limit time (10 mins)
MAX_FILES = int(environ.get("MAX_FILES", "4"))  # Max files allowed per user
VERIFY_EXPIRE = int(environ.get('VERIFY_EXPIRE', 28800))  # Time (in hours) after which verification expires

# ⚙️ Worker Configuration
WORKERS = int(getenv('WORKERS', '20'))  # Number of async workers
MULTI_CLIENT = True  # Enable multi-client handling (if needed)

# 🔧 App/Heroku Configuration
name = str(environ.get('name', 'avbotz'))  # Project name
APP_NAME = None
if 'DYNO' in environ:
    ON_HEROKU = True
    APP_NAME = str(getenv('APP_NAME'))  # Heroku app name (optional)
else:
    ON_HEROKU = False

# 🌐 Server Settings
PORT = int(getenv('PORT', '8087'))  # Port for web server
NO_PORT = str(getenv("NO_PORT", False)).lower() in ("true", "1", "yes")  # Disable port in URL
HAS_SSL = str(getenv("HAS_SSL", True)).lower() in ("true", "1", "yes")  # Use HTTPS if True
BIND_ADDRESS = getenv("WEB_SERVER_BIND_ADDRESS", "127.0.0.1")  # Server bind address
FQDN = getenv("FQDN", "https://movie-loverz-bot2-653efadac3bd.herokuapp.com/") or BIND_ADDRESS  # Full domain name or fallback to bind address
PORT_SEGMENT = "" if NO_PORT else f":{PORT}/"  # Port in URL if not disabled
PROTOCOL = "https" if HAS_SSL else "http"  # Protocol for URL
URL = f"https://movie-loverz-bot2-653efadac3bd.herokuapp.com/"  # Final generated base URL
