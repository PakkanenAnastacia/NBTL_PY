import io
import os

from typing.io import IO


class FileHandler:
    """
    C-like wrapper of the file handler built-in
    """

    fileModeTypes = "r", "a", "w", "x", "w+"

    def __init__(self):
        self.mode = None
        self.path = None
        self.eof_position = None
        self.file_pointer = None

    def open_file(self,
                  path: str,
                  mode: str
                  ) -> None:
        """
        Opens a connection and stores the file pointer
        "r" - Read - Default value. Opens a file for reading, error if the file does not exist
        "a" - Append - Opens a file for appending, creates the file if it does not exist
        "w" - Write - Opens a file for writing, creates the file if it does not exist
        "x" - Create - Creates the specified file, returns an error if the file exists
        """
        if not (mode in FileHandler.fileModeTypes):
            raise Exception("Incorrect file handler type!")
        if self.file_pointer is None:
            self.mode = mode
            self.path = path
            self.file_pointer = open(path, mode)
            return

        if type(self.file_pointer) == io.TextIOWrapper:
            if not self.file_pointer.closed:
                raise Exception("File not closed!")
            else:
                self.mode = mode
                self.path = path
                self.file_pointer = open(path, mode)
                return
        else:
            raise Exception("What are you even doing? o_o")

    def close_file(self) -> None:
        """
        Closes the connection, if no connection has been opened or the connection is already closed, it explodes
        """
        if self.file_pointer is None:
            raise Exception("File not opened!")
        if not self.file_pointer.closed:
            self.file_pointer.close()
        else:
            raise Exception("File already closed!")

    '''
    It always write a line, or a sequence of lines separated with \n
    '''

    def write(self, arg) -> None:
        """
        Writes to the file pointer if the pointer is an opened connection
        """
        if type(self.file_pointer) == io.TextIOWrapper:
            if not self.file_pointer.closed:
                if type(arg) == list:
                    for element in arg:
                        self.file_pointer.write(element + "\n")
                if type(arg) == str:
                    self.file_pointer.write(arg + "\n")
            else:
                raise Exception("The file is closed")
        else:
            raise Exception("You need to open de file first.")

    def read_line(self) -> str:
        """
        Gets one line of the file
        """
        if self.mode != "r":
            raise Exception("The file is not in read mode!")
        return self.file_pointer.readline()

    def read_whole_file(self) -> list:
        """
        Gets the whole file as a list of lines
        """
        return self.file_pointer.read().splitlines()

    def is_end_of_file(self) -> bool:
        """
        Tell whenever or not the file you are trying to read has reached the end
        """
        if self.eof_position is None:
            cur = self.file_pointer.tell()  # save current position
            self.file_pointer.seek(0, os.SEEK_END)
            self.eof_position = self.file_pointer.tell()  # find the size of file and buffer it
            self.file_pointer.seek(cur, os.SEEK_SET)
            return cur == self.eof_position
        else:
            cur = self.file_pointer.tell()  # save current position
            return cur == self.eof_position
