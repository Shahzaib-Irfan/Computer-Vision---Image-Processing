from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from ImagePlayer import Ui_ImagePlayer
import cv2
import sys

class ImagePlayer_Backend:
    def __init__(self):
        app = QApplication(sys.argv)
        self.ImagePlayer = QMainWindow()
        self.ui = Ui_ImagePlayer()
        self.ui.setupUi(self.ImagePlayer)
        self.ImagePlayer.show()

        self.ui.btnBrowse.pressed.connect(self.browseFile)
        self.ui.btnRefresh.pressed.connect(self.clearImage)

        self.timer = QTimer(self.ImagePlayer)

        sys.exit(app.exec_())

    def browseFile(self):
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(None, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")

        if not image_path:
            print("File not loaded")
            sys.exit()

        self.image = cv2.imread(image_path)

        if self.image is None or self.image.shape[0] == 0 or self.image.shape[1] == 0:
            print("Invalid image.")
            sys.exit()

        q_image = QImage(self.image.data, self.image.shape[1], self.image.shape[0], self.image.strides[0], QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(q_image)

        self.ui.label.setPixmap(pixmap)
        self.ui.label.setScaledContents(True)

    def clearImage(self):
        self.ui.label.clear()
        self.timer.stop()

if __name__ == "__main__":
    backend = ImagePlayer_Backend()
    sys.exit(app.exec_())
