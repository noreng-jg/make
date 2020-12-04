#!/bin/bash

cur=$(pwd)
read -ep 'Enter password: ' password
hashed_pass=$(printf $password | sha256sum | awk '{ print $1 }')
scenario_folder=make/scenarios/
cd $scenario_folder
echo 'Choose scenario: '
read -ep '<TAB> to search within: ' scenario
cd $cur

read -p "This will reset all your database content, are you sure? [yY] " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
python3 make/db_reset.py
cat $scenario_folder$scenario | xargs -0 echo | python3 make/cascade_insertion.py $hashed_pass 
fi
