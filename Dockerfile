FROM anibali/pytorch:1.13.0-cuda11.8-ubuntu22.04

RUN sudo apt-get update \
  && sudo apt-get install -y libgl1-mesa-glx libgtk2.0-0 libsm6 libxext6 \
  && sudo rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY './requirements.txt' .

# RUN apt-get install libgtk2.0-dev pkg-config -yqq 

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY --chown=daemon:daemon . .

CMD ["python", "app.py"]
