import cv2
from .file_handler import FileHandler
from .screen_capture import ScreenCapture
import numpy as np
import os


# noinspection SpellCheckingInspection
class VideoCompiler:
    """
    This class takes a NBLT file and creates a video file from it
    """

    def __init__(self):
        self.frame_rate: int = 0
        self.configured: bool = False
        self.file_handler: FileHandler = FileHandler()
        self.project_name: str = ""
        self.frame_size: (int, int) = None

    def configure_compiler(self, frame_rate: int, filename: str) -> None:
        """
        Configures the video compiler
        :param frame_rate:
        Frame rate of the vido file, need to be bigger tha 0 and smaller than 30
        :param filename:
        The path to the file that needs to be compiled
        """
        if frame_rate <= 0 or frame_rate > 30:
            raise Exception("Frame rates can't be negative or bigger than 30, what kind of vomit vision you want?")
        self.frame_rate = frame_rate

        if not os.path.isfile(filename):
            raise Exception("You are trying to access a file that does not exist...")

        self.file_handler.open_file(filename, "r")
        print("Calculating...")
        # reads the first line to get the configuration
        self.project_name = self.file_handler.read_line()[:-1]  # first doesnt matter
        self.file_handler.read_line()  # first doesnt matter
        frame = self.file_handler.read_line().split()  # the second has the resolution
        self.frame_size = (int(frame[0]), int(frame[1]))
        self.configured = True
        print("Set up complete...")

    def compile_file(self) -> None:
        """
        This takes a file, decompiles it and makes a video out of it.
        """
        if not self.configured:
            raise Exception("ImageCompiler not configured!")
        out = cv2.VideoWriter(self.project_name + '.mp4', cv2.VideoWriter_fourcc(*'MP4V'), self.frame_rate,
                              self.frame_size)
        while not self.file_handler.is_end_of_file():
            to_buff = self.file_handler.read_line()
            img = ScreenCapture.decode_encoded_compressed_shot(to_buff)
            matrix = np.array(img)
            inter = cv2.cvtColor(matrix, cv2.COLOR_BGR2RGB)
            out.write(inter)
        out.release()
        self.file_handler.close_file()
        print("Project compiled!")
        return
