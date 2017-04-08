import dicom
import sys
import pylab
import os
from matplotlib import pyplot as plt
from matplotlib import animation


def get_path_filelist(path, filter=None):
    files = os.listdir(path)
    file_list = []
    for f in files:
        if (os.path.isfile(path + '/' + f)):
            if filter is None:
                # 添加文件
                file_list.append(f)
            else:
                if filter in f:
                    file_list.append(f)

    return file_list


path = sys.argv[1]
file_list = get_path_filelist(path)
file_list.sort(key=lambda x: int(str(x).replace(".dcm", "")))
print(file_list)

fig = plt.figure()
di = dicom.read_file(path + '/0.dcm')
im = plt.imshow(di.pixel_array,vmin=-2000, vmax=4095, cmap=pylab.cm.bone)


def animate(i):
    im.set_array(dicom.read_file(path + '/' + file_list[i]).pixel_array)
    return [im]


anim = animation.FuncAnimation(fig, animate, frames=len(file_list), interval=10, blit=True)
plt.show()
