#!/bin/bash

set -eEu
set -o pipefail

################################################################
### Define the env config we expect the calling host to use ####
################################################################

. cicd/functions.sh

# what is our python path? 
# what is the url of our image store?
