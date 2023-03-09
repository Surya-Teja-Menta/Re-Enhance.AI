from __future__ import division, print_function
# coding=utf-8
import os,cv2,uuid,threading
import numpy as np
from gan import *
from splits import Splits
from deliver import Deliver
# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename


def main(user_root='test'):
        
    try:
        """Inference demo for Real-ESRGAN.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--input_path', type=str, default='inputs', help='Input image or folder')
        parser.add_argument('-n','--model_name',type=str,default='RealESRGAN_x4plus',help=('Model names: RealESRGAN_x4plus | RealESRNet_x4plus | RealESRGAN_x4plus_anime_6B | RealESRGAN_x2plus'
                'RealESRGANv2-anime-xsx2 | RealESRGANv2-animevideo-xsx2-nousm | RealESRGANv2-animevideo-xsx2'
                'RealESRGANv2-anime-xsx4 | RealESRGANv2-animevideo-xsx4-nousm | RealESRGANv2-animevideo-xsx4'))
        parser.add_argument('-o', '--output', type=str, default='results', help='Output folder')
        parser.add_argument('-s', '--outscale', type=float, default=4, help='The final upsampling scale of the image')
        parser.add_argument('--suffix', type=str, default='out', help='Suffix of the restored image')
        parser.add_argument('-t', '--tile', type=int, default=0, help='Tile size, 0 for no tile during testing')
        parser.add_argument('--tile_pad', type=int, default=10, help='Tile padding')
        parser.add_argument('--pre_pad', type=int, default=0, help='Pre padding size at each border')
        parser.add_argument('--face_enhance', action='store_true', help='Use GFPGAN to enhance face')
        parser.add_argument('--half', action='store_true', help='Use half precision during inference')
        parser.add_argument('--alpha_upsampler',type=str,default='realesrgan',help='The upsampler for the alpha channels. Options: realesrgan | bicubic')
        parser.add_argument('--ext',type=str,default='auto',help='Image extension. Options: auto | jpg | png, auto means using the same extension as inputs')
        args = parser.parse_args()
        runn(args.input_path)
    except Exception as e:
        print(e)





def runn(file_path):
    print("Image Loaded")
    s=Splits()
    tokens,h,w,ext = s.get_tokens(file_path)
    print('Tokens created')
    print(len(tokens),w,h,ext)
    d=gan.main()
    if d:
        print('resoultions created')
        i=s.get_image('outputs/',w,ext)
        print(i)

    else:
        print("Error")



if __name__ == '__main__':
    main()