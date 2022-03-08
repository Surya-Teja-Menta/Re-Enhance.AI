import argparse
import cv2
import glob
import os
from basicsr.archs.rrdbnet_arch import RRDBNet

from realesrgan import RealESRGANer
from realesrgan.archs.srvgg_arch import SRVGGNetCompact

class gan:
        
    def main(user_root):
        try:
            

            
            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
            netscale = 4
            model_name = 'RealESRGAN_x4plus'
            # determine model paths
            model_path = os.path.join('experiments/pretrained_models', model_name + '.pth')
            if not os.path.isfile(model_path):
                model_path = os.path.join('realesrgan/weights', model_name + '.pth')
        
            # restorer
            upsampler = RealESRGANer(
                scale=netscale,
                model_path=model_path,
                model=model,
                tile=8,
                tile_pad=10,
                pre_pad=0,
                )

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
