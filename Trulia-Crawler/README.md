# Web-Crawler for Trulia.com


## Description

- This tool's development is at design stage.
- The output is in json format.
- This program is written in Python.
- Anaconda Python package distribution is recommended. The Python version recommended is 2.7.
- The main parameters for tuning the program are in **config/parameters.py**. The meanings of parameters are documented in parameters like document_1, document_2.
- The README file mainly uses Worcester, MA as the pilot city to test code.


## Initialization

- Run `$ pip install scrapy` to install scrapy. If you are using Anaconda, you can also use `$ conda install scrapy` to install.
- Run `$ scrapy startproject trulia_crawler` to start the project folder `trulia_crawler` with some initial files.
- Run `$ scrapy genspider baseTrulia www.trulia.com` to create the first spyder `baseTrulia` for Trulia.com.
  - To see the list of spyders you have or created, run `$ scrapy list` to check.
  - To test the code objects in an interactive shell while writing the program, you may use `$ scrapy shell http://www.trulia.com/homes/Massachusetts/Worcester/sold/1779200-61-Edgeworth-St-Worcester-MA-01605`  This feature can be used for testing the codes in the parse_item function it the corresponding spyder class.
  - The file `items.py` defines the info that will be exported in the output.
- The Google Maps API key, smallest mesh-grid size are stored/defined in the file **config/parameters.json**.
  - To obtain the Google Maps API key, one needs to register on [Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding/intro)

## Packages Required

- Python packages needed for using this tool are

```python
scrapy
OpenSSL, requests, twisted, urllib, argparse, datetime, fnmatch, time, json, lxml, numpy
```

## Test

- Run `$ scrapy crawl Trulia_Base` to test whether spyder works or not. If not, try the following to debug...
- Run `$ scrapy parse http://www.trulia.com/homes/Massachusetts/Worcester/sold/1779200-61-Edgeworth-St-Worcester-MA-01605 -c parse_item` to test whether the specific spyder works or not, where the callback function `parse_item` in `-c parse_item` is a parser (i.e. callback) function in the base spyder.
  - To check out the helps on the usage of scrapy command line tool, run `$ scrapy parse -h` to see what options are available.
- The program in the file *utils/rotate_user_agent.py* uses random user agents to "trick" Trulia to think the browsing request was from different web browsers, and this measure is used for avoiding the website to ban my IP.
- For a base spyder **Trulia_by_url**, run `$ scrapy crawl Trulia_by_url --nolog -a start_url="http://www.trulia.com/property/3210700881-6-Bayberry-Ln-Worcester-MA-01602"` to check crawling results, where `--nolog` specifies no log on screen. Add `-o output.json` to export the web-crawling result to the output json file.

## Instructions

- The data of all links for each city/town are stored in the file **queue/city_list.txt**. The list of links depends on the date when it is generated, and is tagged with key being this date.
  - The *city_list.txt* file for listing cities we need to process is of the format
<br /> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Worcester, MA
<br /> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; shrewsbury,ma
<br /> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ......

## Usage

- Run `$ python generate_links_by_city.py` to extract property link addresses in Trulia through geomesh.
  - Put the list of cities in the file **queue/city_list.txt**. These are also the only cities we'll run web-crawling for.
  - The output that contains the list of http addresses for the properties in the city are stored in the folder specified in the file **config/parameters.json** with key *property_webpage_link_storeage_folder*.
  - Run `$ python refill_weblinks_from_cache.py` to fill in the missing webpage links for the cities (e.g. files such as worcester_ma.json in folder app/data/) from the cached links file queue/all_links_cached.csv. This needs to be after the first round of getting files for webpage links through $ python generate_links_by_city.py command.
  - Run `$ python organize_city_list.py` if you are not done with the whole state for webpage links extraction, say, in MA. This can help move the list of cities in the state that were processed into the file queue/cities_done_with_property_link_extraction.txt so that the queue/city_list.txt file only has the cities that need to continue running geomesh.

- Run `$ python crawl_trulia.py -c "Worcester, MA" -l False -n 300` to run web-crawling on the property webpages to scrape proprety information on them.
  - Option -c specifies the city to run.
  - Options -l and -n are optional.
  - Option -l is boolean specifying whether to run geomesh to get all http links for the city or not. Default value is False assuming one already ran `$ python generate_links_by_city.py ***` before.
  - Option -n specifies how many properties in the property http-links file (given the city) to run. Default value is large enough to run all links.
  - Scraped property results in json format are exported to **output_bucket** folder.
- Run `$ python cleanup.py` to clean up the temporary files created after the program was run.
- Run `$ python create_property_status_from_weblinks.py -c "Worcester,MA"` to create the file containng property status for all properties in Worcester. You may change the city on which you want to run this command by providing it in the option -c. The property status must be one of the three types, "For Sale", "Sold" and "Foreclosure".

## Features & Functionalities
- If one wants to parse the scraped information from a property webpage in Python, use `>>> import app.parser_for_property_json`. To get to know more about the details of using the features of this parser, run `>>> help(app.parser_for_property_json)` to check out sample usage and description.
- The folder **special_tasks** contains the programs for specific jobs, e.g.
  - The program getSquareFootage.py is for extracting the square footage information from the json files containing the property information, and export the output by address to a csv file.

## Output & Log Storage
- The http links for properties processed by city are stored in folder `app/data`.
- The json files for scraped webpages are stored in the folder `output_bucket`.
- The http links that were successfully processed are stored in the file `queue/links_crawled_queue.csv`.
- All http links found during the geomesh program are cached in the file specified in the parameter **all_links_cached** in the parameter setting file config/parameters.json. Currently the cached links are stored in the specified file `queue/all_links_cached.csv`. To restart caching all links, simply delete the all_links_cached file.
- Logs are stored in `log` folder.
  - The log folder and log files in it can be deleted at any time without affecting the program. This will only lose log information.
- To restart everything including deleting all downloaded data, you may run `$ bash kill_switch.sh` to clear everything.
  - This functionality is only compatitable with UNIX-like OS.
  - This is VERY DANGEROUS if you are in the middle of a web-cralwing process. You need to know what you are doing before running this kill switch.
