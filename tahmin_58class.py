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

classes = { 
            0:'Speed limit (5km/h)',
            1:'Speed limit (15km/h)',
            2:'Speed limit (30km/h)',
            3:'Speed limit (40km/h)',
            4:'Speed limit (50km/h)',
            5:'Speed limit (60km/h)',
            6:'Speed limit (70km/h)',
            7:'speed limit (80km/h)',
            8:'Dont Go straight or left',
            9:'Dont Go straight or Right',
            10:'Dont Go straight',
            11:'Dont Go Left',
            12:'Dont Go Left or right',
            13:'Dont Go Right',
            14:'Dont overtake from Left',
            15:'No Uturn',
            16:'No Car',
            17:'No horn',
            18:'Speed limit (40km/h)',
            19:'Speed limit (50km/h)',
            20:'Go straight or right',
            21:'Go straight',
            22:'Go Left',
            23:'Go Left or right',
            24:'Go Right',
            25:'keep Left',
            26:'keep Right',
            27:'Roundabout mandatory',
            28:'watch out for cars',
            29:'Horn',
            30:'Bicycles crossing',
            31:'Uturn',
            32:'Road Divider',
            33:'Traffic signals',
            34:'Danger Ahead',
            35:'Zebra Crossing',
            36:'Bicycles crossing',
            37:'Children crossing',
            38:'Dangerous curve to the left',
            39:'Dangerous curve to the right',
            40:'Unknown1',
            41:'Unknown2',
            42:'Unknown3',
            43:'Go right or straight',
            44:'Go left or straight',
            45:'Unknown4',
            46:'ZigZag Curve',
            47:'Train Crossing',
            48:'Under Construction',
            49:'Unknown5',
            50:'Fences',
            51:'Heavy Vehicle Accidents',
            52:'Unknown6',
            53:'Give Way',
            54:'No stopping',
            55:'No entry',
            56:'Unknown7',
            57:'Unknown8',
}

labels=([(0, '0'), (1, '1'), (2, '10'), (3, '11'), (4, '12'), (5, '13'), (6, '14'), (7, '15'), (8, '16'), (9, '17'), (10, '18'), (11, '19'), (12, '2'), (13, '20'), (14, '21'), (15, '22'), (16, '23'), (17, '24'), (18, '25'), (19, '26'), (20, '27'), (21, '28'), (22, '29'), (23, '3'), (24, '30'), (25, '31'), (26, '32'), (27, '33'), (28, '34'), (29, '35'), (30, '36'), (31, '37'), (32, '38'), (33, '39'), (34, '4'), (35, '40'), (36, '41'), (37, '42'), (38, '43'), (39, '44'), (40, '45'), (41, '46'), (42, '47'), (43, '48'), (44, '49'), (45, '5'), (46, '50'), (47, '51'), (48, '52'), (49, '53'), (50, '54'), (51, '55'), (52, '56'), (53, '57'), (54, '6'), (55, '7'), (56, '8'), (57, '9')])


#yuklenen_model=load_model(r'C:\Users\HP\Desktop' +'\\' +'Traffic_Signal_Vgg16_10epoch_96%.h5')
yuklenen_model=load_model(r'C:\Users\HP' +'\\' +'trafik_model_yenidatasetv3.h5')

app=Flask(__name__)
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
        
        if len(filestr)==0:
            data = data_fail
            return data
        #convert string data to numpy array          
        npimg = np.fromstring(filestr, np.uint8)
        # convert numpy array to image
        testCase = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED) 
        testCase= cv2.rotate(testCase, cv2.ROTATE_90_CLOCKWISE)
        img=np.copy(testCase)
        print(npimg)
        print(npimg.dtype)
        print(npimg.shape)
        print(img)
        print(img.dtype)
        print(img.shape)
        img=detect.filteringImages(img)
        full_filename = os.path.join('./', 'imgilk.png')
        cv2.imwrite(full_filename, img)
        #plt.imshow(img)

        img=detect.returnRedness(img)
        #plt.imshow(img)
        img=detect.threshold(img,T=155)
        #plt.imshow(img)
        img=detect.morphology(img,11)
        #plt.imshow(img)
        #img=img.astype(np.uint8)
        contours=detect.findContour(img)
        big=detect.findBiggestContour(contours)
        if type(big)==int:
            data=data_fail
            return data
           
        testCase,sign=detect.boundaryBox(testCase,big)
        full_filename = os.path.join('./', 'imgTestCase.png')
        cv2.imwrite(full_filename, testCase)
        sign=sign.astype(np.uint8)
        img=cv2.resize(sign,(224,224))
        img=img.reshape(224,224,3)
        full_filename = os.path.join('./', 'imgsign.png')
        cv2.imwrite(full_filename,img)
        filename=r'C:\Users\HP\.spyder-py3\imgsign.png'
        img=Image.open(filename)
        img=img.resize((224,224))
        img=np.array(img)
# =============================================================================
#         print(img)
#         print(img.dtype)
#         print(img.shape)
#         img = img.astype('float32')
#         img=detect.NormalizeData(img)
#         print(img)
#         print(img.dtype)
#         print(img.shape)
#         #img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#         print(img)
# =============================================================================
        img=tf.expand_dims(img,axis=0)
        pred=yuklenen_model.predict(img)
        if np.amax(pred)*100<70:
            result="Trafik isareti bulunamadı"
        else:
           

           index=labels[np.argmax(pred)]
           print(index)
           index=int(index[1])
           result=classes[index]
            
        print (result)
            
    
        print('full_filename =' + request.files['attach'].filename)
    
        #request.files['attach']
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
        
#app.debug = True
app.run(host='0.0.0.0', port=80)