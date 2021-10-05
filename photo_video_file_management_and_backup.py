# -*- coding: utf-8 -*-
"""
This program contains a list of functions for managing the storage of various types of
    videos and photo files for better file management
"""

import os
import shutil
import time
from PIL import Image


def get_date_taken(image_file):
    try:
        return Image.open(image_file)._getexif()[36867]
    except KeyError:
        return time.ctime(os.path.getmtime(image_file))


def merge_files_from_one_folder_to_another_folder(folder_merge_from: str, folder_merge_to: str, overwrite: bool = False):
    """ It merges two folders by copying the files from folder `folder_merge_from` to `folder_merge_to`.
        For example, if we want to copy photos from one directory to another directory, but afraid of deleting photos in the
        destination folder, we may use this function to do the copy in a safe way.

        For example: folder1 has files "/Users/user/Downloads/folder1/2020/11/1/a.jpg"
                     folder2 has files "/Users/user/Downloads/folder1/2020/11/1/b.jpg"
            This program is to merge say, from folder1 to folder2 so that we expect the folder2
                has files ["/Users/user/Downloads/folder1/2020/11/1/a.jpg"
                         , "/Users/user/Downloads/folder1/2020/11/1/b.jpg"]
                by using merge_files_from_one_folder_to_another_folder(folder1, folder2)

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
        >>> folder_merge_from, folder_merge_to = "./folder1", "./folder2"
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
                newfile_to = os.path.abspath(folder_merge_to + newfile_from[len(folder_merge_from):])
                newroot = os.path.abspath(folder_merge_to + root[len(folder_merge_from):])
                if not os.path.isdir(newroot):
                    os.makedirs(newroot)
                if overwrite or (not os.path.isfile(newfile_to)):
                    shutil.copy(newfile_from, os.path.dirname(newfile_to))
                    print("."*25)
                    print(f"Copied file {newfile_from} to {newfile_to}")
                    c += 1
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
        >>> folder_merge_to = "./folder1"
        >>> clear_ds_store_empty_files(folder1)
    """
    for root, dirs, files in os.walk(folder):
        root = os.path.abspath(root)
        if os.path.isfile(os.path.join(root, ".DS_Store")):
            try:
                os.remove(os.path.join(root, ".DS_Store"))
            except Exception as e:
                print("-"*15)
                print(" "*10 + "File {} is locked and can not be deleted. Error:{}".format(os.path.join(root, ".DS_Store"), str(e)))


def flattern_file_paths(folder: str):
    """ It flattens the files so that all individual files are moved to the first level, folder

        For example: folder = "./folder1", and it contains "./folder1/01/1.jpg", "./folder1/02/abc/2.jpg",
            This program moves all files "1.jpg", "2.jpg" into folder "./folder1" while deleting empty
            folders "./folder1/01/", "./folder1/02/abc"

    Parameters
    ----------
    folder : str
        The directory the program will flattern paths

    Returns
    -------
    None.
    """
    dir2delete = []
    folder = os.path.abspath(folder)
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f not in [".DS_Store", "", "."]:
                if not os.path.isfile(os.path.join(folder, f)):
                    shutil.move(os.path.abspath(os.path.join(root, f)), folder)
        for d in dirs:
            if os.path.abspath(os.path.join(root, d)) != folder:
                dir2delete.extend([os.path.join(root, d)])
    for d in dir2delete:
        if os.path.isdir(os.path.join(root, d)):
            shutil.rmtree(os.path.join(root, d))


def remove_duplicate_files_from_folder2clear(folder2keep, folder2clear):
    """ Remove the same files in the folder folder2clear that also exist in folder folder2keep

        For example:
            folder2keep has files "./folder1/01/a.jpg", "./folder1/03/b.jpg"
            folder2clear has files "./folder2/01/a.jpg", "./folder1/01/c.jpg"
            Then, this function remove "./folder2/01/a.jpg" in the folder2clear because
                "01/a.jpg" exists in the folder2keep

    Parameters
    ----------
    folder2keep : str
        The directory of the folder that we'll keep and be compared to
    folder2clear : str
        The directory of the folder we'll check against folder2keep, if same files exist
        in folder2keep, then delete these duplicate files in folder2clear

    Returns
    -------
    None.

    Examples
    --------
        >>> folder2keep, folder2clear = "./folder1", "./folder2"
        >>> remove_duplicate_files_from_folder2clear(folder2keep, folder2clear)
    """
    folder2keep = os.path.abspath(folder2keep)
    folder2clear = os.path.abspath(folder2clear)
    c = 0
    for root, dirs, files in os.walk(folder2clear):
        root = os.path.abspath(root)
        for f in files:
            if f not in [".DS_Store", "", "."]:
                file2clear = os.path.abspath(os.path.join(root, f))
                fileinkeepfolder = os.path.abspath(folder2keep + file2clear[len(folder2clear):])
                if os.path.isfile(fileinkeepfolder):
                    os.remove(file2clear)
                    print("."*25)
                    print(f"Deleted file {file2clear} since it exists in {folder2keep}")
                    c += 1
    if c > 0:
        print("-"*15)
        print(f"Deleted {c} files in the foldler {folder2clear} because these duplicate files were found in {folder2keep}")


if __name__ == "":
    # 1) Merge the files from "./folder1" to "./folder2" while keeping the directory path pattern
    merge_files_from_one_folder_to_another_folder("./folder1", "./folder2", overwrite=False)
    #    To force overwrite of the same files even they exist in folder2
    merge_files_from_one_folder_to_another_folder("./folder1", "./folder2", overwrite=True)
    #
    #
    # 2) Clear the ".DS_Store" cache files in folder
    clear_ds_store_empty_files("./folder1")
    clear_ds_store_empty_files("./folder2")
    #
    #
    # 3) Move all individual files from whatever folders within "./folder1" onto this folder
    flattern_file_paths("./folder1")
    #
    #
    # 3) Delete duplicate files in "./folder2" found in "./folder1"
    remove_duplicate_files_from_folder2clear("./folder1", "./folder2")
