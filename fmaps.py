#!/usr/bin/env python
"""
This script is used for changing fieldmap JSON files 
to include the IntendedFor key-value(s) pair.

You will need a list of fieldmap files, func nii.gz files, and dwi nii.gz files 
as text files for this exact implementation.

Author: [Your Name]

Usage:
- Modify the values of the following constants according to your file paths:
    - DWI_LIST_FILE: the file path of the text file containing a list of DWI files
    - FUNC_LIST_FILE: the file path of the text file containing a list of functional files
    - FMAP_LIST_FILE: the file path of the text file containing a list of fieldmap files
    - SOURCE_PATH: the path to the source directory containing subject and session data
- Run the script

Required Packages:
- os
- json

Functions:
- get_dwi_list(dwi_list: str, sub_id: str, ses_id: str) -> List[str]:
    Returns a list of DWI file names filtered by subject ID and session ID.
    Args:
        - dwi_list (str): the file path of the text file containing a list of DWI files
        - sub_id (str): the subject ID to filter by
        - ses_id (str): the session ID to filter by
    Returns:
        - dwis (List[str]): a list of DWI file names filtered by sub_id and ses_id
    
- get_func_list(func_list: str, sub_id: str, ses_id: str) -> List[str]:
    Returns a list of functional file names filtered by subject ID and session ID.
    Args:
        - func_list (str): the file path of the text file containing a list of functional files
        - sub_id (str): the subject ID to filter by
        - ses_id (str): the session ID to filter by
    Returns:
        - funcs (List[str]): 
          a list of functional file names filtered by sub_id and ses_id

- add_intended_for(json_file: str, funcs: List[str]) -> None:
    Reads in a JSON file and adds a new key-value pair with an array of strings for "IntendedFor".
    Args:
        - json_file (str): the file path of the JSON file to be updated
        - funcs (List[str]): 
        a list of functional file names for the same subject and session
    Returns:
        - None

Note: Make sure to update the constant values before running the script.
"""

# import packages for reading txt files, editing json files
import os
import json

# specify list files
DWI_LIST_FILE = 'TFS_dwi_list.txt'
FUNC_LIST_FILE = 'TFS_func_list.txt'
FMAP_LIST_FILE = 'TFS_fmap_list.txt'
SOURCE_PATH = 'testing/TFS/bids/sourcedata'

# define functions

def get_dwi_list(dwi_list: str, sub_id: str, ses_id: str) -> list[str]:
    """
    Returns a list of DWI file names in the format ses_id/dwi_file 
    from a text file specified by dwi_list, filtered by the
    subject ID and session ID specified by sub_id and ses_id respectively.

    Args:
    - dwi_list (str): the file path of the text file containing a list of DWI files
    - sub_id (str): the subject ID to filter by
    - ses_id (str): the session ID to filter by

    Returns:
    - dwis (List[str]): a list of DWI file names 
    filtered by sub_id and ses_id in the format ses_id/dwi_file
    """
    with open(dwi_list, 'r', encoding = 'UTF-8') as file_dwi:
        dwi_list = file_dwi.read().splitlines()
        dwis = []
        for dwi_file in dwi_list:
            # get filename without path
            dwi_file = os.path.basename(dwi_file)
            if sub_id in dwi_file and ses_id in dwi_file:
                dwis.append(ses_id + '/' + dwi_file)
    return dwis

def get_func_list(func_list: str, sub_id: str, ses_id: str) -> list[str]:
    """
    Returns a list of functional file names in the format ses_id/func_file 
    from a text file specified by func_list, filtered by the
    subject ID and session ID specified by sub_id and ses_id respectively.

    Args:
    - func_list (str): the file path of the text file 
      containing a list of functional files
    - sub_id (str): the subject ID to filter by
    - ses_id (str): the session ID to filter by

    Returns:
    - funcs (List[str]): a list of functional file names 
      filtered by sub_id and ses_id in the format ses_id/func_file
    """
    with open(func_list, 'r', encoding = 'UTF-8') as file_func:
        func_list = file_func.read().splitlines()
        funcs = []
        for func in func_list:
            # get filename without path
            func = os.path.basename(func)
            if sub_id in func and ses_id in func:
                funcs.append(ses_id + '/' + func)
    return funcs

def add_intended_for(json_file: str, funcs: list[str]) -> None:
    """
    Reads in a JSON file specified by json_file and adds 
    a new key-value pair with an array of strings for 
    "IntendedFor": [
        "<ses_id>/<sub_id>_<ses_id>_task-<taskID_1>_bold.nii.gz",
        "<ses_id>/<sub_id>_<ses_id>_task-<taskID_2>_bold.nii.gz", 
        ...
    ],
    where <ses_id>, <sub_id>, and <taskID> are extracted from 
    the file names in funcs. 
    Each element in the "IntendedFor" array corresponds to an
    fMRI file in the funcs for the same subject and session.

    Args:
    - json_file (str): the file path of the JSON file to be updated
    - funcs (List[str]): a list of functional file names 
      in the format ses_id/func_file for the same subject and session

    Returns:
    - None
    """

    with open(json_file, 'r', encoding = 'UTF-8') as file_json:
        json_dict = json.load(file_json)
    json_dict['IntendedFor'] = [func for func in funcs]
    with open(json_file, 'w', encoding = 'UTF-8') as file_json:
        json.dump(json_dict, file_json, indent=4)

# perform for all subjects and sessions
# get list of all subjects
sub_list = os.listdir(SOURCE_PATH)
for sub in sub_list:
    # get list of all sessions for each subject
    ses_list = os.listdir(SOURCE_PATH + '/' + sub)
    for ses in ses_list:
        # get list of all func files for each subject and session
        funcs = get_func_list(FUNC_LIST_FILE, sub, ses)
        # get list of all fmap files for each subject and session
        fmap_files_dir = SOURCE_PATH + '/' + sub + '/' + ses + '/fmap'
        # if fieldmap files exist, add "IntendedFor" key-value pair to each fmap json file
        fmap_file_ap = fmap_files_dir + '/' + sub + '_' + ses + '_acq-fMRI_dir-AP_epi.json'
        fmap_file_pa = fmap_files_dir + '/' + sub + '_' + ses + '_acq-fMRI_dir-PA_epi.json'
        if os.path.exists(fmap_file_ap) and os.path.exists(fmap_file_pa):
            add_intended_for(
                fmap_files_dir + '/' + sub + '_' + ses + '_acq-fMRI_dir-AP_epi.json',
                funcs
                )
            add_intended_for(
                fmap_files_dir + '/' + sub + '_' + ses + '_acq-fMRI_dir-PA_epi.json',
                funcs
                )
        # get list of all dwi files for each subject and session
        dwis = get_dwi_list(DWI_LIST_FILE, sub, ses)
        # if fieldmap files exist, add "IntendedFor" key-value pair to each dwi json file
        fmap_file_ap = fmap_files_dir + '/' + sub + '_' + ses + '_acq-dwi_dir-AP_epi.json'
        fmap_file_pa = fmap_files_dir + '/' + sub + '_' + ses + '_acq-dwi_dir-PA_epi.json'
        if os.path.exists(fmap_file_ap) and os.path.exists(fmap_file_pa):
            add_intended_for(
                fmap_files_dir + '/' + sub + '_' + ses + '_acq-dwi_dir-AP_epi.json',
                dwis
                )
            add_intended_for(
                fmap_files_dir + '/' + sub + '_' + ses + '_acq-dwi_dir-PA_epi.json',
                dwis
                )
