from abc import ABC
from typing import Callable

from pynput.keyboard import Listener as KeyListener
from pynput.mouse import Listener as MouseListener

from .screen_capture import ScreenCapture, Recorder
from .file_handler import FileHandler


class EventRecorder(Recorder, ABC):

    def __init__(self):
        super().__init__()
        self.key_listener = None
        self.mouse_listener = None
        self.capture = ScreenCapture()
        self.is_configured = False
        self.file_handler = None
        self.on_key_release_function: Callable = OnKeyRelease(self)
        self.on_click_function: Callable = OnClickRelease(self)

    def configure_recorder(self, file_handler: FileHandler, width: int, height: int):
        self.capture.set_size(width, height)
        self.file_handler = file_handler
        self.is_configured = True

    def start_recording(self):
        if not self.is_configured:
            raise Exception("Screen capture not configured!")
        # It only matters the button releases
        self.is_paused = True
        self.key_listener = KeyListener(on_release=self.on_key_release_function)
        self.key_listener.start()
        self.mouse_listener = MouseListener(on_click=self.on_click_function)
        self.mouse_listener.start()
        print("Recording started!")

    def stop_recording(self):
        self.key_listener.stop()
        self.mouse_listener.stop()
        self.file_handler.close_file()
        print("Recording stopped!")


class OnKeyRelease:

    def __init__(self, recorder: EventRecorder) -> None:
        self.recorder: EventRecorder = recorder

    def __call__(self, *args, **kwargs):
        if self.recorder.is_configured and not self.recorder.is_paused:
            record = self.recorder.capture.take_compressed_encoded_shot()
            self.recorder.file_handler.write(record)


class OnClickRelease:

    def __init__(self, recorder: EventRecorder) -> None:
        self.recorder: EventRecorder = recorder

    def __call__(self, x, y, button, pressed):
        if self.recorder.is_configured and not self.recorder.is_paused:
            if not pressed:
                record = self.recorder.capture.take_compressed_encoded_shot()
                self.recorder.file_handler.write(record)

