# Compare WAD

Compare GoldSrc WAD3 files.

## Usage

Call the script from a commandline (such as CMD or Terminal)
using the path of each WAD to compare as the arguments:

```cli
python3 comparewad.py path/to/reference.wad path/to/compare.wad
```

The result of the comparison will be printed as a diff table of the file entries.<br>
File entries with identical names but different data will show as modified (`!`),
and the dimensions and filesizes will be printed on the same line.
> [!NOTE]
> Even if the dimensions and filesizes of two files are identical,
> the contents might be different.
