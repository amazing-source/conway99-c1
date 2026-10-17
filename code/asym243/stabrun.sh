#!/bin/bash
while read name S; do python3 stabcover.py "$name" "$S" 3; done < stab_specs.txt
