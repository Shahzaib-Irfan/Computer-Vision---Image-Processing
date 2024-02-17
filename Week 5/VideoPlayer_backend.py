from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from VideoPlayer import Ui_VideoPlayer
from opencv_filters import filters
import time
from datetime import datetime
import cv2
import sys

class VideoPlayer_Backend:
    def __init__(self):
        app = QApplication(sys.argv)
        self.VideoPlayer = QMainWindow()
        self.ui = Ui_VideoPlayer()
        self.ui.setupUi(self.VideoPlayer)
        self.VideoPlayer.show()
        
        self.webcam_checked = self.ui.rdbtnSort.isChecked()
        self.video_speed = self.ui.Speedslider.value()
        self.camera_index = self.ui.availableCameras.currentData() if self.ui.availableCameras.currentData() is not None else 0
        self.grayScale_value = self.ui.verticalSlider.value()
        self.ui.btnBrowse.pressed.connect(self.browseFile)
        self.ui.btnRefresh.pressed.connect(self.clearVideo)
        self.ui.availableCameras.addItems(self.get_available_cameras())
        self.ui.availableCameras.currentIndexChanged.connect(lambda: self.updateCameraData(self.ui.availableCameras.currentText()))
        self.ui.btnBrowse_2.pressed.connect(self.capture)
        self.ui.Speedslider.valueChanged.connect(self.updateVideoSpeed)
        self.ui.verticalSlider.valueChanged.connect(self.updateGrayScaleValue)
        self.ui.rdbtnSort.clicked.connect(self.updateWebcamChecked)
        self.ui.availableFilters.addItems(filters)

        self.timer = QTimer(self.VideoPlayer)
        self.timer.timeout.connect(self.updateFrame)
        
        sys.exit(app.exec_())

    def updateCameraData(self, data):
        self.camera_index = int(data)

    def updateVideoSpeed(self, value):
        self.video_speed = value / 4
        self.adjustOriginalVideoSpeed()

    def updateGrayScaleValue(self, value):
        self.grayScale_value = value
    
    def updateWebcamChecked(self):
        self.webcam_checked = self.ui.rdbtnSort.isChecked()

    def get_available_cameras(self):
        available_cameras = []
        camera_index = 0

        while True:
            cap = cv2.VideoCapture(camera_index)
            if not cap.isOpened():
                break

            available_cameras.append(str(camera_index))
            cap.release()
            camera_index += 1

        return available_cameras

    def capture(self):
        cap = None
        if self.webcam_checked:
            cap = cv2.VideoCapture("https://www.cnps.cat/panoramica.html/video.cgi")
        else:    
            cap = cv2.VideoCapture(self.camera_index)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        now = datetime.now()
        current_time = now.strftime("%H-%M-%S")
        video_filename = f"captured_video_{current_time}.avi"
        
        out = cv2.VideoWriter(video_filename, fourcc, 20.0, (640, 480))

        start_time = cv2.getTickCount()

        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret==True:
                out.write(frame)

                cv2.imshow('frame', frame)

            if (cv2.getTickCount() - start_time) / cv2.getTickFrequency() > 10:
                    break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()
        
        return video_filename



    def browseFile(self):
        file_dialog = QFileDialog()
        video_path, _ = file_dialog.getOpenFileName(None, "Open Video File", "", "Video Files (*.mp4 *.avi *.mkv *.mov)")

        if not video_path:
            print("File not loaded")
            sys.exit()

        self.vid = cv2.VideoCapture(video_path)

        if not self.vid.isOpened():
            print("Video Capture is not opened")
            sys.exit()

        fps = self.vid.get(cv2.CAP_PROP_FPS)
        self.timer.start(int(1000 / int(fps)))

    def updateFrame(self):
        ret, frame = self.vid.read()

        if not ret or frame is None or frame.shape[0] == 0 or frame.shape[1] == 0:
            print("End of video.")
            self.timer.stop()
            return

        if self.grayScale_value == 127:
            q_image = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_BGR888)
        else:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_frame = cv2.convertScaleAbs(gray_frame, alpha=self.grayScale_value / 255.0)
            q_image = QImage(gray_frame.data, gray_frame.shape[1], gray_frame.shape[0], gray_frame.strides[0], QImage.Format_Grayscale8)

        pixmap = QPixmap.fromImage(q_image)
        self.ui.label.setPixmap(pixmap)

        self.ui.label.setScaledContents(True)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            self.timer.stop()



    def clearVideo(self):
        self.ui.label.clear()
        self.timer.stop()
        self.ui.label.setPixmap(QPixmap('C:/Users/SalmanTrader/OneDrive/Pictures/CS Logo.png'))

    def adjustOriginalVideoSpeed(self):
        if hasattr(self, 'vid') and self.vid.isOpened():
            original_fps = self.vid.get(cv2.CAP_PROP_FPS)
            self.timer.setInterval(int(1000 / int(original_fps * self.video_speed) if int(original_fps * self.video_speed) is not 0 else 1))

if __name__ == "__main__":
    backend = VideoPlayer_Backend()
    sys.exit(app.exec_())
