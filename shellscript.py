#!/bin/bash

# Define the paths
tpo_path=~/TPO
update_path=${tpo_path}/update
main_path=${tpo_path}/main
file_txt=files_md5sum.txt
file_zip=fileA.zip

# Step 1: Unzip the file
cd $update_path
unzip $file_zip

# Step 2: Check the MD5 sums
while read -r line; do
  file=$(echo $line | cut -d' ' -f2)
  expected_MD5=$(echo $line | cut -d' ' -f1)
  
  # Compute the actual MD5
  actual_MD5=$(md5sum $file | cut -d' ' -f1)
  
  # Compare the MD5s
  if [ "$expected_MD5" != "$actual_MD5" ]; then
    echo "md5sum of file $file does not match. Exit!"
    exit 1
  fi
done < $file_txt

# Step 3: Move the old files
date=$(date +%Y%m%d)
mkdir $main_path/update_$date
find $main_path -maxdepth 1 -type f -exec mv {} $main_path/update_$date/ \;

# Step 4: Move the new files
mv $update_path/* $main_path/
rm $main_path/$file_txt

# Step 5: Run the command
if [ -x "$tpo_path/softwareCommand" ]; then
    sudo $tpo_path/softwareCommand
else
    echo "softwareCommand not found or not executable"
    exit 1
fi

# Step 6: Remove all files from the update folder
rm -r $update_path/*

# Step 7: Print the message
echo $(date)
echo "new update deployed and system restarted"
