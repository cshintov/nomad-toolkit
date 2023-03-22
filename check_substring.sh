#!/bin/bash
#
set -x

function check_substring {
    # Usage: check_substring "string1" "string2"
    # Returns: 1 if string2 is a substring of string1, 0 otherwise
    if [[ "$1" == *"$2"* ]]; then
        return 1
    else
        return 0
    fi
}

# Test cases
check_substring "polygon-mumbai" "mumbai"
echo "Expected: 1, Actual: $?"

#check_substring "polygon-mumbai" "delhi"
#echo "Expected: 0, Actual: $?"

#check_substring "foo" "foo"
#echo "Expected: 1, Actual: $?"

#check_substring "foo" ""
#echo "Expected: 1, Actual: $?"

