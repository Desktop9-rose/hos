import re
import os
from PIL import Image, ImageFilter


class Desensitizer:
    def __init__(self):
        # --- 敏感信息正则库 ---
        self.patterns = {
            "name": re.compile(r"(姓名|患者)[:：\s]*([\u4e00-\u9fa5]{2,4})"),
            "phone": re.compile(r"(1[3-9]\d{9})"),
            "id_card": re.compile(r"(\d{6})(\d{8})(\d{4}|[\dX])"),
            "hospital_header": re.compile(r".*医院|.*科室|检验报告单")
        }

    def desensitize_text(self, text):
        # (此处文本脱敏逻辑保持不变，省略以节省空间)
        return text, False

    def blur_image_region(self, image_path, output_path, regions=None):
        """
        图片脱敏：对指定区域进行高斯模糊
        """
        print(f"DEBUG [Desensitizer]: 开始处理图片 {image_path}")

        try:
            # 1. 打开图片
            img = Image.open(image_path)
            print(f"DEBUG [Desensitizer]: 图片打开成功，尺寸: {img.size}")

            w, h = img.size

            # 2. 确定模糊区域 (默认顶部 15%)
            if not regions:
                blur_h = int(h * 0.15)
                regions = [(0, 0, w, blur_h)]
                print(f"DEBUG [Desensitizer]: 使用默认模糊区域 (高 {blur_h}px)")

            # 3. 处理图片
            blurred_img = img.copy()

            for (x, y, rw, rh) in regions:
                # 确保坐标是整数
                box = (int(x), int(y), int(x + rw), int(y + rh))
                print(f"DEBUG [Desensitizer]: 正在模糊区域 {box}")

                crop = img.crop(box)
                blur = crop.filter(ImageFilter.GaussianBlur(radius=20))  # 增加模糊半径
                blurred_img.paste(blur, box)

            # 4. 保存结果
            blurred_img.save(output_path, quality=90)
            print(f"DEBUG [Desensitizer]: 保存成功 -> {output_path}")

            # 5. 验证文件是否存在
            if os.path.exists(output_path):
                return True
            else:
                print("DEBUG [Desensitizer]: 保存后文件未找到！")
                return False

        except Exception as e:
            print(f"DEBUG [Desensitizer]: 发生异常 -> {e}")
            import traceback
            traceback.print_exc()  # 打印完整报错堆栈
            return False


# 单例
desensitizer = Desensitizer()