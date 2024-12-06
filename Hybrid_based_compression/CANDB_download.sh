#!/bin/bash

candb_id="1AgLfR-Cr5AjzHj8RqQ-5N6aMcnqe-VsT"
candb_name="2022_09_06_12_30_06.txt"


wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1xQFy3qg-cXPRrkqJ0VvqSxBHT1N4y8Fg' -O prep_eval.txt

wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1vp2LopcU1os36Z7OLUu6td8MrSi83W_z' -O 2022_09_06_12_50_48.txt


curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id=${candb_id}" > /dev/null
code="$(awk '/_warning_/ {print $NF}' /tmp/cookie)"
curl -Lb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${code}&id=${candb_id}" -o ${candb_name}
