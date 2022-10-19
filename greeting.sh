# for node in $(cat nodes-running-chains.txt.new); do
#     echo $node
#     ssh shinto.cv@$node sudo run-parts /etc/update-motd.d | grep Memory
#     echo
# done

for node in $(cat nodes-running-chains.txt.new); do
    echo $node
    ssh shinto.cv@$node sudo run-parts /etc/update-motd.d | grep -i cpu
    echo
done
