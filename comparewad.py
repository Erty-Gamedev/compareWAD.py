import sys
import filecmp
from pathlib import Path
from wad3_reader import Wad3Reader
import consolestyling as cs

__version__ = '1.0.0'


def print_usage() -> None:
    print(f"""Usage: python3 comparewad.py REFERENCE_WAD COMPARE_WAD

{cs.BOLD}REQUIRED ARGUMENTS{cs.RESET}
 * REFERENCE_WAD\t(path)\tpath to the WAD file to compare against
 * COMPARE_WAD  \t(path)\tpath to WAD file to compare with

{cs.BOLD}OPTIONS{cs.RESET}
  --version\t-v\t\tprint script version and exit
  --help\t-h\t\tprint this message and exit
""")

def exit_error(msg: str) -> None:
    print(cs.styleError(msg))
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
        exit_error(f"'{left.resolve()}' was not found")
    
    right = Path(sys.argv[2])
    if not right.exists():
        exit_error(f"'{right.resolve()}' was not found")

    return left, right


if __name__ == "__main__":
    left, right = handle_args()

    if filecmp.cmp(left, right, shallow=False):
        print(cs.styleWarning("The files are identical"))
        exit(0)

    left_r = Wad3Reader(left)
    right_r = Wad3Reader(right)

    left_set = set(left_r.entries.keys())
    right_set = set(right_r.entries.keys())

    all_files = list(left_set.union(right_set))
    all_files.sort()

    modified: list[str] = []
    for file in left_set.intersection(right_set):
        if left_r[file].md5 != right_r[file].md5:
            modified.append(file)
    modified.sort()

    unique_left = len(left_set.difference(right_set))
    unique_right = len(right_set.difference(left_set))

    print(
        f"{len(modified) + unique_left + unique_right} differences ("\
        f"{cs.styleAdded(f"{unique_left} added")}, "\
        f"{cs.styleRemoved(f"{unique_right} removed")}, "\
        f"{cs.styleModified(f"{len(modified)} modified")})\n"
    )

    print(f"{cs.FGBRIGHT_BLACK}{left.name:19}| {right.name}")
    print(f"___________________|___________________{cs.RESET}")

    bar = cs.styleMuted('|')

    for file in all_files:
        if file not in left_r:
            print(
                f"{cs.styleAdded('- ')}"\
                f"{cs.styleAdded(file, True):<30}{bar}"\
                f"{cs.styleAdded(f" + {file:<16}")}{bar}"
            )
            continue

        if file not in right_r:
            print(
                f"{cs.styleRemoved(f"+ {file:<17}")}{bar}"\
                f"{cs.styleRemoved(' - ')}"\
                f"{cs.styleRemoved(file, True):<29}{bar}"
            )
            continue

        if file in modified:
            left_f, right_f = left_r[file], right_r[file]

            print(f"{cs.styleModified(f"! {file:<17}")}{bar}{cs.styleModified(f" ! {file:<16}")}{bar}", end='')
            print(cs.styleMuted(
                f" ({left_f.width}x{left_f.height}, {left_f.disksize} bytes - "\
                f"{right_f.width}x{right_f.height}, {right_f.disksize} bytes)"
            ))
            continue

    exit(0)
