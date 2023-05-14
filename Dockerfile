FROM debian:latest
RUN apt update -y
RUN apt upgrade -y
RUN apt install python3 python3-pip -y
RUN apt install git
WORKDIR /root
RUN git clone https://github.com/farinap5/ImageReconAIBot.git
RUN pip install tensorflow
RUN pip install discord
RUN pip install opencv-python
RUN mkdir /root/ImageReconAIBot/img
COPY access.json /root/ImageReconAIBot/access.json
#ENV
CMD /root/ImageReconAIBot/main.py
