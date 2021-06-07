#!/bin/bash
services='. api/ ../ssh ../cli ../agent'

for service in $services
do
echo "Running go mod tidy in  the $service service ..."
cd $service
echo "Current location: $(pwd)"
go mod tidy
done
