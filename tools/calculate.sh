#!/bin/bash
# User: linhaobuaa
# Date: 2015-01-09 21:00:00
# Version: 0.1.0
# calculate

export DATETIME="$(date "+%Y-%m-%d_%H-%M-%S")"
echo $DATETIME
python post_filter.py >> run.log
python rubbish_filter.py >> run.log
python cut_word.py >> run.log
python sentiment_cal.py >> run.log
python stat.py >> run.log
python hot_sort.py >> run.log
python rel_sort.py >> run.log
python sensitive_sort.py >> run.log
python recommend.py >> run.log
export DATETIME="$(date "+%Y-%m-%d_%H-%M-%S")"
echo $DATETIME
