#!/bin/bash
#/ Usage: ./sync.sh [-m MESSAGE]

set -e
set -o nounset

set -x
mind-meld mindstorms diff refs/heads/mindstormmindstorms
