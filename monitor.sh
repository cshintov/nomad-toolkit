nexec () {
        task=$1
        allocid=$2
        cmd=$3
        nomad alloc exec -i -t -task $task $allocid $cmd
}

nlsa () {
        chain=$1
        nomad job allocs $chain | sed 1d | grep --color -v stop | cut -d' ' -f1-3
}

job='solana-devnet'

allocs=$(nlsa $job | cut -d' ' -f1)
command="solana-validator --ledger /data/solana-ledger monitor"

for alloc in $allocs; do
    echo $alloc
    nomad alloc exec -i -t -task $job $alloc $command
done;
