source .bashrc
cd GAForD
conda activate gaford

DIR=/home/vidnerova/GAForD/data/BA/
#nodes=$1
#density=$2
#rew=$3
#sim=$4

for k in `seq 0 9`
do
    python main.py  ${DIR}/BA_nNodes${nodes}_density${density}.p ${sim} > BA_nNodes${nodes}_density${density}_sim${sim}_${k}.log 
done
