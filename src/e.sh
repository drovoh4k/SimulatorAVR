#!/bin/bash

file='test_1/test'
# file='test_1/test'

avra $(pwd)/tests/$file.asm

echo
echo "CODE EXECUTION:"
echo 

./simavr $(pwd)/tests/$file.hex -tr