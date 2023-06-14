# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 18:47:14 2023

@author: HP
"""

from flask import Flask, request
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import traffic_sign_detection_with_image as detect
import json
from matplotlib import pyplot as plt
import tensorflow as tf
import os
from PIL import Image

classes = {0: 'Azami hız sınırlaması (20km/saat)',
           1: 'Azami hız sınırlaması  (30km/saat)',
           2: 'Kamyonlar için öndeki taşıtı geçmek yasaktır ',
           3: 'Ana Yol Tali Yol Kavşağı',
           4: 'Ana Yol',
           5: 'Yol Ver',
           6: 'Dur',
           7: 'Taşıt Trafiğine Kapalı Yol',
           8: 'Kamyon Giremez',
           9: 'Girişi Olmayan Yol',
           10: 'Dikkat',
           11: 'Sola Doğru Tehlikeli Viraj',
           12: 'Azami hız sınırlaması  (50km/saat)',
           13: 'Sağa Doğru tehlikeli viraj',
           14: 'Tehlikeli Eğim İniş',
           15: 'Kasisli yol',
           16: 'Kaygan Yol',
           17: 'Sağdan Daralan Kaplama',
           18: 'Yolda Çalışma',
           19: 'Trafik ışıkları',
           20: 'Yaya Geçidi',
           21: 'Okul Geçidi',
           22: 'Bisiklet Giremez',
           23: 'Azami hız sınırlaması  (60km/saat)',
           24: 'Gizli Buzlanma',
           25: 'Vahşi Hayvan Geçidi',
           26: 'Bütün yasaklama ve Kısıtlama sonu',
           27: 'İleriden Sağa Mecburi Yön',
           28: 'İleriden Sola Mecburi Yön',
           29: 'İleri mecburi yön',
           30: 'İleri ve Sağa Mecburi Yön',
           31: 'İleri ve Sola Mecburi Yön',
           32: 'Sağdan Gidiniz',
           33: 'Soldan Gidiniz',
           34: 'Azami hız sınırlaması (70km/saat)',
           35: 'Ada etrafında dönünüz',
           36: 'Geçme Yasağı Sonu',
           37: 'Kamyonlarda geçme yasağı sonu',
           38: 'Azami hız sınırlaması (80km/saat)',
           39: 'Azami hız sınırının sonu (80km/h)',
           40: 'Azami hız sınırlaması (100km/saat)',
           41: 'Azami hız sınırlaması (120km/saat)',
           42: 'Öndeki taşıtı geçmek yasaktır'
           }
labels = ([(0, '0'), (1, '1'), (2, '10'), (3, '11'), (4, '12'), (5, '13'), (6, '14'), (7, '15'), (8, '16'), (9, '17'), (10, '18'), (11, '19'), (12, '2'), (13, '20'), (14, '21'), (15, '22'), (16, '23'), (17, '24'), (18, '25'), (19, '26'), (20, '27'), (21,
          '28'), (22, '29'), (23, '3'), (24, '30'), (25, '31'), (26, '32'), (27, '33'), (28, '34'), (29, '35'), (30, '36'), (31, '37'), (32, '38'), (33, '39'), (34, '4'), (35, '40'), (36, '41'), (37, '42'), (38, '5'), (39, '6'), (40, '7'), (41, '8'), (42, '9')])



yuklenen_model = load_model(r'C:\Users\HP' + '\\' + 'trafik_model_yeni.h5')

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
data_fail = {
    "isSuccess": False,
    "result": "trafik işareti bulunamadı"
}


@app.route('/trafikisareti', methods=['POST'])
def deneme():

    try:

        latestfile = request.files['attach']
        filestr = latestfile.read()
        if len(filestr) == 0:
            data = data_fail
            return data
        # convert string data to numpy array
        npimg = np.fromstring(filestr, np.uint8)
        # convert numpy array to image
        testCase = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
        testCase= cv2.rotate(testCase, cv2.ROTATE_90_CLOCKWISE)
        full_filename = os.path.join('./', 'imgilk.png')
        cv2.imwrite(full_filename, testCase)
       
        img = np.copy(testCase)
        img = detect.filteringImages(img)
     
        img = detect.returnRedness(img)
        full_filename = os.path.join('./', 'imgilk.png')
        cv2.imwrite(full_filename, img)
        img = detect.threshold(img, T=155)
     
        img = detect.morphology(img, 11)
     

        contours = detect.findContour(img)
        big = detect.findBiggestContour(contours)
        if type(big) == int:
            print(1)
            data=data_fail
            return data

        testCase, sign = detect.boundaryBox(testCase, big)
       
        
        full_filename = os.path.join('./', 'imgTestCase.png')
        cv2.imwrite(full_filename, testCase)
        
        full_filename = os.path.join('./', 'imgsign.png')
        cv2.imwrite(full_filename, sign)
        
        sign=sign/255
        
        img = cv2.resize(sign, (100, 100))
        img = img.reshape(100, 100, 3)
       
        img = tf.expand_dims(img, axis=0)
        pred = yuklenen_model.predict(img)
        if np.amax(pred)*100 < 70:
            print(np.amax(pred))
            result = "Trafik isareti bulunamadı"
        else:

            index = labels[np.argmax(pred)]
            print(index)
            index = int(index[1])
            result = classes[index]

        print(result)

        print('full_filename =' + request.files['attach'].filename)

        
        data = {
            "isSuccess": True,
            "result": result
        }
        return json.dumps(data)
    except Exception as e:
        print(e)
        data = {
            "isSuccess": False,
            "result": str(e)
        }

    return data


app.run(host='0.0.0.0', port=80)
