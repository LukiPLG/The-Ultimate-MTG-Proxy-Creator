import os
import cv2
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
from PIL import Image

def upscaler(path):
    model = RRDBNet(
        num_in_ch=3,
        num_out_ch=3,
        num_feat=64,
        num_block=23,
        num_grow_ch=32,
        scale=2
    )

    upsampler = RealESRGANer(
        scale=2,
        model_path="models/RealESRGAN_x2plus.pth",
        model=model,
        tile=0,
        tile_pad=10,
        pre_pad=0,
        half=False
    )

    img = cv2.imread(path)
    output, _ = upsampler.enhance(img)

    output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    return Image.fromarray(output_rgb)
