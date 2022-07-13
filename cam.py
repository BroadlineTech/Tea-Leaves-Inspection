

import cv2
import time
import os
import datetime
from threading import Thread
from queue import Queue
import numpy as np
import imutils
from PIL import Image


class Camera:
    def __init__(self, mirror=False):
        self.data = None
        #print("Great!!")
        self.cam = cv2.VideoCapture(0,  cv2.CAP_DSHOW)
        
        self.WIDTH = 640
        self.HEIGHT = 480

        self.center_x = self.WIDTH / 2
        self.center_y = self.HEIGHT / 2
        self.touched_zoom = False

        self.image_queue = Queue()
        self.video_queue = Queue()

        self.scale = 1
        self.__setup()

        self.recording = False

        self.mirror = mirror

    def __setup(self):
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
        #self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.WIDTH)
        #self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HEIGHT)
        time.sleep(2)

    def get_location(self, x, y):
        self.center_x = x
        self.center_y = y
        self.touched_zoom = True

    def stream(self):

        def streaming():

            self.ret = True
            while self.ret:
                self.ret, np_image = self.cam.read()
                if np_image is None:
                    continue
                if self.mirror:

                    np_image = cv2.flip(np_image, 1)
                if self.touched_zoom:
                    np_image = self.__zoom(np_image, (self.center_x, self.center_y))
                else:
                    if not self.scale == 1:
                        np_image = self.__zoom(np_image)
                self.data = np_image
                k = cv2.waitKey(1)
                if k == ord('q'):
                    self.release()
                    break

        Thread(target=streaming).start()

    def __zoom(self, img, center=None):

        height, width = img.shape[:2]
        if center is None:

            center_x = int(width / 2)
            center_y = int(height / 2)
            radius_x, radius_y = int(width / 2), int(height / 2)
        else:

            rate = height / width
            center_x, center_y = center


            if center_x < width * (1-rate):
                center_x = width * (1-rate)
            elif center_x > width * rate:
                center_x = width * rate
            if center_y < height * (1-rate):
                center_y = height * (1-rate)
            elif center_y > height * rate:
                center_y = height * rate

            center_x, center_y = int(center_x), int(center_y)
            left_x, right_x = center_x, int(width - center_x)
            up_y, down_y = int(height - center_y), center_y
            radius_x = min(left_x, right_x)
            radius_y = min(up_y, down_y)


        radius_x, radius_y = int(self.scale * radius_x), int(self.scale * radius_y)


        min_x, max_x = center_x - radius_x, center_x + radius_x
        min_y, max_y = center_y - radius_y, center_y + radius_y


        cropped = img[min_y:max_y, min_x:max_x]

        new_cropped = cv2.resize(cropped, (width, height), interpolation=cv2.INTER_CUBIC)

        return new_cropped

    def touch_init(self):
        self.center_x = self.WIDTH / 2
        self.center_y = self.HEIGHT / 2
        self.touched_zoom = False
        self.scale = 1

    def zoom_out(self):

        if self.scale < 1:
            self.scale += 0.1
        if self.scale == 1:
            self.center_x = self.WIDTH
            self.center_y = self.HEIGHT
            self.touched_zoom = False

    def zoom_in(self):

        if self.scale > 0.2:
            self.scale -= 0.1

    def zoom(self, num):
        if num == 0:
            self.zoom_in()
        elif num == 1:
            self.zoom_out()
        elif num == 2:
            self.touch_init()



    def save_picture(self):


        ret, img = self.cam.read()
        now1 = datetime.datetime.now()
        now_str1 = now1.strftime("%Y-%m-%d-%H-%M-%S")
        ret, img = self.cam.read()
        outfilename1 = 'Img-{}.jpg'.format(now_str1)
        path = 'C:/hannah/demo/teaimages'
        
        cv2.imwrite(os.path.join(path, outfilename1), img)
        # list_of_files = glob.glob(r'C:\hannah\demo\teaimages\*.jpg') 
        # latest_file = max(list_of_files, key=os.path.getctime)
        # path1 = ('C:/hannah/demo/teaimages/' + latest_file)
        #cv2.imshow('Background Removed', img)
        '''
        imag = cv2.imread(path1)
        lower = np.array([140, 140, 140])
        upper = np.array([255, 255, 255])
        thresh = cv2.inRange(imag, lower, upper)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (26, 30))
        morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        mask = 255 - morph
        result = cv2.bitwise_and(imag, imag, mask=mask)
        cv2.imshow('Background Removed', result)
        outfilename2 = 'Img-{}.jpg'.format(now_str1)
        path2 = ('C:/hannah/demo/teaimages')
        cv2.imwrite(os.path.join(path2, outfilename2), result)
        '''

    def record_video(self):

        fc = 20.0
        record_start_time = time.time()
        now = datetime.datetime.now()
        date = now.strftime('%Y%m%d')
        t = now.strftime('%H')
        num = 1
        filename = 'C:/Users/dashi/Documents/MyRiV/espeyh_videos/captured_{}_{}.avi'.format(date, t, num)
        while os.path.exists(filename):
            num += 1
            filename = 'videos/captured_{}_{}_{}.avi'.format(date, t, num)
        codec = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
        out = cv2.VideoWriter(filename, codec, fc, (int(self.cam.get(3)), int(self.cam.get(4))))
        while self.recording:
            if time.time() - record_start_time >= 600:
                self.record_video()
                break
            ret, frame = self.cam.read()
            if ret:
                if len(os.listdir('C:/Users/dashi/Documents/MyRiV/espeyh_videos')) >= 100:
                    name = self.video_queue.get()
                    if os.path.exists(name):
                        os.remove(name)
                out.write(frame)
                self.video_queue.put_nowait(filename)
            k = cv2.waitKey(1)
            if k == ord('q'):
                break

    def show(self):
        while True:
            frame = self.data
            if frame is not None:
                cv2.imshow('TeaLeaves', frame)
                cv2.setMouseCallback('TeaLeaves', self.mouse_callback)
            key = cv2.waitKey(1)
            if key == ord('q'):

                self.release()
                cv2.destroyAllWindows()
                break

            elif key == ord('z'):

                self.zoom_in()

            elif key == ord('x'):

                self.zoom_out()

            elif key == ord('p'):

                self.save_picture()

            elif key == ord('v'):

                self.touch_init()

            elif key == ord('r'):

                self.recording = not self.recording
                if self.recording:
                    t = Thread(target=cam.record_video)
                    t.start()

    def release(self):
        self.cam.release()
        cv2.destroyAllWindows()

    def mouse_callback(self, event, x, y, flag, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            self.get_location(x, y)
            self.zoom_in()
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.zoom_out()


if __name__ == '__main__':
    cam = Camera(mirror=True)
    cam.stream()
    cam.show()