#!/bin/bash
#
#set -ex

network=${1:? network : mainnet}
component=${2:? component: bor}

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

snapshoturl=$(get_snapshot_url $network $component)
echo "$snapshoturl"

snapshot_name=$(extract_snapshot_name $snapshoturl)
echo $snapshot_name
