import argparse
import cv2
import glob
import os
from basicsr.archs.rrdbnet_arch import RRDBNet

from realesrgan import RealESRGANer
from realesrgan.archs.srvgg_arch import SRVGGNetCompact

class gan:
        
    def main(user_root='test'):
        try:
            """Inference demo for Real-ESRGAN.
            """
            parser = argparse.ArgumentParser()
            parser.add_argument('-i', '--input', type=str, default='inputs', help='Input image or folder')
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

            # determine models according to model names
            
            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
            netscale = 4
            model_name = 'RealESRNet_x4plus'
            # determine model paths
            model_path = os.path.join('experiments/pretrained_models', model_name + '.pth')
            if not os.path.isfile(model_path):
                model_path = os.path.join('realesrgan/weights', model_name + '.pth')
        
            # restorer
            upsampler = RealESRGANer(
                scale=netscale,
                model_path=model_path,
                model=model,
                tile=0,
                tile_pad=10,
                pre_pad=0,
                half=args.half)

            # from gfpgan import GFPGANer
            # face_enhancer = GFPGANer(
            #     model_path='https://github.com/TencentARC/GFPGAN/releases/download/v0.2.0/GFPGANCleanv1-NoCE-C2.pth',
            #     upscale=4,
            #     arch='clean',
            #     channel_multiplier=2,
            #     bg_upsampler=upsampler)
            os.makedirs(f'outputs', exist_ok=True)
            os.makedirs(f'outputs/{user_root}', exist_ok=True)

            if os.path.isfile(f'inputs/{user_root}'):
                paths = [f'inputs/{user_root}/']
            else:
                paths = sorted(glob.glob(os.path.join(f'inputs/{user_root}', '*')))

            for idx, path in enumerate(paths):
                imgname, extension = os.path.splitext(os.path.basename(path))
                print('Processing {}.{}'.format(imgname, extension))
                print('Testing', idx, imgname)

                img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
                if len(img.shape) == 3 and img.shape[2] == 4:
                    img_mode = 'RGBA'
                else:
                    img_mode = None

                try:
                    output, _ = upsampler.enhance(img, outscale=4)
                    # _, _, output = face_enhancer.enhance(img, has_aligned=False, only_center_face=False, paste_back=True)
                except RuntimeError as error:
                    print('Error', error)
                    print('If you encounter CUDA out of memory, try to set --tile with a smaller number.')
                else:
                    ext='auto'
                    if ext == 'auto':
                        extension = extension[1:]
                    else:
                        extension = ext
                    if img_mode == 'RGBA':  # RGBA images should be saved in png format
                        extension = 'png'
                    save_path = os.path.join('outputs',user_root, f'{imgname}.{extension}')
                    cv2.imwrite(save_path, output)
                    print('Saved', save_path)
                    print('Done')
            return True
        except Exception as e:
            print(e)
            return False

if __name__ == '__main__':
    gan.main()
