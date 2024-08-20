from preprocessing import *

#updated method to take alist of dicom file from a directory
#This function removes the dependency of mapping csv file used by dukes code
def read_precontrast_mri_ispy(full_sequence_dir):

    dicom_file_list = sorted(os.listdir(full_sequence_dir))
    dicom_data_list = []
    # Saving the values of first two image positions
    # This is used to orient inferior to superior
    first_image_position = 0
    second_image_position = 0

    for i in range(len(dicom_file_list)):
        #print(dicom_file_list[i])
        full_sequence_dir = Path(full_sequence_dir)
        file_name = full_sequence_dir.joinpath(dicom_file_list[i])

        #file_name = full_sequence_dir / dicom_file_list[i]

        #print(file_name)
        dicom_data = pydicom.dcmread(file_name)
        
        if i == 0:
            first_image_position = dicom_data[0x20, 0x32].value[-1]
        elif i == 1:
            second_image_position = dicom_data[0x20, 0x32].value[-1]

        dicom_data_list.append(dicom_data.pixel_array)

    # Stack in numpy array
    image_array = np.stack(dicom_data_list, axis=-1)



    # For patients in a certain orentation, also need to flip in another axis
    # This is the same in all dicom files so we can just use the last
    # dicom file that we have from the iteration. It also needs to be rounded.
    if round(dicom_data[0x20, 0x37].value[0], 0) == -1:
        image_array = np.rot90(image_array, 2)

    return image_array, dicom_data
