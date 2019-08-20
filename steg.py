#!/usr/bin/env python3

import argparse
import bitarray
import numpy as np
import png
import sys

# Examples of use:
## Encoding:
### python3 steg.py -w in.png -o out.png -t "text to encode or base64"
### cat file | python3 steg.py -w in.png -o out.png
## Decode:
### python3 steg.py -r out.png


def argsparser():
    parser = argparse.ArgumentParser(description='Simple steganography')
    parser.add_argument('-i', help="Get info of the image", type=str)
    parser.add_argument("-w", help="Write into the image", type=str)
    parser.add_argument("-t", help="Text to input or std", type=str)
    parser.add_argument("-o", help="Output filename", type=str)
    parser.add_argument("-r", help="Read Image", type=str)
    return parser.parse_args()

def get_image(filename):
    img = None
    file = open(filename, 'rb')
    reader = png.Reader(file=file)
    img = reader.read()
    return img

def print_info(img):
    info_dict = img[3]
    is_grey = info_dict["greyscale"]
    alpha = info_dict["alpha"]
    width = info_dict["size"][0]
    height = info_dict["size"][1]
    bitd = info_dict["bitdepth"]
    print("Width: {}".format(width))
    print("Height: {}".format(height))
    print("Greyscale: {}".format(is_grey))
    print("alpha: {}".format(alpha))
    print("planes: {}".format(info_dict["planes"]))
    print("bitdepth: {}".format(bitd))
    nb = 1 if alpha else 3
    if alpha:
        nb = nb + 1
    bits = width * height * nb
    byte = bits//8
    print("Bits available: {}".format(bits))
    print("Bytes available: {}".format(byte))
    return byte, bitd

def insert_data(img, text):
    byte, bitd = print_info(img)
    image = np.vstack(list(map(np.uint8, img[2])))
    l = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in text])))
    if len(l)+8 > byte:
        print("The text cannot be inserted")
        return None
    i = 0
    for x in range(len(image)):
        for y in range(len(image[0])):
            image[x][y] &= 0b11111110
            if i<len(l):
                image[x][y] |= l[i]
            i = i + 1
    return image

def save_image(img, data, filename):
    info = img[3]
    f = open(filename, 'wb')
    w = png.Writer(width=info["size"][0], height=info["size"][1],
            greyscale=info["greyscale"], alpha=info["alpha"],
            bitdepth=info["bitdepth"])
    w.write(f, data)
    f.close()

def get_data(img):
    l = []
    for line in img[2]:
        for el in line:
            l.append(el & 1)
    i = 0
    c = 0
    for d in l:
        if d == 0:
            c += 1
        else:
            c = 0
        i += 1
        if c == 15:
            i += 1
            break
    l = l[0:i]
    l = [l[i:i + 8] for i in range(0, len(l), 8)]
    st = []
    for byt in l:
        if len(byt)<8:
            break
        b = byt[0]<<7 | byt[1]<<6 | byt[2]<<5 | byt[3]<<4 | byt[4]<<3
        b = b | byt[5]<<2 | byt[6]<<1 | byt[7]
        st.append(chr(b))
    return ''.join(st)

def main():
    args = argsparser()
    if args.i:
        img = get_image(args.i)
        if not img:
            print("Error opening image")
            sys.exit(1)
        print_info(img)
    elif args.w:
        if not args.o:
            print("Need an output image")
            sys.exit(1)
        img = get_image(args.w)
        text = None
        if args.t:
            text = args.t
        else:
            text = sys.stdin.readlines()
            text = ''.join(text)
        data = insert_data(img, text)
        save_image(img, data, args.o)
    elif args.r:
        img = get_image(args.r)
        text = get_data(img)
        print(text)

if __name__=="__main__":
    main()
