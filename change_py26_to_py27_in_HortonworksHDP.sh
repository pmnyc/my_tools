#!/bin/bash

yum install -y nano centos-release-scl zlib-devel \
		bzip2-devel openssl-devel ncurses-devel \
		sqlite-devel readline-devel tk-devel \
		gdbm-devel db4-devel libpcap-devel xz-devel \
		libpng-devel libjpg-devel atlas-devel;
		
yum groupinstall "Development tools" -y;

yum install -y python27;

source /opt/rh/python27/enable;

echo 'source /opt/rh/python27/enable;' >> .bashrc;

wget https://bootstrap.pypa.io/ez_setup.py -O - | python
easy_install-2.7 pip
pip install --upgrade pip

pip install --upgrade numpy scipy \
		pandas scikit-learn tornado pyzmq \
		pygments matplotlib jinja2 jsonschema

pip install jupyter


# Start the Jupyter Notebook
# nano ~/start_jupyter.sh
	# and add the following content to it.

#source /opt/rh/python27/enable
#IPYTHON_OPTS="notebook --port 8889 \
#--notebook-dir='/usr/hdp/current/spark-client/' \
#--ip='*' --no-browser" pyspark
#chmod +x ~/start_jupyter.sh
#./start_jupyter.sh
