import dicom
import argparse
import pylab
import os
import tqdm

parser = argparse.ArgumentParser(description="由dicom格式文件生成png图片")

parser.add_argument("origin", help="文件源路径（文件或文件夹）")
parser.add_argument("--output", "-o", help="输出路径", default="./")

argv = parser.parse_args()


def get_path_filelist(path):
    files = os.listdir(path)
    file_list = []
    for f in files:
        if os.path.isfile(path + '/' + f):
            if '.dcm' in f:
                file_list.append(path + '/' + f)

    return file_list


if os.path.isdir(argv.origin):
    filelist = get_path_filelist(argv.origin)
else:
    if '.dcm' not in argv.origin:
        exit("Uncorrect origin file.")
    filelist = [argv.origin]

for file in tqdm.tqdm(filelist):
    dcm = dicom.read_file(file)
    filename = os.path.basename(file).replace(".dcm", "")
    pylab.imsave(argv.output + '/' + filename + '.png', dcm.pixel_array, cmap=pylab.cm.bone)
