DIR=/mnt/data7T/vidnerova/GAforD_data/LRM_ER_rewired/
density=$2
nodes=$1
for rew in `seq 0 3`
do
    for sim in `seq 0 38`
    do
	pids=()
	for k in `seq 0 9`
	do
	    python main.py  ${DIR}/LRM_ER_nNodes${nodes}_density${density}_rew${rew}.p ${sim} > LRM_ER_nNodes${nodes}_density${density}_rew${rew}_sim${sim}_${k}.log &
	    pids[${k}]=$!
	done
	for pid in ${pids[*]}; do
	    wait $pid
	done
    done
done
