import pytesseract
from PIL import Image, ImageEnhance
import sys
import os
from kivy.utils import platform

# --- Tesseract 路径配置 ---
if sys.platform == 'win32':
    # 电脑端路径
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class LocalOCR:
    def __init__(self):
        pass

    def preprocess_image(self, image_path):
        try:
            img = Image.open(image_path)
            img = img.convert('L')
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2.0)
            return img
        except Exception as e:
            print(f"图像预处理失败: {e}")
            return None

    def extract_text(self, image_path):
        print(f"DEBUG [OCR]: 开始识别 {image_path}")

        # 1. 检查运行环境
        if platform == 'android':
            # ⚠️ 注意：在安卓上本地运行 Tesseract 非常复杂（需要交叉编译二进制文件）。
            # 为了保证 APK 能顺利运行不闪退，这里我们暂时返回模拟数据或提示。
            # 真正的商业项目这里会调用 百度/阿里 的云端 OCR API。
            print("DEBUG [OCR]: 检测到 Android 环境，本地引擎不可用。")
            return "（安卓端提示：本地 OCR 引擎未集成。\n请连接云端 API 或在电脑端测试本地功能。）\n\n模拟结果：\n白细胞：12.5↑ (偏高)\n红细胞：4.5 (正常)\n血小板：210 (正常)"

        # 2. 电脑端正常逻辑
        processed_img = self.preprocess_image(image_path)
        if not processed_img:
            return "图像处理失败"

        try:
            text = pytesseract.image_to_string(
                processed_img,
                lang='chi_sim+eng',
                config='--psm 6'
            )
            return text.strip() if text else "未识别到文字"

        except pytesseract.TesseractNotFoundError:
            return "错误：电脑未安装 Tesseract，无法识别。"
        except Exception as e:
            return f"识别出错: {str(e)}"


ocr_engine = LocalOCR()