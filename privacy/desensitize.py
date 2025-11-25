import re
import os

# 尝试导入 Pillow，如果失败则跳过图片处理功能
try:
    from PIL import Image, ImageFilter

    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False
    print("⚠️ [Privacy] Pillow 未安装，图片打码功能已禁用")


class Desensitizer:
    def __init__(self):
        self.privacy_keywords = [
            "姓名", "性别", "年龄", "医院", "科室", "医生",
            "就诊号", "住院号", "病历号", "床号",
            "采样时间", "送检医生", "接收时间", "电话", "住址", "身份证"
        ]

    def desensitize_text(self, text):
        if not text: return ""
        lines = text.split("\n")
        safe_lines = []
        for line in lines:
            if not any(kw in line for kw in self.privacy_keywords):
                safe_lines.append(line)
        return "\n".join(safe_lines).strip()

    def blur_image_region(self, image_path, output_path, regions=None):
        """
        如果环境支持 Pillow，则打码；否则直接复制文件。
        这样在 Android 上即使没装 Pillow 也能跑通流程。
        """
        if not HAS_PILLOW:
            # 降级处理：直接复制文件，改个名
            try:
                with open(image_path, 'rb') as src, open(output_path, 'wb') as dst:
                    dst.write(src.read())
                return True
            except:
                return False

        # 有 Pillow 的情况 (电脑端测试用)
        try:
            img = Image.open(image_path)
            w, h = img.size
            if not regions:
                blur_h = int(h * 0.18)
                regions = [(0, 0, w, blur_h)]

            blurred_img = img.copy()
            for (x, y, rw, rh) in regions:
                box = (int(x), int(y), int(x + rw), int(y + rh))
                crop = img.crop(box)
                blur = crop.filter(ImageFilter.GaussianBlur(radius=30))
                blurred_img.paste(blur, box)

            blurred_img.save(output_path, quality=85)
            return True
        except Exception as e:
            print(f"Blur Error: {e}")
            return False


desensitizer = Desensitizer()