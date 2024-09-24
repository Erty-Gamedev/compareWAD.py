from typing import Final
from pathlib import Path
from struct import unpack
from enum import IntEnum
from hashlib import md5


class InvalidFormatException(Exception): pass
class InvalidFileTypeException(Exception): pass

PALETTE_SIZE: Final[int] = 768  # 256 * 3

class FILE_TYPE(IntEnum):
    QPIC = 0x42
    MIPTEX = 0x43
    FONT = 0x46
    SPRAY = 0x40


def read_ntstring(data: bytes, length: int) -> str:
    strbytes = unpack(f"<{length}s", data)[0]
    string = ''
    for b in strbytes:
        if b == 0:
            break
        string += chr(b)
    return string

class DirEntry:
    def __init__(self, data: bytes):
        self.filepos = unpack('<l', data[0:4])[0]
        self.disksize = unpack('<l', data[4:8])[0]
        self.size = unpack('<l', data[8:12])[0]
        self.type = unpack('<b', data[12:13])[0]
        self.compression = unpack('<?', data[13:14])[0]
        self.padding = unpack('<h', data[14:16])[0]
        self.name = read_ntstring(data[16:32], 16)

    def __str__(self):
        return self.name


class FileEntry:
    def __init__(self) -> None:
        self.name: str
        self.disksize: int
        self.width: int
        self.height: int
        self.data: bytes
        self.md5: bytes

    def __str__(self):
        return self.name

class MiptexEntry(FileEntry):
    def __init__(self, data: bytes, disksize: int) -> None:
        name_bytes: bytes = unpack('<16s', data[0:16])[0]
        name_bytes = name_bytes.split(b'\x00', 1)[0]
        
        self.name = name_bytes.decode('charmap')
        self.width = unpack('<L', data[16:20])[0]
        self.height = unpack('<L', data[20:24])[0]
        self.mipoffset1 = unpack('<L', data[28:32])[0]
        self.data = data[40:self.mipoffset1]
        self.palette = data[-PALETTE_SIZE-2:-2]
        self.md5 = md5(self.data + self.palette, usedforsecurity=False).digest()
        self.disksize = disksize
    
    def __repr__(self) -> str:
        return f"Miptex({self.name}, {self.disksize} bytes)"

class SprayEntry(MiptexEntry):
    def __repr__(self) -> str:
        return f"Spray({self.name}, {self.disksize} bytes)"


class QpicEntry(FileEntry):
    def __init__(self, data: bytes, name: str, disksize: int) -> None:
        self.name = name
        self.disksize = disksize

        self.width = unpack('<L', data[0:4])[0]
        self.height = unpack('<L', data[4:8])[0]
        data_offset = 8 + self.width * self.height
        self.data = data[8:data_offset]
        self.colors_used = unpack('<h', data[data_offset:data_offset+2])[0]
        palette_size = self.colors_used * 3
        self.palette = data[data_offset+2:data_offset+2+palette_size]
        self.md5 = md5(self.data + self.palette, usedforsecurity=False).digest()

    def __repr__(self) -> str:
        return f"Qpic({self.name}, {self.disksize} bytes)"

class FontEntry(FileEntry):
    def __init__(self, data: bytes, name: str, disksize: int) -> None:
        self.name = name
        self.disksize = disksize

        self.width = unpack('<L', data[0:4])[0]
        self.height = unpack('<L', data[4:8])[0]
        self.row_count = unpack('<L', data[8:12])[0]
        self.row_height = unpack('<L', data[12:16])[0]
        data_offset = 16 + 1024
        data_length = self.width * self.height
        self.data = data[data_offset:data_offset+data_length]
        colors_used_offset = data_offset + data_length
        self.colors_used = unpack('<h', data[colors_used_offset:colors_used_offset+2])[0]
        palette_offset = colors_used_offset + 2
        self.palette = data[palette_offset:palette_offset+(self.colors_used * 3)]
        self.md5 = md5(self.data + self.palette, usedforsecurity=False).digest()

    def __repr__(self) -> str:
        return f"Font({self.name}, {self.disksize} bytes)"


class Wad3Reader:
    """
    Reads all the files from the specified .wad package.
    The instance can be accessed as a dictionary that maps
    file name to its FileEntry instance.
    """

    def __init__(self, file: Path):
        self.file = file
        with file.open('rb') as wadfile:
            data = wadfile.read()

            header = data[0:12]
            magic = header[0:4]
            if magic != bytes('WAD3', 'ascii'):
                raise InvalidFormatException(
                    f"{file} is not a valid WAD3 file.")

            num_dir_entries = unpack('<l', header[4:8])[0]
            dir_offset = unpack('<l', header[8:])[0]

            self.header = {
                'magic': magic,
                'num_dir_entries': num_dir_entries,
                'dir_offset': dir_offset,
            }

            directories = data[dir_offset:]

            self.dir_entries = []
            self.entries: dict[str, FileEntry] = {}
            for i in range(0, 32 * num_dir_entries, 32):
                entry = DirEntry(directories[i:i+32])
                self.dir_entries.append(entry)
                filepos = entry.filepos
                disksize = entry.disksize
                entry_file: FileEntry

                if entry.type == FILE_TYPE.QPIC:
                    entry_file = QpicEntry(
                        data[filepos:filepos+disksize],
                        entry.name,
                        disksize
                    )
                elif entry.type == FILE_TYPE.MIPTEX:
                    entry_file = MiptexEntry(
                        data[filepos:filepos+disksize],
                        disksize
                    )
                elif entry.type == FILE_TYPE.SPRAY:
                    entry_file = SprayEntry(
                        data[filepos:filepos+disksize],
                        disksize
                    )
                elif entry.type == FILE_TYPE.FONT:
                    entry_file = FontEntry(
                        data[filepos:filepos+disksize],
                        entry.name,
                        disksize
                    )
                else:
                    raise InvalidFileTypeException(f"Invalid entry file type: '{entry.type}'")

                self.entries[entry_file.name.lower()] = entry_file

    def __contains__(self, name: str) -> bool:
        return name.lower() in self.entries

    def __getitem__(self, name: str) -> FileEntry:
        return self.entries[name.lower()]
