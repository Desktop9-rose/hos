from PIL import Image, ImageEnhance
import sys
from kivy.utils import platform

# ---------------------------------------------------------
# 关键修复：条件导入 pytesseract
# 在安卓上不要尝试导入它，否则会直接报 ModuleNotFoundError 闪退
# ---------------------------------------------------------
pytesseract = None
if platform != 'android':
    try:
        import pytesseract

        if sys.platform == 'win32':
            # 电脑端 Tesseract 路径 (请根据实际安装位置修改)
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    except ImportError:
        print("警告: 未安装 pytesseract，本地OCR功能在电脑上将不可用")


class LocalOCR:
    def preprocess_image(self, image_path):
        try:
            img = Image.open(image_path).convert('L')
            return ImageEnhance.Contrast(img).enhance(2.0)
        except Exception as e:
            print(f"预处理失败: {e}")
            return None

    def extract_text(self, image_path):
        print(f"DEBUG [OCR]: 开始识别 {image_path}")

        # 1. 安卓环境处理 (直接返回演示数据，防止崩溃)
        if platform == 'android':
            print("DEBUG [OCR]: Android 环境检测到，跳过本地引擎。")
            return "（安卓端演示数据）\n白细胞：12.5↑ (偏高)\n红细胞：4.5 (正常)\n血小板：210 (正常)\n\n(注: 真实环境需对接百度/阿里API)"

        # 2. 电脑环境处理
        if not pytesseract:
            return "错误：未检测到 pytesseract 模块，无法进行本地识别。"

        processed_img = self.preprocess_image(image_path)
        if not processed_img:
            return "图像处理失败"

        try:
            text = pytesseract.image_to_string(processed_img, lang='chi_sim+eng', config='--psm 6')
            return text.strip() if text else "未识别到文字"
        except pytesseract.TesseractNotFoundError:
            return "错误：电脑未安装 Tesseract 软件。"
        except Exception as e:
            return f"识别出错: {e}"


ocr_engine = LocalOCR()