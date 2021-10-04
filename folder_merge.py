# -*- coding: utf-8 -*-
"""
This program is for safe copying the files to merge from one folder to another folder
    while keeping source folder hierarchy.
"""

import os
import shutil

def merge_files_from_one_folder_to_another_folder(folder_merge_from: str, folder_merge_to: str, overwrite: bool = False):
    """ It merges two folders by copying the files from folder `folder_merge_from` to `folder_merge_to`.
        For example, if we want to copy photos from one directory to another directory, but afraid of deleting photos in the
        destination folder, we may use this function to do the copy in a safe way

    Parameters
    ----------
    folder_merge_from : str
        The directory of the folder where we copy/merge the files from
    folder_merge_to : str
        The directory of the folder where we copy/merge the files to

    overwrite: bool, optional
        Determine if the same file exists in the destination folder, should we overwrite the file or not

    Returns
    -------
    None.

    Examples
    --------
        >>> folder_merge_to = "./Photos and Videos"
        >>> folder_merge_from = "./extra_photos"
        >>> merge_files_from_one_folder_to_another_folder(folder_merge_from, folder_merge_to)
    """
    folder_merge_from = os.path.abspath(folder_merge_from)
    folder_merge_to = os.path.abspath(folder_merge_to)
    #curr_dir = os.path.abspath(os.getcwd())
    c = 0
    for root, dirs, files in os.walk(folder_merge_from):
        root = os.path.abspath(root)
        for f in files:
            if f not in [".DS_Store", "", "."]:
                newfile_from = os.path.abspath(os.path.join(root, f))
                newfile_to = newfile_from.replace(folder_merge_from,folder_merge_to)
                newfile_to = newfile_to.replace("//","/")
                newroot = root.replace(folder_merge_from,folder_merge_to)
                newroot = newroot.replace("//","/")
                if not os.path.isdir(newroot):
                    os.makedirs(newroot)
                if overwrite or (not os.path.isfile(newfile_to)):
                    shutil.copy(newfile_from, os.path.dirname(newfile_to))
                    print("."*25)
                    print(f"Copied file {newfile_from} to {newfile_to}")
                    c +=1
    print("<"*25)
    print(f"There are {c} files being copied to {folder_merge_to}")


def clear_ds_store_empty_files(folder: str):
    """ The program clears the .DS_Store cache files on a Mac computer

    Parameters
    ----------
    folder : str
        The directory to clear all .DS_Store files from

    Returns
    -------
    None.

    Examples
    --------
        >>> folder_merge_to = "./Photos and Videos"
        >>> folder_merge_from = "./extra_photos"
        >>> clear_ds_store_empty_files(folder_merge_from)
        >>> clear_ds_store_empty_files(folder_merge_to)
    """
    for root, dirs, files in os.walk(folder):
        root = os.path.abspath(root)
        if os.path.isfile(os.path.join(root, ".DS_Store")):
            try:
                os.remove(os.path.join(root, ".DS_Store"))
            except Exception as e:
                print("-"*15)
                print(" "*10 + "File {} is locked and can not be deleted. Error:{}".format(os.path.join(root, ".DS_Store"), str(e)))
