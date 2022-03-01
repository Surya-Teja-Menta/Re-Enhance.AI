FROM ubuntu


RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    python3.8 python3-pip python3.8-dev
RUN apt-get install libglib2.0-0 ffmpeg libsm6 libxext6 -y
LABEL image for a flask application


RUN python3 -m pip install --upgrade pip

COPY . /esrgan

WORKDIR /esrgan

RUN pip3 install --use-deprecated=html5lib torch==1.10.2+cpu torchvision==0.11.3+cpu  -f https://download.pytorch.org/whl/cpu/torch_stable.html

RUN pip install -r requirements.txt


ENTRYPOINT python3 application.py