import os

#os.system("./darknet detector demo cfg/coco.data cfg/yolov3-tiny.cfg yolov3-tiny.weights")

# if __name__=="__main__":

#     print("get Picture")
#     os.system("fswebcam front.jpg")
os.system("./darknet detect cfg/yolov3-tiny.cfg yolov3-tiny.weights front.jpg")
