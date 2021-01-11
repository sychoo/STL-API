#!/bin/bash

# store the directory where the user invoked the stl command
exec_dir="$(pwd)"
cd $(dirname $0)

stllex < test.txt
