#!/bin/bash
while read name S; do python3 stabcover.py "$name" "$S" 12; done < stab_specs2.txt
