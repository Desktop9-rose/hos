import requests
import json
import re
from concurrent.futures import ThreadPoolExecutor
from utils.config_loader import config_manager
import urllib3

urllib3.disable_warnings()


class CloudAI:
    def __init__(self):
        pass

    def _parse_result(self, text):
        """解析 AI 返回的 Markdown 文本为结构化字典 (移植自 input_file_2.py)"""
        # 清理格式
        text = re.sub(r'[:：]+', '：', text)
        text = re.sub(r'\*\*', '', text)  # 去掉 markdown 加粗

        result = {
            "summary": "暂无核心结论",
            "anomalies": [],
            "advice": []
        }

        # 简单粗暴的分块解析
        blocks = re.split(r'###|\n\n', text)
        for block in blocks:
            block = block.strip()
            if "核心结论" in block:
                val = block.replace("核心结论", "").replace("：", "").strip()
                if val: result["summary"] = val[:100]
            elif "异常指标" in block:
                val = block.replace("异常指标", "").replace("：", "").strip()
                if val and "无" not in val:
                    result["anomalies"] = [line.strip() for line in val.split('\n') if line.strip()]
            elif "生活建议" in block:
                val = block.replace("生活建议", "").replace("：", "").strip()
                if val:
                    # 处理分号或换行分隔
                    sugs = re.split(r'[；;\n]', val)
                    result["advice"] = [s.strip() for s in sugs if len(s.strip()) > 3][:4]

        return result

    def _call_deepseek(self, text):
        api_key = config_manager.get("DEEPSEEK", "API_KEY")
        if not api_key: return None

        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

        # Prompt 保持与 input_file_2.py 一致
        prompt = f"""基于以下医疗报告文本（已脱敏），请简要解读。
        要求：
        1. 语言通俗，不要用专业术语。
        2. 格式强制如下（不要输出其他废话）：
        ### 核心结论
        (一句话概括)
        ### 异常指标
        (列出异常项，无则写无)
        ### 生活建议
        (3条建议，分号分隔)

        报告内容：
        {text[:1500]}"""  # 截断防止超长

        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1
        }

        try:
            resp = requests.post(url, json=data, headers=headers, timeout=20, verify=False)
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"DeepSeek Error: {e}")
        return None

    def _call_tongyi(self, text):
        api_key = config_manager.get("TONGYI", "API_KEY")
        if not api_key: return None

        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

        prompt = f"你是一个医疗助手。请解读以下报告：\n{text[:1500]}\n请按格式输出：\n### 核心结论\n...\n### 异常指标\n...\n### 生活建议\n..."

        data = {
            "model": "qwen-turbo",
            "input": {"messages": [{"role": "user", "content": prompt}]},
            "parameters": {"result_format": "message"}
        }

        try:
            resp = requests.post(url, json=data, headers=headers, timeout=20, verify=False)
            if resp.status_code == 200:
                return resp.json()["output"]["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Tongyi Error: {e}")
        return None

    def analyze(self, ocr_text):
        """并发调用双模型"""
        print("🧠 [CloudAI] 正在调用双模型...")

        with ThreadPoolExecutor(max_workers=2) as executor:
            future_ds = executor.submit(self._call_deepseek, ocr_text)
            future_ty = executor.submit(self._call_tongyi, ocr_text)

            res_ds = future_ds.result()
            res_ty = future_ty.result()

        # 简单交叉验证策略：优先用 DeepSeek，失败则用通义
        final_raw = res_ds if res_ds else res_ty

        if not final_raw:
            return {
                "summary": "网络繁忙，AI 暂时无法响应",
                "anomalies": ["请稍后重试"],
                "advice": ["建议咨询线下医生"]
            }

        return self._parse_result(final_raw)


cloud_ai = CloudAI()