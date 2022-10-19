toolkit=/Users/shinto/Tatum/repos/nomad-toolkit

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

function get_nodes_json() {
  # cat /tmp/nodes | 
  nomad node status |
    sed '1d' | sed 's/  */ /g' |
    jq -R 'split(" ")|{id:.[0], dc:.[1], node:.[2], drain:.[4], eligible:.[5], status:.[6]}' | 
    jq -s
}

# list tasks running on one node
function tasks_on_node() {
    node=$1
    tasks=$(nomad node status -short $node | sed -e '1,/Allocations/d' | sed '1d' | cut -d' ' -f5 | sort)
    print_array $tasks
}

function tasks_on_node_json() {
  # cat /tmp/allocs.eude1 | 
  node=$1
  nomad node status -short $node |
    sed -e '1,/Allocations/d' | sed '1d' | sed 's/  */ /g' | sort |
    jq -R 'split(" ")|{id:.[0], task:.[2], status:.[5]}' | 
    jq -s
}

function get_node_id() {
    name=$1
    echo xxxx $name
    echo $(jq -r --arg name "$name" '.[$name]')
    cat $toolkit/nodes.json | jq -r --arg name "$name" '.[$name]'
}

# nodeid=$(get_node_id eu-de1-01)
# echo $nodeid

# creates files for each node in `tasks` dir with the tasks listed
function get_tasks_on_nodes() {
    readarray -t nodes <<< $(get_nodes_json | jq -c '.[]')
    for item in ${nodes[@]}; do
      echo $item
      node=$(echo $item | jq -r '.node')
      id=$(echo $item | jq -r '.id')
      tasks_file=tasks/$node.tasks

      cat > $tasks_file <<EOF
node: $node 

id: $id 

=====
tasks:

$(tasks_on_node $id)
EOF

    done
}

# 925b1a42 = eu-de1-01
# tasks_on_node 925b1a42

# get_nodes_json
# tasks_on_node_json 925b1a42
# tasks_on_node_json 4485843e

# tasks_on_node b68d9175
# tasks_on_node_json b68d9175

# get_tasks_on_nodes
# tasks_on_node 4c35bcfb #a7da23c7 #a7bd474c #7c95032b #1e43affe #5ded9d28 #e48acec4


# node=$1
# tasks_on_node $(get_node_id ${node})
tasks_on_node 12757e42 
