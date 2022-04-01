# cat /tmp/nodes | sed '1d' |
#   jq -R 'split(" ")|{id:.[0], dc:.[2], node:.[4], drain:.[8], eligible:.[10], status:.[12]}' | jq -s

node=925b1a42
# ID        Node ID   Task Group                        Version  Desired  Status   Created     Modified
# nomad node status -short $node | sed -e '1,/Allocations/d' | sed '1d' | sort
status_out=/tmp/allocs.eude1
cat $status_out | sed -e '1,/Allocations/d' | sed '1d' | sed 's/  */ /g' | sort |
    jq -R 'split(" ")|{id:.[0], task:.[2], status:.[5]}' | jq -s
