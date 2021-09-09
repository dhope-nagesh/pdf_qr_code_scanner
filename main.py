import tempfile
import glob
import argparse
from os.path import join, basename, isdir
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode
from pyzbar.wrapper import ZBarSymbol
import cv2
import numpy as np


from time import perf_counter
from contextlib import contextmanager


def scan_qr_codes(image, deep_search=False):
    width, height = image.size

    # Setting the points for cropped image
    left = 0
    top = 0
    right = width
    bottom = height // 4

    im1 = image.crop((left, top, right, bottom))

    # Scale image, so that it is more clear to search QR code
    if deep_search:
        im1 = im1.resize((right * 2, bottom * 2))

    for THRESHOLD in [cv2.THRESH_TRUNC, cv2.THRESH_BINARY, None]:

        if THRESHOLD is None:
            bw_im = np.array(im1)
        else:
            ret, bw_im = cv2.threshold(np.array(im1), 150, 255, THRESHOLD)
        decoded_objects = decode(bw_im, symbols=[ZBarSymbol.QRCODE])

        if decoded_objects is not None and len(decoded_objects) > 0:
            for obj in decoded_objects:
                return obj.data.decode("utf-8")
    return None


def scan(input_folder, deep_search, unrecognized_folder):
    total_unrecognized = 0
    for file in glob.glob(join(input_folder, '*.pdf')):
        pdf_name = basename(file)
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path(file, dpi=200, output_folder=path, thread_count=20)
            print("Exported ", pdf_name, " to ", path)
            for idx, img in enumerate(images_from_path):
                page_num = idx + 1
                qr_code = scan_qr_codes(img, deep_search)
                if qr_code is not None:
                    print([pdf_name, page_num, qr_code])
                elif qr_code is None and page_num % 2 == 1:
                    total_unrecognized += 1
                    if isdir(unrecognized_folder):
                        img.save(f"{unrecognized_folder}/{page_num}_{pdf_name}.jpg")

    print("Total unrecognized pages: ", total_unrecognized)
    if isdir(unrecognized_folder):
        print("Unrecognized pages are saved at ", unrecognized_folder)


def get_args():
    parser = argparse.ArgumentParser(description='Scan pdfs')
    parser.add_argument('-i', '--input-folder', required=True, help='Where all pdf files take place.')
    parser.add_argument('-o', '--output-folder', required=False, help='Put unrecognized files here')
    parser.add_argument('-d', '--deep-search', help='Deep search', action='store_true')
    return parser.parse_args()


@contextmanager
def catchtime() -> float:
    start = perf_counter()
    yield lambda: perf_counter() - start


if __name__ == '__main__':
    args = get_args()
    output_folder = args.output_folder if isdir(args.output_folder if args.output_folder is not None else '') else None
    if output_folder is None:
        print("output_folder not provided, to save unrecognized file use -o or --output-folder option")
    with catchtime() as t:
        scan(args.input_folder, args.deep_search, output_folder)

    print(f"Execution time: {t():.4f} secs")
