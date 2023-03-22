# install decompression and progress bar dependencies
#sudo apt-get update -y
#sudo apt-get install -y zstd
#sudo apt-get install -y pv
#sudo apt-get install -y aria2

#set -x
#set -e

# bash snapshot.sh polygon-mumbai heimdall mumbai
chain=${1:?need a chain (zfs dataset): ex: polygon-mainnet} # zfs dataset
component=${2:? need a component: ex:bor}
network=${3:? need a network: ex:mainnet}

DATA=/data/$chain
HEIMDALL_DATA_DIRECTORY=/data/${chain}/heimdall/data
BOR_DATA_DIRECTORY=/data/${chain}/bor/bor/chaindata

# Goto data directory for the chain
cd $DATA

# Usage: check_substring "string1" "string2"
# Returns: 1 if string2 is a substring of string1, 0 otherwise
function check_substring {
    if [[ "$1" == *"$2"* ]]; then
        return 1
    else
        return 0
    fi
}


get_snapshot_url() {
  local network=$1
  local component=$2
  curl_output=$(curl -s https://snapshots.polygon.technology/)
  snapshot_url=$(echo "$curl_output" | grep -oE "https://[^[:space:]]+tar\.[^[:space:]]+" | sort -t ' ' -k 2,2 -r | grep $network | grep $component)
  snapshot_url="${snapshot_url%%</td>}"
  if [ -z "$snapshot_url" ]; then
    echo "Error: Snapshot URL not found for network $network and component $component" >&2
    exit 1
  fi
  echo "$snapshot_url"
}


extract_snapshot_name() {
  local url=$1
  local snapshot_name=$(basename "$url")
  echo "$snapshot_name"
}
 

# Exit if there's a mismatch between the chain data directory and the network
check_substring "$chain" "$network"
if [ $? -ne 1 ]; then
  echo "Error: network '$network' mismatch with chain '$chain'."
  exit 1
fi


if [ $component = "bor" ]; then
    data_dir=${BOR_DATA_DIRECTORY}
else
    data_dir=${HEIMDALL_DATA_DIRECTORY}
fi

SNAPSHOTURL=$(get_snapshot_url $network $component)
SNAP=$(extract_snapshot_name $SNAPSHOTURL)

# create data dir
mkdir -p $data_dir
rm -ri $data_dir/*

# Download
aria2c -x6 -s6 $SNAPSHOTURL

# Extract
pv $SNAP | tar -I zstd -xf - -C $data_dir

# Go back
cd -
