import requests
import base64
import json
import os
import urllib3
from utils.config_loader import config_manager

# 禁用 SSL 警告 (防止 Android 端因证书验证慢导致请求失败)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CloudOCR:
    def __init__(self):
        pass

    def _get_token(self):
        """获取百度 Access Token"""
        api_key = config_manager.get("BAIDU_OCR", "API_KEY")
        secret_key = config_manager.get("BAIDU_OCR", "SECRET_KEY")

        if not api_key or not secret_key:
            print("❌ [CloudOCR] API KEY 或 SECRET KEY 未配置")
            return None

        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": api_key,
            "client_secret": secret_key
        }
        try:
            # 获取 Token 的请求通常很快，10秒超时足够
            resp = requests.get(url, params=params, timeout=10, verify=False)
            return resp.json().get("access_token")
        except Exception as e:
            print(f"❌ [CloudOCR] Token 获取失败: {e}")
            return None

    def recognize(self, image_path):
        """
        执行云端识别
        注意：为了防止 Android 端闪退，移除了 PIL 压缩逻辑，直接上传原图。
        """
        print(f"☁️ [CloudOCR] 开始识别: {image_path}")

        # 1. 检查文件是否存在
        if not image_path or not os.path.exists(image_path):
            return {"error": "找不到图片文件"}

        # 2. 获取 Token
        token = self._get_token()
        if not token:
            return {"error": "无法连接云端服务 (Token获取失败)"}

        # 3. 读取并编码图片 (不依赖 Pillow)
        try:
            with open(image_path, 'rb') as f:
                img_data = f.read()
            b64_data = base64.b64encode(img_data).decode('utf-8')
        except Exception as e:
            return {"error": f"读取图片失败: {str(e)}"}

        # 4. 准备请求数据
        api_url = config_manager.get("BAIDU_OCR", "OCR_API_URL")
        if not api_url:
            # 默认回退地址 (医疗检验报告)
            api_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/medical_report_detection"

        request_url = f"{api_url}?access_token={token}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "image": b64_data,
            "language_type": "CHN_ENG",
            "detect_direction": "true"
        }

        # 5. 发送请求
        try:
            # 因为上传的是原图，适当延长超时时间到 45秒
            timeout = config_manager.get_int("BAIDU_OCR", "TIMEOUT", 45)
            resp = requests.post(request_url, headers=headers, data=data, timeout=timeout, verify=False)
            result = resp.json()

            # 6. 解析结果
            if "words_result" in result:
                text_list = []
                for item in result["words_result"]:
                    # 尝试获取文字内容
                    w = item.get("words", "")
                    # 部分医疗接口可能返回 key: value 格式
                    if not w and "key" in item:
                        w = f"{item.get('key', '')}: {item.get('value', '')}"

                    if w:
                        text_list.append(w)

                final_text = "\n".join(text_list)
                if not final_text:
                    return {"error": "识别成功但无有效文字内容"}

                return final_text

            elif "error_msg" in result:
                return {"error": f"百度API报错: {result['error_msg']}"}

            return {"error": "未识别到有效文字"}

        except requests.exceptions.Timeout:
            return {"error": "网络请求超时，请检查网络状况"}
        except Exception as e:
            return {"error": f"网络请求异常: {str(e)}"}


# 单例实例
cloud_ocr = CloudOCR()