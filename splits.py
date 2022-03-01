import numpy as np
import cv2,os
import flask

class Splits:
    def __init__(self,size=516):
        self.size = size

    def get_tokens(self,image_path,user_root):

        try:
            ext=image_path.split('.')[-1]
            #dir='inputs/'
            # for i in os.listdir(dir):
            #     os.remove(os.path.join(dir, i))
            image = cv2.imread(image_path)
            print('Image shape:', image.shape)
            r, c = 0, 0
            h = image.shape[0]//self.size if image.shape[0]%self.size == 0 else image.shape[0]//self.size + 1
            w = image.shape[1]//self.size if image.shape[1]%self.size == 0 else image.shape[1]//self.size + 1
            print(h,w)
            tokens = []
            for i in range(h):
                r = i*self.size
                for j in range(w):
                    c = j*self.size
                    tokens.append(image[r:r+self.size,c:c+self.size])
            print('Total tokens:', len(tokens))
            os.makedirs(f'inputs/{user_root}',exist_ok=True)
            for i in range(len(tokens)):
                cv2.imwrite(f'inputs/{user_root}/'+str(i)+'.'+ext,tokens[i])
                print('Token {} saved'.format(i))
            return tokens,h,w,ext

        except Exception as e:
            print(e)

    def get_image(self,path, w,ext,user_root):
        try:
            stack=[]
            tokens=[]
            
            for i in range(len(os.listdir(f'{path}{user_root}'))):
                tokens.append(cv2.imread(f'{path}{user_root}/{str(i)}.{ext}'))
            for i in range(0,len(tokens),w):
                stack.append(np.hstack(tokens[i:i+w]))
            final=np.vstack(stack)
            print(final.shape,'final Image created')
            os.makedirs(f'results/{user_root}',exist_ok=True)
            cv2.imwrite(f'results/{user_root}/Enhanced_image.{ext}',cv2.cvtColor(final,cv2.COLOR_BGR2RGB))
            cv2.imwrite(f'results/{user_root}/Enhanced_image.{ext}',final)
            # img=cv2.imread(f'results/{user_root}/Enhanced_image.{ext}')
            # simg=cv2.blur(img,(3,3),0)
            #simg=cv2.cvtColor(simg,cv2.COLOR_BGR2RGB)
            # cv2.imwrite(f'results/{user_root}/Enhanced_image.{ext}',simg)
            print('Enhanced_image.{} created'.format(ext))
            return 'results/{}/Enhanced_image.{}'.format(user_root,ext)
        except Exception as e:
            print(e)