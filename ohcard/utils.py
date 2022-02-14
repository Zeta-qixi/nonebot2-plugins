import cv2
from .data_load import PATH
from PIL import Image
import requests
from io import BytesIO

template =  cv2.imread(PATH + 'template.png')
t_height, t_width = template.shape[:2]


def save_pic(url :str, name: str):
    res = requests.get(url)
    img = Image.open(BytesIO(res.content))
    img.save(PATH + name + ".png")

def check_pic(url :str):
    save_pic(url, 'target_image')
    target = cv2.imread(PATH + 'target_image.png')
    t_height, t_width = template.shape[:2]
    result = cv2.matchTemplate(target, template, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
	# 如果匹配度小于99%，就认为没有找到。
    if min_val > 0.01:
        return False

    return True