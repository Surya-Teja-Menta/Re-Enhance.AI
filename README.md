# Re-Enhance.AI

The Re-Enhance.AI project is a set of tools and algorithms that can be used to improve the quality of your Image.

The tools are designed to be used in a concurrent multi-threaded environment.we can run this web app with one or more images. The Resultant Super Resolution image is mailed to the user. After the task done, the depending folders are deleted.


### Installation

1. Clone repo

    ```bash
    git clone https://github.com/Surya-Teja-Menta/Re-Enhance.AI.git
    cd Real-ESRGAN
    ```

2. Install dependent packages
    ```bash
    #if you have GPU
    pip install torch torchvision
    pip install -r requirements.txt
    ```
    ```bash
    #if you don't have GPU
    pip install -r requirements.txt
    ```
3. Run the code

    ```bash
    python application.py
    ```

## Outputs
---
| Test Image | Enhanced Image |
| ---------- | ------------- |
| ![test](test_image.png) | ![generated](enhanced_image.png) |

Observe the details in the Generated Enhanced Image. The enhanced image is a super resolution image.

