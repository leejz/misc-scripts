#!/bin/bash

cat $1 | while IFS= read L; do if [[ $L == \>* ]]; then echo "$L"; else echo $L | rev | tr "ATGCatgc" "TACGtacg"; fi; done > $2
