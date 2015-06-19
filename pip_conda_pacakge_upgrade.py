#!/usr/bin/env python
 
 """
 This is for automated installation of anaconda or pip python packages

 This might cause problems, be cautious!!!!

 Sample usage:
 $ python pip_conda_pacakge_upgrade.py
 """

import subprocess
import pip

pip_install_ind = True
s = subprocess.call("sudo conda update --all",shell=True)
if s != 0:
    pip_install_ind = False

if pip_install_ind:
    dists = []
    for dist in pip.get_installed_distributions():
        dists.append(dist.project_name)
     
    for dist_name in sorted(dists, key=lambda s: s.lower()):
        cmd = "sudo pip install {0} -U".format(dist_name)
        print '#', cmd
        subprocess.call(cmd,shell=True)
