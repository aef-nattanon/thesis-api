
import torch
import cv2 as cv
from pathlib import Path
import numpy as np
import time
import json


def super_resolution(img, lapsrn_model):
    frame = cv.imread(img)
    _height, width = frame.shape[:2]
    if width < 500:
        result = lapsrn_model.upsample(frame)
        cv.imwrite(img, result)
    return img


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


def number_detection(img, dri, number_model):
    save_dir = './run_number/'+dri
    results = number_model(img)
    results.crop(save_dir=save_dir, save=True)
    results.save(save_dir=save_dir+'/result')

    # print("crop: ", crop)
    data_0 = results.pandas().xyxy[0].sort_values(by=['xmin', 'ymin'])
    print("results: ", results)
    print("pandas: ", data_0)
    return data_0.to_json(orient="records"), data_0.loc[:, "name"].tolist()


def meter_detection(img, dri, meter_model):
    save_dir = './run_meter/'+dri
    # meter_model.conf = 0.70  # NMS confidence threshold

    # Inference
    results = meter_model(img)
    results.crop(save_dir=save_dir, save=True)
    results.save(save_dir=save_dir+'/result')
    return save_dir+'/crops/meter number/'+Path(img).stem+'.jpg'


def my_detection(img, meter_model, number_model, lapsrn_model):
    print("👌 start: ", img)
    ts = str(time.time())

    meter_dir = meter_detection(img, ts, meter_model)
    meter_my_check_dir = my_check(meter_dir)
    meter_my_check_dir = super_resolution(meter_dir, lapsrn_model)
    r_json, data = number_detection(meter_my_check_dir, ts, number_model)
    print("results json: ", json)
    print("✅❌ result data: ", data)
    return json.loads(r_json), data, ts


def initialize_models():
    # number_model
    number_model = torch.hub.load(
        'ultralytics/yolov5', 'custom', path='./models/best-number-grayscale-to-negative-3.pt')
    # meter_model
    meter_model = torch.hub.load(
        'ultralytics/yolov5', 'custom', path='./models/best-meter.pt')
    # lapsrn_model
    lapsrn_model = cv.dnn_superres.DnnSuperResImpl_create()
    lapsrn_model.readModel("./models/LapSRN_x4.pb")
    lapsrn_model.setModel("lapsrn", 4)
    return number_model, meter_model, lapsrn_model


if __name__ == "__main__":
    print('ini grayscale-to-negative-2 🧑🏻‍💻')
    number_model, meter_model, lapsrn_model = initialize_models()
    my_detection('./1-a1-demo.jpg', meter_model, number_model, lapsrn_model)
    my_detection('./1-b1-demo.jpg', meter_model, number_model, lapsrn_model)
    my_detection('./1-c1-demo.jpg', meter_model, number_model, lapsrn_model)
    print('end 🤖')
