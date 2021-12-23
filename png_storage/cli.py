import argparse
import io
import os
from pathlib import Path
import zipfile


def encode(args):
    zip_contents = io.BytesIO()
    with zipfile.ZipFile(zip_contents, 'w') as zp:
        for path in map(Path, args.paths):
            if path.is_file():
                zp.write(path)
            else:
                for (dirpath, _, filenames) in os.walk(path):
                    for name in filenames:
                        zp.write(os.path.join(dirpath, name))

    zip_contents.seek(0)
    with open(args.out, 'wb') as out, open(args.png, 'rb') as png:
        out.write(png.read())
        out.write(zip_contents.read())


def decode(args):
    outdir = Path(args.dir)
    outdir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.encoded_file, 'r') as zp:
        zp.extractall(args.dir)


def main():
    parser = argparse.ArgumentParser(description='PNG file encoding/decoding')
    subparsers = parser.add_subparsers()

    get_input_parser = subparsers.add_parser("encode", help="Encode files into a png")
    get_input_parser.add_argument("png", type=str, help="<Required> PNG to encode files into")
    get_input_parser.add_argument("-p", "--paths", nargs='+', type=str, required=True, help="<Required> Paths to encode")
    get_input_parser.add_argument("-o", "--out", type=str, default="out.png", help="Encoded PNG output")
    get_input_parser.set_defaults(func=encode)

    get_input_parser = subparsers.add_parser("decode", help="Decode files from a png")
    get_input_parser.add_argument("encoded_file", type=str, help="Encoded PNG to decode")
    get_input_parser.add_argument("-d", "--dir", type=str, default=".", help="Path to output directory")
    get_input_parser.set_defaults(func=decode)

    args = parser.parse_args()

    if 'func' not in args:
        exit(parser.print_usage())

    args.func(args)

if __name__ == '__main__':
    main()
