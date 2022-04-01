function print_array() {
  for item in $*; do
      echo $item
  done;
}

# get all the nodes
function get_nodes() {
  nodes=$(nomad node status | cut -d' ' -f1 | sed '1d')
  print_array $nodes
}

# list tasks running on one node
function tasks_on_node() {
    node=$1
    tasks=$(nomad node status -short $node | sed -e '1,/Allocations/d' | sed '1d' | cut -d' ' -f5 | sort)
    print_array $tasks
}

# get_nodes
# tasks_on_node 00d472b7

# 925b1a42 = eu-de1-01
tasks_on_node 925b1a42
