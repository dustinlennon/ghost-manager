#!/bin/bash

if [ -f .env ]; then
  while IFS= read -r line; do
    if echo $line | egrep -q -v "^#.*$"; then
      eval export $(eval echo $line)
    fi   
  done < .env
fi

exec "/bin/bash" "--noprofile" "--rcfile" ".ghostpubrc"