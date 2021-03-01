#!/bin/bash
path=$1
if [ -d ./list ];then
        echo "list exist"
else
        mkdir list
fi
find ${path}/*.tif > list/test.txt
