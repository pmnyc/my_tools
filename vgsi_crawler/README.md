# Web-Crawler for vgsi.com

## Description
Developer: Man Peng

This tool is for extracting the building/parcel information for both residential and commercial buildings from vgsi.com. The output is in json format.

VGSI is a supplier of land parcel management software technology and services to local government organizations.

For example, in RI, the towns VGSI collects data for are [these (click here)](http://www.vgsi.com/vision/Applications/ParcelData/RI/Home.aspx)

## Instructions
The instruction for running on Linux is specific for Ubuntu.
* If one runs the program on Linux (Ubuntu 14.04.3 LTS) command line interface, i.e. running browser headless without displaying what is happening on browser, install the packages by executing `bin/install_prerequisite.sh` and `bin/install_phantomjs.sh`. The program code detects system platform and determine how to run python package selenium.
* The EC2 instance recommended to run the program is m3.medium. The program needs good network connection.
* Currently, this program only supports two browsers, Firefox and PhantomJS.
    * FireFox is used for testing purpose to see the live actions through simulating clicks. PhantomJS is used for official execution for the program to run in the background headlessly.
    * PhantomJS latest stable version is 2.0. Unfortunately, it stops supporting Python in future. Current stable version is still able to perform most of jobs.
    * PhantomJS can be [downloaded here](http://phantomjs.org/download.html). Windows installation is by a straightforward unzip. For Linux, it needs to be compiled from source codes. (It may take more than 40 mins to finish compilation)
    * For Linux and Mac, [check out here](http://phantomjs.org/build.html) for compiling from source codes.
* Change the starting link _web_link_start_ for each state in the file **./conf/settings.json**. For example, for RI, the starting link is _http://www.vgsi.com/vision/Applications/ParcelData/RI/Home.aspx_
* Change the browser between Firefox and PhantomJS in the file `config/settings`.
* To run a specific job, change parameters in the file `crawler_exe.sh`. The specification of it is as follows:
    * For example, the command line is `python main.py --town 1 --startpage 1 --save_html --save_snapshot`
    * Option **--town value** must be provided.
    * If **--startpage** is not provided, then its default value is 1.
    * If **--save_html** is not provided, then default is no saving of html file of webpage.
    * If **--save_snapshot** is not provided, then default is no saving of snapshot of webpage.

## Specifications
* `utils/loginpage_webbrowser.py`. The parameters for running this program are as follows:
    * town_order: Specify the town (town_order) for each state, it processes all the parcels for this town.
    * startpage: Specify which page to start in that town's webpage. Default value is 1. If somehow network failed and one wants restart process from that page on, set that page number here. For example, there are 322 pages for the town, but the program stops at page 123, set this startpage=123 so that it will continue with the rest of pages.
    * save_html: Boolean. Specify whether we save html cache or not.
    * save_snapshot: Boolean. Specify whether we take snapshot of the webpages.
    * browser: Specify which browswer to use, it is either PhantomJS or Firefox
* `bin/clearRAM.sh`: run this bash script to clean the cached memory if needed.
* `bin/clearAll.sh`: run this bash script to clear all temp files that we won't need.
* `app/parser.py`: this is the main parser for scraping the parcel information from the parcel's webpage.
* `bin/install_phantomjs.sh`: run this bash script to install phantomjs in Linux
* In Windows, after installing PhantomJS (latest stable version is 2.0), use the location of `bin/phantomjs.exe` file to specify the `webdriver.PhantomJS(executable_path=<phantomjs.exe location>)` when using Python's `selenium` package.
* The parsing of the webpages is in `app/parser.py`.
* As of Dec 2015, there are 322 pages for Charlestown, RI and 1657 pages for Cranston, RI.
* To test the speed of internet on Linux instance, one may run the following:
```shell
    wget -O speedtest-cli https://raw.github.com/sivel/speedtest-cli/master/speedtest_cli.py
    chmod +x speedtest-cli
    ./speedtest-cli
```
