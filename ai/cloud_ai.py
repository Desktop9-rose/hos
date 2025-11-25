import json
import re
from kivy.network.urlrequest import UrlRequest
from utils.config_loader import config_manager


class CloudAI:
    def __init__(self):
        self.callback = None

    def analyze(self, ocr_text, callback):
        """
        调用 DeepSeek (UrlRequest版)
        :param callback: func(result_dict)
        """
        self.callback = callback
        print("🧠 [CloudAI] 正在调用 AI...")

        api_key = config_manager.get("DEEPSEEK", "API_KEY")
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

        prompt = f"基于以下医疗报告文本（已脱敏），请简要解读。\n要求：\n1. 语言通俗。\n2. 格式强制如下：\n### 核心结论\n(一句话)\n### 异常指标\n(列出异常)\n### 生活建议\n(3条)\n\n报告内容：\n{ocr_text[:1500]}"

        # 构造 JSON body
        body = json.dumps({
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1
        })

        def on_success(req, result):
            try:
                content = result["choices"][0]["message"]["content"]
                self.callback(self._parse_result(content))
            except Exception as e:
                print(f"AI Parse Error: {e}")
                self.callback(self._get_fallback("AI 响应格式错误"))

        def on_fail(req, error):
            print(f"AI Network Error: {error}")
            self.callback(self._get_fallback("网络连接失败"))

        # 发送 POST
        UrlRequest(url, req_body=body, req_headers=headers, on_success=on_success, on_failure=on_fail, on_error=on_fail,
                   timeout=20)

    def _get_fallback(self, reason):
        return {
            "summary": f"解读失败 ({reason})",
            "anomalies": ["请检查网络"],
            "advice": ["请咨询医生"]
        }

    def _parse_result(self, text):
        text = re.sub(r'[:：]+', '：', text)
        text = re.sub(r'\*\*', '', text)
        result = {"summary": "暂无结论", "anomalies": [], "advice": []}

        blocks = re.split(r'###|\n\n', text)
        for block in blocks:
            block = block.strip()
            if "核心结论" in block:
                result["summary"] = block.replace("核心结论", "").replace("：", "").strip()[:100]
            elif "异常指标" in block:
                val = block.replace("异常指标", "").replace("：", "").strip()
                if val:
                    lines = [l.strip() for l in val.split('\n') if l.strip() and "无" not in l]
                    result["anomalies"] = lines[:5]
            elif "生活建议" in block:
                val = block.replace("生活建议", "").replace("：", "").strip()
                if val:
                    sugs = [s.strip() for s in re.split(r'[；;\n]', val) if len(s.strip()) > 3]
                    result["advice"] = sugs[:3]
        return result


cloud_ai = CloudAI()