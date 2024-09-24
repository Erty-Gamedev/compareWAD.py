import sys
import filecmp
from pathlib import Path
from wad3_reader import Wad3Reader

__version__ = '1.0.0'


def print_usage() -> None:
    print('''Usage: python3 comparewad.py REFERENCE_WAD COMPARE_WAD

REQUIRED ARGUMENTS
 * REFERENCE_WAD\t(path)\tpath to the WAD file to compare against
 * COMPARE_WAD  \t(path)\tpath to WAD file to compare with

OPTIONS
  --version\t-v\t\tprint script version and exit
  --help\t-h\t\tprint this message and exit
''')

def exit_error(msg: str) -> None:
    print(msg)
    exit(1)

def handle_args() -> tuple[Path, Path]:
    n_args = len(sys.argv)
    if n_args < 2:
        print_usage()
        exit(0)
    
    if '-h' in sys.argv or '--help' in sys.argv:
        print_usage()
        exit(0)

    if '-v' in sys.argv or '--version' in sys.argv:
        print(f"Compare WAD v{__version__}")
        exit(0)
    
    if n_args < 3:
        exit_error('Missing path for WAD to compare against')
    
    left = Path(sys.argv[1])
    if not left.exists():
        exit_error(f"{left.resolve()} was not found")
    
    right = Path(sys.argv[2])
    if not right.exists():
        exit_error(f"{right.resolve()} was not found")

    return left, right


if __name__ == "__main__":
    left, right = handle_args()

    if filecmp.cmp(left, right, shallow=False):
        print("The files are identical")
        exit(0)

    left_r = Wad3Reader(left)
    right_r = Wad3Reader(right)

    all_files = list(set(left_r.entries.keys()).union(right_r.entries.keys()))
    all_files.sort()

    print(f"{left.name:19}| {right.name}")
    print('___________________|___________________')
    for file in all_files:
        if file not in left_r:
            print(f"- {file:<17}| + {file}")
            continue

        if file not in right_r:
            print(f"+ {file:<17}| - {file}")
            continue

        if left_r[file].md5 != right_r[file].md5:
            left_f, right_f = left_r[file], right_r[file]
            print(f"! {file:<17}| ! {file:<17} "\
                f"({left_f.width}x{left_f.height}, {left_f.disksize} bytes - "\
                f"{right_f.width}x{right_f.height}, {right_f.disksize} bytes)")
            continue
