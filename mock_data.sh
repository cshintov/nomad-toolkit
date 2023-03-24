#!/bin/bash

# Define the mock data
mock_data=(
    "5.19.62.237,eu-de1-db01,/data/eth-main,1000000000"
    "5.19.62.237,eu-de1-db01,/data/eth-main-archive,2000000000"
    "5.19.62.237,eu-de1-db01,/data/celo-test,3000000000"
    "5.19.105.5,eu-de1-db02,/data/celo-archive,4000000000"
    "5.19.4.189,eu-de1-db03,/data/polygon-main,5000000000"
    "5.8.64.67,eu-de1-app01,/data/polygon-mumbai,6000000000"
)

# Loop through the mock data and print it to stdout
for data in "${mock_data[@]}"
do
    echo $data
done

