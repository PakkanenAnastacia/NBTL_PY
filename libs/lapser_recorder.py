import threading
import time
from abc import ABC
from .screen_capture import ScreenCapture, Recorder
from .file_handler import FileHandler


class LapserRecorder(Recorder, ABC):
    """This is the recorder in time lapse mode"""

    def __init__(self, timelapse: int):
        super().__init__()
        self.lapse = timelapse  # lapse in seconds
        self.is_activated = True
        self.capture = ScreenCapture()
        self.is_configured = False
        self.handler = None

    def configure_recorder(self, file_handler: FileHandler, width: int, height: int):
        self.handler = file_handler
        self.capture.set_size(width, height)
        self.is_configured = True

    def stop_recording(self):
        self.is_activated = False
        self.handler.close_file()
        print("Recording stopped!")

    def start_recording(self):
        if not self.is_configured:
            raise Exception("Screen capture not configured!")
        task = threading.Thread(target=self.record, args=())
        task.start()
        self.is_activated = True
        self.is_paused = True
        print("Recording started!")

    def record(self):
        while self.is_activated:
            if self.is_configured and not self.is_paused:
                record = self.capture.take_compressed_encoded_shot()
                self.handler.write(record)
                time.sleep(self.lapse)
