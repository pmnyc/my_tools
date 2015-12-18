#!/usr/bin/env bash
# This script install PhantomJS in your Debian/Ubuntu System
#

#####################################
# This script must be run as root:
# sudo sh install_phantomjs.sh
#####################################

sudo apt-get install -y libxss1 libappindicator1 libindicator7 xvfb
sudo apt-get install -y xserver-xephyr tightvncserver
sudo apt-get install -y build-essential g++

sudo apt-get install -y flex bison gperf ruby perl
sudo apt-get install -y libsqlite3-dev
sudo apt-get install -y libfontconfig1-dev

sudo apt-get install -y libicu-dev libfreetype6 libssl-dev libpng-dev libjpeg-dev
sudo apt-get install -y libx11-dev libxext-dev

git clone --recurse-submodules git://github.com/ariya/phantomjs.git
cd phantomjs
./build.py

cp bin/phantomjs /usr/bin/

# The following is the symbolink bin/phantomjs into the other folders
# sudo ln -sf bin/phantomjs /usr/local/share/phantomjs
# sudo ln -sf bin/phantomjs /usr/local/bin/phantomjs
# sudo ln -sf bin/phantomjs /usr/bin/phantomjs
