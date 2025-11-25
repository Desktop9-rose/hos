import re
import os
from PIL import Image, ImageFilter


class Desensitizer:
    def __init__(self):
        # 医疗敏感词库 (移植自 input_file_2.py)
        self.privacy_keywords = [
            "姓名", "性别", "年龄", "医院", "科室", "医生",
            "就诊号", "住院号", "病历号", "床号",
            "采样时间", "送检医生", "接收时间", "电话", "住址", "身份证"
        ]

    def desensitize_text(self, text):
        """文本脱敏：直接过滤掉包含敏感词的行"""
        if not text: return ""
        lines = text.split("\n")
        safe_lines = []
        for line in lines:
            # 如果行内包含任意敏感词，则跳过该行
            if not any(kw in line for kw in self.privacy_keywords):
                safe_lines.append(line)
        return "\n".join(safe_lines).strip()

    def blur_image_region(self, image_path, output_path, regions=None):
        # 图片打码逻辑保持不变，这里是安全的
        try:
            img = Image.open(image_path)
            w, h = img.size
            if not regions:
                blur_h = int(h * 0.18)  # 稍微加大一点范围
                regions = [(0, 0, w, blur_h)]

            blurred_img = img.copy()
            for (x, y, rw, rh) in regions:
                box = (int(x), int(y), int(x + rw), int(y + rh))
                crop = img.crop(box)
                blur = crop.filter(ImageFilter.GaussianBlur(radius=30))
                blurred_img.paste(blur, box)

            blurred_img.save(output_path, quality=85)
            return True if os.path.exists(output_path) else False
        except Exception as e:
            print(f"Blur Error: {e}")
            return False


desensitizer = Desensitizer()