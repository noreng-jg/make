#!/bin/bash
password=senha
read -p "This will reset all your database content, are you sure? [yY] " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
python3 make/db_reset.py
python3 make/cascade_insertion.py $(printf $password | sha256sum | awk '{ print $1 }')
fi
