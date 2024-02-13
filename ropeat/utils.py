import numpy as np
import pandas as pd
import re

def get_obj_type_from_ID(ID):
    if ID > 9921000000000 and ID < 10779202101973:
        return 'galaxy'
    elif ID > 30328699913 and ID < 50963307358:
        return 'star'
    elif ID > 20000001 and ID < 120026449:
        return 'transient'
    else:
        return 'unknown'

def train_config(objtype):
    if objtype == 'galaxy':
        return 0
    elif objtype == 'star':
        return 1
    elif objtype == 'transient':
        return 2
    else: 
        return 3

def predict_config(objtype):
    if objtype == 0:
        return 'galaxy'
    elif objtype == 1:
        return 'star'
    elif objtype == 2:
        return 'transient'
    else:
        return 'other'

def make_truth_config_table(list_of_paths,n_jobs=20,verbose=False):
    colnames = ['object_id', 'ra', 'dec', 'x', 'y', 'realized_flux', 'flux', 'mag', 'obj_type']
    config_dict = {'object_id': [],
                   'band':      [],
                   'pointing':  [],
                   'sca':       []}
    if verbose:
        print('We need to get through', len(list_of_paths), 'images.')
        counter = 1
    for path in list_of_paths:
        band = path.split('_')[-3]
        pointing = path.split('_')[-2]
        sca = path.split('_')[-1].split('.')[0]
        if verbose:
            print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
            print(f'This is image {counter}/{len(list_of_paths)}.')
            print(band, pointing, sca)
            f = open(path,'r')
            lines = f.readlines()
            for l in lines[1:]:
                oid = l.split()[0]
                config_dict['object_id'].append(oid)
                config_dict['band'].append(band)
                config_dict['pointing'].append(pointing)
                config_dict['sca'].append(sca)

            if verbose:
                counter += 1
                print(f'There are {len(config_dict["object_id"])} rows in the table.')
    if verbose:
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        print('Done pulling OIDs from files.')
        print('Now, add the config values.')

    # Update this to do something that makes sense about the object IDs and the number of jobs. 
    oid_config = pd.DataFrame(config_dict).sort_values('object_id',ignore_index=True)
    bins = sorted(list(np.linspace(10**6,10**8,10)) + list(np.linspace(10**8,10**12,20)) + list(np.linspace(10**12,10**13,30)))
    config_array = np.digitize(oid_config['object_id'].astype(int),bins)
    oid_config['config'] = config_array

    if verbose:
        print('Added the config column!')
    
    return oid_config

def make_toid(oid,oid_config,ti_path,savepath):

    truth_colnames = ['object_id', 'ra', 'dec', 'x', 'y', 'realized_flux', 'flux', 'mag', 'obj_type']

    oid_lines_list = []
    oid_lines_list.append(','.join(truth_colnames)+','+'band'+','+'pointing'+','+'sca'+'\n')
    oid_tab = oid_config[oid_config['object_id'] == oid]
    for i, row in oid_tab.iterrows():
        band = row['band']
        pointing = row['pointing']
        sca = row['sca']
        with open(ti_path,'r') as f:
            lines = f.readlines()
            for li in lines[1:]:
                oid_tr = int(li.split()[0])
                if oid_tr == oid:                    
                    fline = re.sub("\s+", ",", li.strip())
                    oid_lines_list.append(fline+','+band+','+str(pointing)+','+str(sca)+'\n')
                    
    with open(savepath,'w') as oidf:
        for line in oid_lines_list:
            oidf.write(f'{line}')