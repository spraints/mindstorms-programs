#!/bin/bash
#/ Usage: ./sync.sh [-m MESSAGE]

set -e
set -o nounset

set -x
mind-meld mindstorms fetch --git refs/heads/mindstorms "$@"
git push origin mindstorms
