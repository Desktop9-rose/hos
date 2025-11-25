import requests
import base64
import io
import json
from PIL import Image
from utils.config_loader import config_manager
import urllib3

# 禁用 SSL 警告 (Android 上有时证书验证会慢)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CloudOCR:
    def __init__(self):
        pass

    def _compress_image(self, image_path):
        """深度压缩图片 (移植自 input_file_2.py)"""
        try:
            quality = config_manager.get_int("BAIDU_OCR", "IMAGE_COMPRESS_QUALITY", 60)
            with Image.open(image_path) as img:
                # 1. 调整尺寸 (最大宽 1000px)
                max_width = 1000
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

                # 2. 转 RGB
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                # 3. 压缩到内存
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG', quality=quality, optimize=True)
                return img_byte_arr.getvalue()
        except Exception as e:
            print(f"⚠️ [CloudOCR] 压缩失败，使用原图: {e}")
            with open(image_path, 'rb') as f:
                return f.read()

    def _get_token(self):
        """获取百度 Access Token"""
        api_key = config_manager.get("BAIDU_OCR", "API_KEY")
        secret_key = config_manager.get("BAIDU_OCR", "SECRET_KEY")

        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": api_key,
            "client_secret": secret_key
        }
        try:
            resp = requests.get(url, params=params, timeout=10, verify=False)
            return resp.json().get("access_token")
        except Exception as e:
            print(f"❌ [CloudOCR] Token 获取失败: {e}")
            return None

    def recognize(self, image_path):
        """执行云端识别"""
        print(f"☁️ [CloudOCR] 开始识别: {image_path}")

        # 1. 获取 Token
        token = self._get_token()
        if not token:
            return {"error": "无法连接云端服务 (Token失败)"}

        # 2. 处理图片
        img_data = self._compress_image(image_path)
        b64_data = base64.b64encode(img_data).decode('utf-8')

        # 3. 调用 API
        api_url = config_manager.get("BAIDU_OCR", "OCR_API_URL")
        request_url = f"{api_url}?access_token={token}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "image": b64_data,
            "language_type": "CHN_ENG",
            "detect_direction": "true"
        }

        try:
            timeout = config_manager.get_int("BAIDU_OCR", "TIMEOUT", 30)
            resp = requests.post(request_url, headers=headers, data=data, timeout=timeout, verify=False)
            result = resp.json()

            # 4. 解析结果 (提取 words_result)
            if "words_result" in result:
                text_list = []
                for item in result["words_result"]:
                    # 百度医疗接口通常返回 location, words 等
                    # 这里做通用处理，如果是医疗接口可能包含 key/value
                    w = item.get("words", "")
                    if not w and "key" in item:  # 适配部分医疗结构化接口
                        w = f"{item.get('key', '')}: {item.get('value', '')}"
                    if w:
                        text_list.append(w)
                return "\n".join(text_list)

            elif "error_msg" in result:
                return {"error": f"百度API错误: {result['error_msg']}"}

            return {"error": "未识别到有效文字"}

        except Exception as e:
            return {"error": f"网络请求异常: {str(e)}"}


cloud_ocr = CloudOCR()