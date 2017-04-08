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


path = input('Path:')
type = input('Location(Z|Y):')

file_list = get_path_filelist(path)
file_list.sort(key=lambda x: int(str(x).replace(".dcm", "")))

pixel_endwise = []

for f in file_list:
    if type == 'Z':
        pixel_endwise.append(dicom.read_file(path + '/' + f).pixel_array[0])
    else:
        pixel_endwise.append([i[0] for i in dicom.read_file(path + '/' + f).pixel_array])

fig = plt.figure()
im = plt.imshow(pixel_endwise, vmin=-2000, vmax=4095, cmap=plt.cm.bone)


def animate(i):
    pixel_endwise = []
    for f in file_list:
        if type == 'Z':
            pixel_endwise.append(dicom.read_file(path + '/' + f).pixel_array[i])
        else:
            pixel_endwise.append([k[i] for k in dicom.read_file(path + '/' + f).pixel_array])
    im.set_array(pixel_endwise)
    return [im]


anim = animation.FuncAnimation(fig, animate, frames=500, interval=60, blit=True)
plt.show()
# pylab.imshow(pixel_endwise, cmap=pylab.cm.bone)
# pylab.show()
