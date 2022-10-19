for n in 01 02 03 04 05 06 07 08 09 10 11 12 app01 app02 app03 db01 db02 db03; do
    echo eu-de1-$n >> nodes.resource
    nomad node status -stats $(bash ./get_node_id.sh eu-de1-$n) | grep -A2 -i 'Host Resource'  >> nodes.resource
    ./list_tasks_on_clients.sh eu-de1-$n >> nodes.resource
done;
