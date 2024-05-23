import cv2
import time
import sys
import numpy as np
import os

def detect_and_decode_qr_code(image_path):
    # 读取图片
    image = cv2.imread(image_path)

    if image is None:
        print(f"Image {os.path.basename(image_path)}: Unable to read the image")
        return False, ""
    # 进行目标检测和二维码识别，将检测到的目标框出，并在原图上显示二维码解码后的文本信息
    detector = cv2.QRCodeDetector()
    try:
        data, bbox, _ = detector.detectAndDecode(image)
    except UnicodeDecodeError:
        print(f"Image {os.path.basename(image_path)}: Unable to decode QR code due to invalid encoding")
        return False, ""

    decoded_text = ""
    if bbox is not None:
        # 更新解码后的文本信息
        decoded_text = data

        # 在原图上画出二维码区域的边界
        for i in range(len(bbox)):
            pt1 = tuple(map(int, bbox[i][0]))
            pt2 = tuple(map(int, bbox[(i + 1) % len(bbox)][0]))
            cv2.line(image, pt1, pt2, color=(0, 255, 0), thickness=2)
        # 显示解码后的文本信息
        cv2.putText(image, decoded_text, tuple(map(int, bbox[0][0])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

    # 如果找到二维码，返回 True 和解码后的信息，否则返回 False 和空字符串
    if decoded_text:
        return True, decoded_text
    else:
        return False, ""


def batch_detect_and_decode_qr_codes(images_folder):
    success_count = 0
    total_count = 0

    for file in os.listdir(images_folder):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            total_count += 1
            image_path = os.path.join(images_folder, file)
            success, decoded_text = detect_and_decode_qr_code(image_path)
            if success:
                success_count += 1
                print(f"Image {file}: QR code detected and decoded: {decoded_text}")
            else:
                print(f"Image {file}: No QR code detected")

    success_rate = success_count / total_count * 100
    return success_rate

images_folder = "E:\\代码接单\\opencv二维码检测\\images\\images"
success_rate = batch_detect_and_decode_qr_codes(images_folder)
print(f"QR code detection success rate: {success_rate:.2f}%")



