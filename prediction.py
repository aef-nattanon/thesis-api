
import torch
import cv2 as cv
from pathlib import Path
import numpy as np
import time
import json
import ntpath
from helper import *
from hough_transform import *

from datetime import datetime


def super_resolution(img, lapsrn_model):
    frame = cv.imread(img)
    return super_resolution_by_image(img, frame, lapsrn_model)


def super_resolution_by_image(img, frame, lapsrn_model):
    _height, width = frame.shape[:2]
    if width < 500:
        result = lapsrn_model.upsample(frame)
        cv.imwrite(img, result)
    else:
        cv.imwrite(img, frame)
    return img


def my_bitwise_not_by_image(frame, data_class, data_name):
    frame_thresh = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    if data_name == MODEL_2_NAME:
        return cv.bitwise_not(frame_thresh)
    else:
        return frame_thresh


def my_bitwise_not(img, data_class, data_name):
    frame = cv.imread(img)
    frame_thresh = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    if data_name == MODEL_2_NAME:
        return cv.bitwise_not(frame_thresh)
    else:
        return frame_thresh


def my_check(img):
    frame = cv.imread(img)
    frame_thresh = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    avg_color_per_row = np.average(frame_thresh, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    if avg_color > 150:
        cv.imwrite(img, cv.bitwise_not(frame_thresh))
    else:
        cv.imwrite(img, frame_thresh)
    return img


def number_detection(img, dri, number_model, file_name):
    save_dir = f"./run_number/{dri}"
    results = number_model(img)
    # results.crop(save_dir=save_dir, save=True)
    results.save(save_dir=save_dir+'/result')
    data_0 = results.pandas().xyxy[0].sort_values(by=['xmin', 'ymin'])
    # print("🤖 results: ", results)
    print("📦 pandas: ", data_0)
    return data_0.to_json(orient="records"), data_0.loc[:, "name"].tolist(), f"{save_dir}/result/{file_name}"


def meter_detection(img, dri, meter_model):
    save_dir = './run_meter/'+dri
    # meter_model.conf = 0.70  # NMS confidence threshold

    # Inference
    results = meter_model(img)
    # print('🐞 ---results.pandas().xyxy[0]---', results.pandas().xyxy[0])
    results.crop(save_dir=save_dir, save=True)
    # results.save(save_dir=save_dir+'/result')
    # print('🐞 ---results---', results)

    data_0 = results.pandas().xyxy[0]
    # print('🐞 ---data_0---', data_0)
    data_class = data_0.iloc[0]['class']
    data_name = data_0.iloc[0]['name']
    return save_dir+'/crops/'+data_0.iloc[0]['name']+'/'+Path(img).stem+'.jpg', data_class, data_name


def my_detection(img, meter_model, number_model, lapsrn_model):
    print("👌 start: ", img)

    curr_dt = datetime.now()
    ts = str(int(round(curr_dt.timestamp())))
    # ts = '1'
    meter_dir, data_class, data_name = meter_detection(img, ts, meter_model)
    fixed_image, meter_dir = generalPipeline(meter_dir, True)
    fixed_image = my_bitwise_not(meter_dir, data_class, data_name)

    # fixed_image = my_bitwise_not_by_image(fixed_image, data_class, data_name)
    meter_my_check_dir = super_resolution_by_image(
        meter_dir, fixed_image, lapsrn_model)

    file_name = ntpath.basename(meter_my_check_dir)
    r_json, data, number_path = number_detection(
        meter_my_check_dir, ts, number_model, file_name)
    # print("📜 results json: ", r_json)
    print("✅❌ result data: ", data)
    return json.loads(r_json), data, ts, meter_my_check_dir, number_path


def initialize_models():
    # number_model
    number_model = torch.hub.load(
        'ultralytics/yolov5', 'custom', path='./models/best-number-grayscale-to-negative.pt')
    # meter_model
    meter_model = torch.hub.load(
        'ultralytics/yolov5', 'custom', path='./models/best-models-meter.pt')
    # 'ultralytics/yolov5', 'custom', path='./models/best-meter.pt')
    # lapsrn_model
    lapsrn_model = cv.dnn_superres.DnnSuperResImpl_create()
    lapsrn_model.readModel("./models/LapSRN_x4.pb")
    lapsrn_model.setModel("lapsrn", 4)
    # set confidence value
    number_model.conf = 0.79
    meter_model.conf = 0.40

    return number_model, meter_model, lapsrn_model


if __name__ == "__main__":
    print('ini grayscale-to-negative-2 🧑🏻‍💻')
    number_model, meter_model, lapsrn_model = initialize_models()
    my_detection('./images/img1.jpeg', meter_model, number_model, lapsrn_model)
    my_detection('./images/img3.jpeg', meter_model, number_model, lapsrn_model)
    # my_detection('https://aef-nattanon.github.io/demo3.jpg', meter_model, number_model, lapsrn_model)
    # my_detection('https://aef-nattanon.github.io/img2.jpeg', meter_model, number_model, lapsrn_model)
    print('end 🤖')
