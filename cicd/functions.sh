#!/bin/bash

set -eEu
set -o pipefail

#########################################################
### Define reusable base functions for CI/CD scripts ####
#########################################################

err() {
	print "[ERROR]"
}
