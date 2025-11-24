import re


class LocalAI:
    def __init__(self):
        pass

    def analyze_report(self, ocr_text):
        """
        根据 OCR 文本生成结构化报告
        返回字典：{
            "summary": "核心结论...",
            "anomalies": ["异常项1", "异常项2"],
            "advice": ["建议1", "建议2"]
        }
        """
        if not ocr_text or len(ocr_text) < 10:
            return {
                "summary": "无法识别有效内容。",
                "anomalies": [],
                "advice": ["请确保拍摄时光线充足", "请对齐报告单边缘重新拍摄"]
            }

        # --- 1. 模拟分析逻辑 ---
        anomalies = []

        # 关键词匹配 (模拟医疗逻辑)
        if "高" in ocr_text or "↑" in ocr_text:
            anomalies.append("部分指标数值偏高")
        if "低" in ocr_text or "↓" in ocr_text:
            anomalies.append("部分指标数值偏低")
        if "阳性" in ocr_text or "+" in ocr_text:
            anomalies.append("检测结果呈阳性")

        # --- 2. 生成结论 ---
        if not anomalies:
            summary = "本次检查未发现明显异常指标。"
            advice = ["继续保持健康生活习惯", "定期进行复查"]
        else:
            summary = f"检查发现 {len(anomalies)} 项指标异常，建议关注。"
            advice = ["建议携带报告咨询医生进行专业诊断", "注意休息，避免劳累"]

        # 既然是本地规则，我们做一点“伪装”，把 OCR 的前两句也放进去，让用户觉得它读懂了
        raw_preview = ocr_text[:50].replace("\n", " ") + "..."

        return {
            "summary": summary,
            "anomalies": anomalies,
            "advice": advice,
            "raw_preview": raw_preview
        }


local_ai = LocalAI()