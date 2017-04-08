import dicom
import argparse
import pylab
import tqdm
import os
import math
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument("path", help="Path Of dcm Files")
parser.add_argument("x", help="the X pixel of the tumor center", type=int)
parser.add_argument("y", help="the Y pixel of the tumor center", type=int)
parser.add_argument("z", help="the picture number of the tumor center", type=int)

parser.add_argument("--output", "-o", help="Output path", default="./")
parser.add_argument("--size", "-s", help="Size of the cube (int)", default="63", type=int)
parser.add_argument("--num", "-n", help="number of layer", default="32", type=int)
parser.add_argument("--startpic", "-p", help="number of start layer (priority than num)", default="-1", type=int)

argv = parser.parse_args()


def cut_one_pics(image, st_p, ed_p):
    np_arr = np.array(image)
    return np_arr[st_p[0]:ed_p[0], st_p[1]:ed_p[1]]


def get_start_end_point(x, y, size, image_size):
    ymax = image_size[0]
    # start_point = [x - int(size / 2), ymax - (y + int(size / 2))]
    # stop_point = [x + int(size / 2), ymax - (y - int(size / 2))]
    start_point = [ymax - (y + int(size / 2)), x - int(size / 2)]
    stop_point = [ymax - (y - int(size / 2)), x + int(size / 2)]
    return start_point, stop_point


def get_start_end_file(z, filelist, size, st):
    start_num = z - int(size / 2)
    stop_num = z + int(size / 2)
    if st is not -1:
        start_num = st
        stop_num = st + size
    if start_num <= 0:
        start_num = 1
    while (str(stop_num) + ".dcm") not in filelist:
        stop_num -= 1

    return start_num, stop_num


def get_path_filelist(path, filter=None):
    files = os.listdir(path)
    file_list = []
    for f in files:
        if os.path.isfile(path + '/' + f):
            if '.dcm' in f:
                file_list.append(f)

    file_list.sort(key=lambda x: int(str(x).replace(".dcm", "")))
    return file_list


def plot_nodule(image_num, output_path):
    # Learned from ArnavJain
    # https://www.kaggle.com/arnavkj95/data-science-bowl-2017/candidate-generation-and-luna16-preprocessing
    size_plot = int(math.sqrt(image_num)) + 1
    f, plots = pylab.subplots(size_plot, size_plot, figsize=(10, 10))
    # print(size_plot)
    for z_ in range(image_num):
        try:
            image = pylab.imread(output_path + "/" + str(z_ + 1) + ".png")
            plots[int(z_ / size_plot), z_ % size_plot].imshow(image, cmap=pylab.cm.bone)
        except:
            pass

    # The last subplot has no image because there are only 19 images.
    pylab.show()


file_list = get_path_filelist(argv.path)
image_size = np.array(dicom.read_file(argv.path + "/" + file_list[0]).pixel_array).shape
start_num, stop_num = get_start_end_file(argv.z, file_list, argv.num, argv.startpic)
start_point, stop_point = get_start_end_point(argv.x, argv.y, argv.size, image_size)

for file_index in tqdm.tqdm(range(start_num, stop_num)):
    pylab.imsave(argv.output + "/" + str(file_index - start_num + 1) + '.png',
                 cut_one_pics(dicom.read_file(argv.path + "/" + str(file_index) + ".dcm").pixel_array,
                              start_point, stop_point), cmap=pylab.cm.bone)

# Plot one example
plot_nodule(argv.num, argv.output)
