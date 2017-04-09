from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage import measure, feature
from skimage.measure import label, regionprops, perimeter
from skimage.morphology import binary_closing, ball
import matplotlib.pyplot as plt
import cut_lung
import numpy as np
import dicom
import os
import tqdm


def get_path_filelist(path, filter=None):
    files = os.listdir(path)
    file_list = []
    for f in files:
        if os.path.isfile(path + '/' + f):
            if '.dcm' in f:
                file_list.append(f)

    file_list.sort(key=lambda x: int(str(x).replace(".dcm", "")))
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


def segment_lung_from_ct_scan(ct_scan):
    print("Get segmented lungs:")
    return np.asarray([cut_lung.get_segmented_lungs(slice) for slice in tqdm.tqdm(ct_scan)])


def plot_ct_scan(scan, step=40):
    f, plots = plt.subplots(int(scan.shape[0] / step) + 1, 4, figsize=(25, 25))
    print("Build view:")
    for i in tqdm.tqdm(range(0, scan.shape[0], int(step / 4))):
        plots[int(i / step), int((i % step) / (step / 4))].axis('off')
        plots[int(i / step), int((i % step) / (step / 4))].imshow(scan[i], cmap=plt.cm.bone)

    plt.show()


def filter_nodule(image, threshold):
    image[image < threshold] = 0

    selem = ball(4)
    binary = binary_closing(image, selem)

    label_scan = label(binary)

    areas = [r.area for r in regionprops(label_scan)]
    areas.sort()

    print("Clean blood vessels:")
    for r in tqdm.tqdm(regionprops(label_scan)):
        max_x, max_y, max_z = 0, 0, 0
        min_x, min_y, min_z = 10000, 10000, 10000

        for c in r.coords:
            max_z = max(c[0], max_z)
            max_y = max(c[1], max_y)
            max_x = max(c[2], max_x)

            min_z = min(c[0], min_z)
            min_y = min(c[1], min_y)
            min_x = min(c[2], min_x)
        # if min_z == max_z or min_y == max_y or min_x == max_x or r.area > areas[-5] and r.area != areas[-3]:
        if r.area != areas[-3]:
            for c in r.coords:
                image[c[0], c[1], c[2]] = 0
        else:
            index = (max((max_x - min_x), (max_y - min_y), (max_z - min_z))) / (
                min((max_x - min_x), (max_y - min_y), (max_z - min_z)))
    return image


def plot_3d(image, threshold=-300):
    # Position the scan upright,
    # so the head of the patient would be at the top facing the camera
    print("Create 3d view:")
    p = image.transpose(2, 1, 0)
    p = p[:, :, ::-1]

    verts, faces, _, _ = measure.marching_cubes_lewiner(p, threshold)

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Fancy indexing: `verts[faces]` to generate a collection of triangles
    mesh = Poly3DCollection(verts[faces], alpha=0.1)
    face_color = [0.5, 0.5, 1]
    mesh.set_facecolor(face_color)
    ax.add_collection3d(mesh)

    ax.set_xlim(0, p.shape[0])
    ax.set_ylim(0, p.shape[1])
    ax.set_zlim(0, p.shape[2])

    plt.show()


if __name__ == "__main__":
    path = input("path:")
    file_list = get_path_filelist(path)
    ct_scan = read_dcm_files(file_list, path)
    # plot_3d(ct_scan, 604)
    # plot_ct_scan(ct_scan, 60)
    segmented_ct_scan = segment_lung_from_ct_scan(ct_scan)
    segmented_ct_scan = filter_nodule(segmented_ct_scan, 1000)

    plot_3d(segmented_ct_scan, 1000)
    # plot_ct_scan(segmented_ct_scan)
    # while True:
    #     value = int(input("Threshold(int):"))
    #     plot_3d(segmented_ct_scan, value)
