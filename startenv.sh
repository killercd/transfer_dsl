#!/bin/bash
#pip3 install virtualenv

if [[ ! -d "dsltransfer" ]];
then
    virtualenv dsltransfer
fi
source dsltransfer/bin/activate
pip3 install ply
 

