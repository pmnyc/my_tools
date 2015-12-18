#!/usr/bin/env bash
# This script install PhantomJS in your Debian/Ubuntu System
#
#####################################
# This script must be run as root:
# Sample:
#  python main.py --town 1 --startpage 1 --save_html --save_snapshot
#####################################
#

python main.py --town 1 --startpage 1 --save_html # NEEDS TO CHANGE THIS COMMAND LINE FOR EVERY JOB

## Upload files to S3, only works in Linux, skip if it is run on Windows
cp utils/s3upload.py .

python s3upload.py

rm s3upload.py

zip -r log.zip ./log/
zip -r cache.zip ./cache/
zip -r output_results.zip ./postprocess_output/
