import os
from preprocessing import *



def read_mri(
    full_sequence_dir
):

    if not os.path.exists(full_sequence_dir):
        print("Path does not exist")
    else:
        print("Path exists")
    

    # Now we can iterate through the files in the sequence dir and reach each
    # of them into a numpy array
    dicom_file_list = sorted(os.listdir(full_sequence_dir))
    dicom_data_list = []

    # Saving the values of first two image positions
    # This is used to orient inferior to superior
    first_image_position = 0
    second_image_position = 0

   
    for i in range(len(dicom_file_list)):
        dicom_data = pydicom.dcmread(full_sequence_dir + "\\" + dicom_file_list[i])
        print(full_sequence_dir + "\\" + dicom_file_list[i])
        if i == 0:
            first_image_position = dicom_data[0x20, 0x32].value[-1]
        elif i == 1:
            second_image_position = dicom_data[0x20, 0x32].value[-1]

        dicom_data_list.append(dicom_data.pixel_array)

    print(dicom_file_list)    
    # Stack in numpy array
    image_array = np.stack(dicom_data_list, axis=-1)

    # Rotate if inferior and superior are flipped
    if first_image_position > second_image_position:
        image_array = np.rot90(image_array, 2, (1, 2))

    # For patients in a certain orentation, also need to flip in another axis
    # This is the same in all dicom files so we can just use the last
    # dicom file that we have from the iteration. It also needs to be rounded.
    if round(dicom_data[0x20, 0x37].value[0], 0) == -1:
        image_array = np.rot90(image_array, 2)

    return image_array, dicom_data

def main():
    path = 'ispy_data\\manifest-1711247470441\\ISPY2\\ISPY2-105513\\04-04-2001-105513T0-ISPY2MRIT0-94842\\101000.000000-ISPY2 VOLSER bi-lateral SER-68928'
   
    image_array, dicom_data = read_mri(path)
    image_array = zscore_image(normalize_image(image_array))


    import matplotlib.pyplot as plt

    plt.imshow(image_array[:, :, 50], cmap='gray')
    plt.axis('off')
    plt.show()
    pass


if __name__ == "__main__":
    main()