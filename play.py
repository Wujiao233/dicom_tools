import dicom
import sys
import pylab
import os
import tqdm
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation


def play(array):
    fig = plt.figure()
    im = plt.imshow(array[0], vmin=-2000, vmax=4095, cmap=pylab.cm.bone)

    def animate(i):
        im.set_array(array[i])
        return [im]

    anim = animation.FuncAnimation(fig, animate, frames=len(array), interval=60, blit=True)
    plt.show()


if __name__ == "__main__":
    def get_path_filelist(path, filter=None):
        files = os.listdir(path)
        file_list = []
        for f in files:
            if os.path.isfile(path + '/' + f):
                if filter is None:
                    # 添加文件
                    file_list.append(f)
                else:
                    if filter in f:
                        file_list.append(f)

        return file_list


    def read_dcm_files(filelist, path):
        print("Reading files:")
        slices = [dicom.read_file(path + "/" + f) for f in tqdm.tqdm(filelist)]

        # Sort the dicom slices in their respective order
        slices.sort(key=lambda x: int(x.InstanceNumber))

        # Get the pixel values for all the slices
        slices = np.stack([s.pixel_array for s in slices])
        slices[slices == -2000] = 0
        return slices


    path = sys.argv[1]
    file_list = get_path_filelist(path)
    file_list.sort(key=lambda x: int(str(x).replace(".dcm", "")))
    print(file_list)
    arr = read_dcm_files(file_list, path)
    play(arr)
