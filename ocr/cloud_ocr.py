import base64
import json
import os
from urllib.parse import urlencode
from kivy.network.urlrequest import UrlRequest
from utils.config_loader import config_manager


class CloudOCR:
    def __init__(self):
        self.callback = None

    def recognize(self, image_path, callback):
        """
        执行云端识别 (原生网络版)
        :param callback: func(text, error)
        """
        self.callback = callback
        print(f"☁️ [CloudOCR] 开始识别: {image_path}")

        if not image_path or not os.path.exists(image_path):
            self.callback(None, "找不到图片文件")
            return

        # 1. 读取图片 (二进制)
        try:
            with open(image_path, 'rb') as f:
                img_data = f.read()
            b64_data = base64.b64encode(img_data).decode('utf-8')
        except Exception as e:
            self.callback(None, f"读取图片失败: {str(e)}")
            return

        # 2. 获取 Token
        self._get_token(lambda token: self._start_ocr(token, b64_data))

    def _get_token(self, on_success):
        api_key = config_manager.get("BAIDU_OCR", "API_KEY")
        secret_key = config_manager.get("BAIDU_OCR", "SECRET_KEY")

        # 使用 params 拼接到 URL 中
        url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"

        def on_success_wrapper(req, result):
            # UrlRequest 自动解析 JSON
            if 'access_token' in result:
                on_success(result['access_token'])
            else:
                self.callback(None, f"Token获取失败: {result}")

        def on_fail(req, error):
            self.callback(None, "无法连接网络 (Token)")

        # 发送 GET 请求
        UrlRequest(url, on_success=on_success_wrapper, on_failure=on_fail, on_error=on_fail, timeout=10)

    def _start_ocr(self, token, b64_data):
        api_url = config_manager.get("BAIDU_OCR", "OCR_API_URL")
        if not api_url:
            api_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/medical_report_detection"

        url = f"{api_url}?access_token={token}"

        # 构造表单数据
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        body_dict = {
            'image': b64_data,
            'language_type': 'CHN_ENG',
            'detect_direction': 'true'
        }
        # 关键：手动编码 body
        body = urlencode(body_dict)

        def on_success(req, result):
            if "words_result" in result:
                text_list = []
                for item in result["words_result"]:
                    w = item.get("words", "")
                    # 兼容不同接口格式
                    if not w and "key" in item:
                        w = f"{item.get('key')}: {item.get('value')}"
                    if w: text_list.append(w)

                final_text = "\n".join(text_list) if text_list else "未识别到文字"
                self.callback(final_text, None)
            elif "error_msg" in result:
                self.callback(None, f"百度API报错: {result['error_msg']}")
            else:
                self.callback(None, "识别结果为空")

        def on_fail(req, error):
            self.callback(None, "无法连接网络 (OCR)")

        # 发送 POST 请求
        UrlRequest(url, req_body=body, req_headers=headers, on_success=on_success, on_failure=on_fail, on_error=on_fail,
                   timeout=45)


cloud_ocr = CloudOCR()