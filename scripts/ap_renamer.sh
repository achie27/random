#!/bin/bash

# Context
# A lot of my anime*ahe.com (I see the fallacy in trying to hide this, but ehh) downloads had filenames like this -
# http-__c01.g*share.com_files_0_tg279vrkdytveg_Anime*ahe_Bakemonogatari_-_05_BD_720p_TenB.mp4. 
# That looked ugly and video players would create a randomly ordered playlist which was un-bingeable.
# This script essentially renames the files to not have anything before Anime*ahe.
# So, the file from earlier would be renamed to Anime*ahe_Bakemonogatari_-_05_BD_720p_TenB.mp4.

# Usage
# THE_SITE=Anime*ahe ./ap_renamer.sh /path/to/the/directory [/another/directory]...

# Example
# THE_SITE=Anime*ahe ./ap_renamer.sh /home/me/anime/Bakemonogatari /home/me/anime/Nisemonogatari

function substring_exists () {
  str=$1
  substr=$2
  tmp="${str#*$substr}"
  [[ "${#tmp}" == "${#str}" ]] && echo 0 || echo 1
}

function process_dirs () {
  for ap_videos_dir in "$@"
  do
    all_files=$(ls "$ap_videos_dir")
    for f in $all_files
    do
      ap_exists_in_name=$(substring_exists $f $THE_SITE)
      
      if [ $ap_exists_in_name == "1" ]
      then
        new_file_name="$THE_SITE${f#*$THE_SITE}"
        
        new_file_path="$ap_videos_dir/$new_file_name"
        cur_file_path="$ap_videos_dir/$f"

        mv "$cur_file_path" "$new_file_path"
      fi
    done
  done
}

process_dirs "$@"