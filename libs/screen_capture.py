import base64
from abc import ABC, abstractmethod
from enum import Enum
from io import BytesIO

from PIL import Image, ImageGrab
from screeninfo import get_monitors

from .file_handler import FileHandler
from .string_compressor import StringCompressor


class Recorder(ABC):
    def __init__(self):
        self.is_paused = True

    @abstractmethod
    def configure_recorder(self,
                           handler: FileHandler,
                           width: int,
                           height: int
                           ):
        """Configures the Recorder"""
        pass

    @abstractmethod
    def start_recording(self):
        """Starts the recorder"""
        pass

    @abstractmethod
    def stop_recording(self):
        """Stops the recorder"""
        pass

    def pause_switch(self):
        """Pauses or unpauses the recording"""
        self.is_paused = not self.is_paused


class RecorderTypes(Enum):
    """
    Basic recorder types
    """

    BullShiet = 0
    NonBullShiet = 1

    @staticmethod
    def list_values():
        return list(map(lambda c: c.value, RecorderTypes))

    @staticmethod
    def list_labels():
        return list(map(lambda c: c.name, RecorderTypes))


class ResolutionValues(Enum):
    """
    Possible resolution values that the recorder can accept
    """

    R640_480 = (640, 480)
    R1024_768 = (1024, 768)
    R1280_720 = (1280, 720)
    R1280_800 = (1280, 800)
    R1280_1024 = (1280, 1024)
    R1440_900 = (1440, 900)
    R1600_1200 = (1600, 1200)
    R1920_1080 = (1920, 1080)
    R1920_1200 = (1920, 1200)
    R2048_1080 = (2048, 1080)
    R3840_2160 = (3840, 2160)

    @staticmethod
    def list_values():
        return list(map(lambda c: c.value, ResolutionValues))

    @staticmethod
    def list_labels():
        return list(map(lambda c: str(c.value[0]) + 'x' + str(c.value[1]), ResolutionValues))


class ScreenCapture:
    # Constant
    IMAGE_FORMAT_COMPRESSION: str = "jpeg"

    def __init__(self):
        self.shot_size: [int] = [0, 0]
        self.lapse: int = 0
        self.is_size_set: bool = False

    @classmethod
    def get_original_size(cls) -> (int, int):
        """Gets the size of the main monitor"""
        # this is a horrible implementation but who gives a shiet? o,o
        monitors = get_monitors()
        return monitors[0].width, monitors[0].height

    def set_size(self, width: int, height: int):
        if (width, height) not in ResolutionValues.list_values():
            raise Exception("The resolution is not in the supported ranges!")
        self.shot_size[0]: int = width
        self.shot_size[1]: int = height
        self.is_size_set = True

    def set_size_tuple(self, sizes: (int, int)):
        if sizes not in ResolutionValues.list_values():
            raise Exception("The resolution is not in the supported ranges!")
        self.shot_size[0]: int = sizes[0]
        self.shot_size[1]: int = sizes[1]
        self.is_size_set = True

    def take_compressed_encoded_shot(self) -> str:
        """
        Outputs a screenshot as an hex formatted string.
        Needs an instance for the setup of hte screen size. 
        """
        if not self.is_size_set:
            raise Exception("Size must be set to take the shot")
        buffered = BytesIO()
        image = ImageGrab.grab().resize(tuple(self.shot_size))

        image.save(buffered, format=ScreenCapture.IMAGE_FORMAT_COMPRESSION)
        img_str = base64.b64encode(buffered.getvalue()).decode("UTF-8")
        return StringCompressor.compress(img_str).hex()

    @staticmethod
    def decode_encoded_compressed_shot(arg: str) -> Image:
        """
        Takes a screen of a compressed shot and turns it into an image object
        """
        shot_enc = StringCompressor.decompress(bytes.fromhex(arg))
        msg = base64.b64decode(shot_enc)
        buf = BytesIO(msg)
        img = Image.open(buf)
        return img
