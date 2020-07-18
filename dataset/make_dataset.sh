#!/bin/sh

echo "Make datasets for bridge_bidding_RL"

echo "Start to make training datasets"
for i in `seq 0 24`
do
    echo "Start $i"
    python make_dataset.py $i
done


echo "Start to make an evaluation dataset"
python make_dataset.py 25

echo "Done!"
