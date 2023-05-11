from src.dataset import VideoToBatchImage
from src.model import ModelClassificationZLine, ModelDetect
import cv2
import os

TRESHOLD_ZLINE = 25
TRESHOLD_NOTLINE = 80 
TRESHOLD_COUNT_TRUE_PRED = 2
TRESHOLD_COUNT_FALSE_PRED = 5
TRESHOLD_STOP_PREDICTION = 100
STOP_PREDICTION = 20

class PredictClassification():
    def __init__(self, path_video, stride=2/60):
        """
        stride: сколько кадров пропускать в видео.
        """
        self.model = ModelClassificationZLine()
        self.dataset = VideoToBatchImage(path_video, stride= stride)
        
        self.list_img_true = []
        self.list_img_false = []
        self.res = []

        for img in self.dataset:
            self.check_classification(img, self.predict(img))
            if len(self.res) > 0 and len(self.list_img_false) > TRESHOLD_STOP_PREDICTION or len(self.res) > STOP_PREDICTION:
                break
    
    def predict(self, img):
        pred = self.model(img)

        return pred
    
    def check_classification(self, img, predict):
        """
        Метод работает над проверкой изображений, выделяет те, изображения,
        на которых есть z-линия.

        img: текущее изображение
        predict: предсказание классификатора на изобр.

        return: список картинок, которые можно подавать детектору.
        """
        fanc_pred_proc = lambda x: round(x.item() * 100, 4)
        pred_zline = fanc_pred_proc(predict[0][1])
        pred_notline = fanc_pred_proc(predict[0][0])
        
        if pred_zline >= TRESHOLD_ZLINE:
            self.list_img_true.append(img)
            self.list_img_false = [] 
        elif pred_notline >= TRESHOLD_NOTLINE:
            self.list_img_false.append(img)
            self.list_img_true = []

        if len(self.list_img_false) > TRESHOLD_COUNT_FALSE_PRED:
            self.list_img_true = []
            self.list_img_false = []
        elif len(self.list_img_true) >= TRESHOLD_COUNT_TRUE_PRED:
            if len(self.list_img_false) > 0:
                self.res = self.list_img_true + self.list_img_false
            else:
                self.res = self.list_img_true
            
        return self.res
    
    def __getitem__(self, index):
        return self.res[index]
    
    def __len__(self):
        return len(self.res)


class PredictDetection():
    def __init__(self, path_save, list_img):
        self.path_save = path_save
        self.model = ModelDetect()
        
        for i, img in enumerate(list_img):
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            res = self.model(img)
            # сохраняем картинки только с боксами
            if len(res[0].boxes) > 0:
                self.save_res(i, res[0])
            
    def save_res(self, i, pred):
        print('пошло сохранение')
        # создание папки для сохранения картинок
        try:
            os.mkdir(self.path_save)
        except:
            pass

        path = self.path_save + '/'+ str(i) + '.png'
        cv2.imwrite(path, pred.plot())