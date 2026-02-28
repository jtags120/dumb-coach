"""Video player example with multithreaded canny edge detection process."""
  # type: ignore[import]
from cv2PySide6 import MediaController, NDArrayLabel
import numpy as np
from PySide6.QtCore import QObject, Signal, Slot, QThread, Qt, QUrl
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from processing import image_landmarks, video_landmark, image_landmarks


class FrameSender(QObject):
    """Object to sent the array to processor thread."""

    frameChanged = Signal(QVideoFrame)

class PassthroughProcessor(QObject):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.currentArray = np.empty((0, 0, 0))
        self.thread
        
        
        
        arrayChanged = False
    
    def __call__(self):
        return PassthroughProcessor(QObject)

class video_player(QWidget, ):
    def __init__(self, parent=None,):
        super().__init__(parent)
        self.frames = 


    arrayChanged = Signal(np.ndarray)

    def currentArray(self) -> np.ndarray:
        """Last array passed to :meth:`setArray`."""
        return self._currentArray

    def ready(self) -> bool:
        return self._ready

    def setArray(self, array: np.ndarray):
        self._ready = False
        self._currentArray = array
        
        self.arrayChanged.emit(array)
        self._ready = True

    def refreshCurrentArray(self):
        """Re-process and emit :meth:`currentArray`."""
        self.setArray(self.currentArray()).moveToThread(self.processorThread) 
        self.processorThread().start()

        self.videoPlayer().setVideoSink(QVideoSink(self))
        
        self.videoPlayer().videoSink().videoFrameChanged.connect(
            self.onFramePassedFromCamera
            )
        self._arrayProcessor().arrayChanged.connect(self.arrayLabel().setArray)
        
        self.arrayLabel().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mediaController().setPlayer(self.videoPlayer())


        layout = QVBoxLayout()
        layout.addWidget(self.arrayLabel())
        layout.addWidget(self.mediaController())
        self.setLayout(layout)

    def videoPlayer(self) -> QMediaPlayer:
        return self._videoPlayer

    def processorThread(self) -> QThread:
        return self._processorThread

    def arrayLabel(self) -> NDArrayLabel:
        return self._arrayLabel

    def mediaController(self) -> MediaController:
        return self._mediaController


    @Slot(QVideoFrame)
    def onFramePassedFromCamera(self, frame: QVideoFrame):
        self._frameSender.frameChanged.emit(frame)

    def closeEvent(self, event):
        self.processorThread().quit()
        self.processorThread().wait()
        super().closeEvent(event)


if __name__ == "__main__":
    from cv2PySide6 import get_data_path
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    widget = video_player()
    video_path = 
    url = QUrl.fromLocalFile(get_data_path(video_path))
    widget.videoPlayer().setSource(url)
    widget.show()
    app.exec()
    app.quit()