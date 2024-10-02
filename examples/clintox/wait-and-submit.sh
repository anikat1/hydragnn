#!/bin/bash
KEY=$1
[ -z $KEY ] && KEY=debug

wait_and_exec () {
    while true; do
        JOBCNT=`sqs | grep $KEY | wc -l`
        if [ $JOBCNT -eq 0 ]; then
            echo ">>> No job in the debug queue. Good to go."
            "$@"
            ## Need time after submission
            sleep 3
            break
        else
            echo ">>> $JOBCNT job(s) in the deqbug queue. Sleep."
            sleep 60
        fi
    done
}

# 10 jobs will be submitted in total
for i in `seq 5`; do
    wait_and_exec sbatch -q debug job-fulltrain.sh
done
