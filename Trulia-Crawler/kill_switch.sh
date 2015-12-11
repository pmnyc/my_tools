#!/usr/bin/env 

# @author: Man Peng

# This program is for deleting all downloaded data
# USE with EXTREME CAUTION

echo 
read -p "Want to delete All downloaded data?" -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # do dangerous stuff
    # ask again to make sure
    echo 
    read -p "ARE YOU SURE??? It IS VERY DANGEROUS!!!" -n 1 -r
    echo 
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        # do really dangerous stuffs
        rm -rf log/
        rm -rf app/data/*
        rm -rf output_bucket/*
        rm -f queue/all_links_cached.csv
        echo > queue/links_crawled_queue.csv
        echo > queue/cities_done_with_property_link_extraction.txt
        echo > queue/city_list.txt
        python cleanup.py
    fi
fi
