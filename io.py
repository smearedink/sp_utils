
import numpy as np
import fileinput

def read_sp_files(files):
    """Read all *.singlepulse files in the current directory in a DM range.
        Return 5 arrays (properties of all single pulses):
                DM, sigma, time, sample, downfact."""
    finput = fileinput.input(files)
    data = np.loadtxt(finput,
                       dtype=np.dtype([('dm', 'float32'),
                                        ('sigma','float32'),
                                        ('time','float32'),
                                        ('sample','uint32'),
                                        ('downfact','uint8')]))
    return np.atleast_2d(data)

def read_tarfile(filenames, names, tar):
    members = []
    for name in names:
        if name in filenames:
            member = tar.getmember(name)
            members.append(member)
        else:
            pass
    fileinfo = []
    filearr = []
    for mem in members:
        file = tar.extractfile(mem)
        for line in file.readlines():
            fileinfo.append(line)
        filearr+=(fileinfo[1:])
        fileinfo = []
    temp_list = []
    for i in range(len(filearr)):
        temp_line = filearr[i].split()
        temp_list.append(temp_line)
    main_array = np.asarray(temp_list)
    main_array = np.split(main_array, 5, axis=1)
    main_array[0] = main_array[0].astype(np.float16)
    main_array[1] = main_array[1].astype(np.float16)
    main_array[2] = main_array[2].astype(np.float16)
    main_array[3] = main_array[3].astype(np.int)
    main_array[4] = main_array[4].astype(np.int)
    return main_array
def gen_arrays(dm, threshold, sp_files, tar):    
    """
    Extract dms, times and signal to noise from each singlepulse file as 1D arrays.
    """
    max_dm = np.ceil(np.max(dm)).astype('int')
    min_dm = np.min(dm).astype('int')
    diff_dm = max_dm-min_dm
    ddm = min_dm-diff_dm
    if (ddm <= 0):
        ddm = 0
    dmss = np.zeros((1,)).astype('float32')
    timess = np.zeros((1,)).astype('float32')
    sigmass = np.zeros((1,)).astype('float32')
    ind = []
    dm_time_files = []
    for i in range(ddm,(max_dm+diff_dm)):
        """after DM of 1826 the dm step size is >=1, therefore we need to pick the correct DMs."""
        if (i >= 1826) and (i < 3266):
            if int(i)%2 == 1:
                i = i+1
            try:
                singlepulsefiles = [sp_files[sp_file] for sp_file in range(len(sp_files)) if ('DM'+str(i)+'.') in sp_files[sp_file]]
                dm_time_files += singlepulsefiles
                if tar is not None:
                    data = read_tarfile(sp_files, singlepulsefiles, tar)
                else:
                    data = read_sp_files(singlepulsefiles)[0]
            except:
                pass
        elif (i >= 3266) and (i < 5546):
            if int(i)%3 == 0:
                i = i+2
            if int(i)%3 == 1:
                i = i+1
            try:
                singlepulsefiles = [sp_files[sp_file] for sp_file in range(len(sp_files)) if ('DM'+str(i)+'.') in sp_files[sp_file]]
                dm_time_files += singlepulsefiles
                if tar is not None:
                    data = read_tarfile(sp_files, singlepulsefiles, tar)
                else:
                    data = read_sp_files(singlepulsefiles)[0]
            except:
                pass
        elif i>=5546:
            if int(i)%5 == 2:
                i = i+4
            if int(i)%5 == 3:
                i = i+3
            if int(i)%5 == 4:
                i = i+2
            if int(i)%5 == 0:
                i = i+1
            try:
                singlepulsefiles = [sp_files[sp_file] for sp_file in range(len(sp_files)) if ('DM'+str(i)+'.') in sp_files[sp_file]]
                dm_time_files += singlepulsefiles
                if tar is not None:
                    data = read_tarfile(sp_files, singlepulsefiles, tar)
                else:
                    data = read_sp_files(singlepulsefiles)[0]
            except:
                pass
        else:    
            try:
                singlepulsefiles = [sp_files[sp_file] for sp_file in range(len(sp_files)) if ('DM'+str(i)+'.') in sp_files[sp_file]]
                dm_time_files += singlepulsefiles
                if tar is not None:
                    data = read_tarfile(sp_files, singlepulsefiles, tar)
                else:
                    data = read_sp_files(singlepulsefiles)[0]
            except:
                pass
        if tar is not None:
            dms = np.reshape(data[0],(len(data[0]),))
            times = np.reshape(data[2],(len(data[1]),))
            sigmas = np.reshape(data[1],(len(data[2]),))
        else:
            dms = data['dm']
            times = data['time']
            sigmas = data['sigma']
        dms = np.concatenate((dmss, dms), axis = 0)
        dmss = dms
        times = np.concatenate((timess, times), axis = 0)
        timess = times
        sigmas = np.concatenate((sigmass, sigmas), axis = 0)
        sigmass = sigmas
    dms = np.delete(dms, (0), axis = 0)
    times = np.delete(times, (0), axis = 0)
    sigmas = np.delete(sigmas, (0), axis = 0)
    return dms, times, sigmas, dm_time_files

