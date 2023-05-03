from ultralytics import YOLO
import torch
import torch.nn as nn
import cv2

PATH_WEIGHT_DETECTION = "E:/7/KPP/ApplicationDetectEsophagit/weights_model/detection/best_yolov8.pt"
PATH_WEIGHT_CLASSIFICATION = "E:/7/KPP/ApplicationDetectEsophagit/weights_model/classification/densnet121_softmax_eph50.pt"

class ModelDetect(nn.Module):
    def __init__(self):
        super(ModelDetect, self).__init__()
        self.model = YOLO(PATH_WEIGHT_DETECTION)
        self.model.val()
        # self.predict = None

    def forward(self, img, conf=0.8):
        # картику не нужно преобразовывать в torch после прочтения cv2
        predict = self.model.predict(source=img, conf=conf)
        return predict
    
    # def save_res(self, name):
    #     cv2.imwrite(name, self.predict[0].plot())


class ModelClassificationZLine(nn.Module):
    def __init__(self):
        super(ModelClassificationZLine, self).__init__()
        self.model = torch.load(PATH_WEIGHT_CLASSIFICATION)
    
    def forward(self, img):
        # картинка прочитана и переведена в торч
        predict = self.model(img)
        return predict
    


    
