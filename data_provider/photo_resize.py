from PIL import Image
from pathlib import Path
import os, sys


def resizeImage(infile, dir, output_dir, size=(512, 512)):
    outfile = os.path.splitext(infile)[0]
    extension = os.path.splitext(infile)[1]

    if extension.lower() != ".jpg":
        return

    if infile != outfile:
        try:

            outfile_path_value = output_dir + os.sep + outfile + extension
            outfile_path = Path(outfile_path_value)
            if not outfile_path.exists():
                im = Image.open(dir + os.sep + infile)
                im.thumbnail(size, Image.ANTIALIAS)
                im.save(outfile_path, "JPEG")

        except IOError:
            print("cannot reduce image for ", infile)


if __name__ == "__main__":
    input_dir = "/tmp/photos/stills"

    output_dir = input_dir + "_resized"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    listdir = os.listdir(input_dir)
    count = 0;
    total = len(listdir);
    for file in listdir:
        resizeImage(file, input_dir, output_dir=output_dir)
        count += 1
        print("resized %s of %s - %s" % (count, total, file))
