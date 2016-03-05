
rpm -Uvh http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el7.rf.x86_64.rpm
rpm -Uvh http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-5.noarch.rpm

yum update
yum upgrade
yum install emacs

history > ~/history.txt

# Common dependencies
yum install epel-release
yum install htop
yum install gcc-c++ make
yum group install "Development Tools"
# yum groupinstall development tools
yum install gettext-devel openssl-devel perl-CPAN perl-devel zlib-devel
yum install ruby
yum install bzip2-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel
yum install yum-utils
yum install xz-libs xz-devel
yum install blas blas-devel
yum install atlas-devel
yum install lapack lapack-devel
yum install libuv libuv-devel
yum install cmake28
yum install cmake
yum install libjpeg-devel
yum install libpng-devel
yum install libtiff-devel
yum install hdf5-devel
yum install geos geos-devel
yum install boost-devel libcurl libcurl-devel
yum install mercurial
yum install czmq-devel
yum install colordiff

# R
yum install texlive
yum install R -y
mkdir ~/rpms
cd ~/rpms/
wget https://download2.rstudio.org/rstudio-server-rhel-0.99.491-x86_64.rpm
yum install --nogpgcheck rstudio-server-rhel-0.99.491-x86_64.rpm
emacs /etc/rstudio/rserver.conf
emacs /etc/rstudio/rsession.conf
# R
# rstudio-server start

emacs /etc/yum.conf 

package-cleanup --oldkernels --count=2

# Setup your git
cd /var/
mkdir -p /var/aig/git
cd /var/aig/git/
git config --global user.email "x.y.z@aig.com"
git config --global user.name "xyz"
git config --global url."https://".insteadOf git://
git config --global color.ui true

# Use git
git clone https://sciencegithub.aig.net/something.git

# Share
yum install samba samba-client samba-common -y
cd /etc/samba/
cp smb.conf smb.conf.bak
## Note config change
emacs /etc/samba/smb.conf
emacs /etc/sysconfig/selinux
useradd smbuser
groupadd smbgrp
usermod -a -G smbgrp smbuser
smbpasswd -a smbuser
mkdir -p /samba/share
chown -R smbuser:smbgrp /samba/share/
chmod -R 0770 /samba/share/
systemctl enable smb.service
systemctl enable nmb.service
systemctl start smb.service
systemctl start nmb.service
service smb status
service nmb status
service --status-all
systemctl enable smb.service
systemctl enable nmb.service
service --status-all
# tail -f /var/log/samba/log.smbd 
# systemctl stop firewalld

# Install Tools
mkdir ~/src

# Redis
cd ~/src/
wget https://github.com/antirez/redis/archive/2.8.20.tar.gz
mv 2.8.20.tar.gz redis-2.8.20.tar.gz 
tar xvzf redis-2.8.20.tar.gz
cd redis-2.8.20/
make
make install
redis-cli info

# Node
cd ~/src/
wget http://nodejs.org/dist/v0.10.38/node-v0.10.38.tar.gz
tar xvzf node-v0.10.38.tar.gz
cd node-v0.10.38/
./configure 
make

# Vagrant
cd ~/src/
git clone https://github.com/mitchellh/vagrant.git
cd vagrant/
git checkout v1.7.4
rake install

# Julia
cd ~/src/
git clone https://github.com/JuliaLang/julia.git
cd julia/; git checkout v0.4.3
make
./usr/bin/julia --version
# ./julia 

# Python workspace
mkdir -p /opt/workspace/python

# Python 2.7
cd ~/src/
wget https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz
tar zxvf Python-2.7.11.tgz 
cp -R Python-2.7.11 /opt/workspace/python/python-2.7.11
cd /opt/workspace/python/python-2.7.11
./configure --prefix=/opt/workspace/python/python-2.7.11
make
make test
make altinstall
/opt/workspace/python/python-2.7.11/bin/python -m ensurepip --upgrade
/opt/workspace/python/python-2.7.11/bin/pip install --upgrade pip

# TODO Python 3.4

# Python 3.5
cd ~/src/
wget https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tgz
tar zxvf Python-3.5.1.tgz
cp -R Python-3.5.1 /opt/workspace/python/python-3.5.1
cd /opt/workspace/python/python-3.5.1
./configure --prefix=/opt/workspace/python/python-3.5.1
# ./configure --with-threads --enable-shared
make
make test
make altinstall
/opt/workspace/python/python-3.5.1/bin/pip3.5 install --upgrade pip

# Python virutalenv
git clone https://github.com/pypa/virtualenv.git
cd virtualenv/
git checkout 14.0.1
cp -R ~/src/virtualenv /opt/workspace/python/python-2.7.11/virtualenv-14.0.1
cp -R ~/src/virtualenv /opt/workspace/python/python-3.5.1/virtualenv-14.0.1
cd /opt/workspace/python/python-2.7.11/virtualenv-14.0.1
/opt/workspace/python/python-2.7.11/bin/python setup.py install
cd /opt/workspace/python/python-3.5.1/virtualenv-14.0.1
/opt/workspace/python/python-3.5.1/bin/python3.5 setup.py install
mkdir /opt/workspace/python/virtualenvs

# Virtualenv example
cd /opt/workspace/python/virtualenvs
/opt/workspace/python/python-3.5.1/bin/virtualenv --python=/opt/workspace/python/python-3.5.1/bin/python3.5 --extra-search-dir=/opt/workspace/python/python-3.5.1/bin/ py3wb01
cd /opt/workspace/python/virtualenvs/py3wb01/bin/
source ./activate
deactivate

############################################
# Python packagse for general exploration  #
############################################

# Snapshoot packages into a virtualenv
cd /opt/workspace/python/virtualenvs/py3wb01/bin/
source ./activate

pip install cython
pip install numpy
pip install scipy
pip install statsmodels
pip install matplotlib
pip install bokeh
pip install scikit-image
pip install jupyter
pip install rpy2
pip install psutil
pip install nose
pip install pymc
pip install ggplot
# There's a bug in sklearn build script; atlas changed, but the 
# build script didn't. Below is the patch.
# This will likely get resolved in the next release.
ln -s /usr/lib64/atlas/libsatlas.so /usr/lib64/atlas/libcblas.so
pip install scikit-learn

pip freeze > requirements.txt
# pip install -r requirements.txt

# As your project evolves, commit changes to requirements.txt

# ######################################################## #
# ########## TODO add tools as needed to this build ###### #
# https://github.com/josephmisiti/awesome-machine-learning #
# ######################################################## #

# Please save changes to repo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

history >> ~/history.txt

# ############################################################
# install spark
steps:
1. download latest scala, jvm, spark
2. run following commands:
cd spark-1.6.0/
sbt/sbt assembly
sbt/sbt package

if you are having trouble, watch this 5 minute video
https://www.youtube.com/watch?v=L5QWO8QBG5c

# ############################################################
# Integrate R into Jupyter notebook
#
# First, source a python virtualenv (like examples above)
# Then, run R
#
# Reference: http://ihrke.github.io/jupyter.html
# ############################################################

$ R
> install.packages(c('rzmq','repr','IRkernel','IRdisplay'), repos = c('http://irkernel.github.io/', getOption('repos')), type = 'source')
> IRkernel::installspec()

# ############################################################
# Integrate Julia into Jupyter notebook
# ############################################################
~/src/julia/julia
julia> Pkg.add("IJulia")
