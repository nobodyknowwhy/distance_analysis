import h5py

# 打开HDF5文件
with h5py.File(r'D:\gs\duoyuanfenxi\H1E_OPER_OCT_L3A_20240516_Chl_a_9KM_10\H1E_OPER_OCT_L3A_20240516_Chl_a_9KM_10.h5',
               'r') as file:
    print("Keys: %s" % file.keys())

    geophysical_data = file['Geophysical Data']

    print("Datasets in 'Geophysical Data': %s" % geophysical_data.keys())

    if 'SST' in geophysical_data:
        sst_data = geophysical_data['SST'][:]
        print("Shape of SST dataset:", sst_data.shape)
        print("First few elements of SST dataset:", sst_data[:5])  # 打印前5个元素作为示例
    else:
        print("SST dataset not found in 'Geophysical Data' group.")

    if 'Chl_a' in geophysical_data:
        print(f"yes, is {geophysical_data['Chl_a'][:]}")
    else:
        print('no')


