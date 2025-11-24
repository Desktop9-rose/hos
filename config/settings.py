import os

# --- 路径配置 ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'app_data.db')
FONT_PATH = os.path.join(BASE_DIR, 'assets', 'fonts', 'NotoSansSC-Bold.otf') # 请确保下载此字体

# --- 老年友好 UI 规范 ---
# 字体大小（sp单位适配屏幕密度）
FONT_SIZE_TITLE = "36sp"
FONT_SIZE_LARGE = "32sp"
FONT_SIZE_NORMAL = "28sp"
FONT_SIZE_SMALL = "24sp"

# 颜色主题 (KivyMD 格式)
THEME_STYLE = "Light"         # 亮色模式，高对比度
PRIMARY_PALETTE = "Teal"      # 蓝绿色，沉稳清晰
ACCENT_PALETTE = "Red"        # 红色用于强调异常/重要操作

# --- 默认应用配置 ---
DEFAULT_CONFIG = {
    "mode": "local",          # local=本地模式, cloud=云端模式
    "font_scale": 1.0,        # 字体缩放比例
    "voice_speed": "slow",    # 语速：slow, normal
    "dialect": "mandarin",    # 方言：mandarin, sichuan, cantonese
    "agreed_disclaimer": 0    # 是否同意免责声明
}