function get_node_id() {
    name=$1
    cat nodes.json | jq -r --arg name "$name" '.[$name]'
}

node=$1
echo $(get_node_id ${node})
