echo "train - 1 flow(s)"
python3 gen_train_nnx.py 1 -o tr1.csv &
python3 gen_train_nnx.py 1 -o tr2.csv &
wait
echo "train - 2 flows"
python3 gen_train_nnx.py 2 -o tr3.csv &
python3 gen_train_nnx.py 2 -o tr4.csv &
wait
echo "train - 3 flows"
python3 gen_train_nnx.py 3 -o tr5.csv &
python3 gen_train_nnx.py 3 -o tr6.csv &
wait
echo "train - 4 flows"
python3 gen_train_nnx.py 4 -o tr7.csv &
python3 gen_train_nnx.py 4 -o tr8.csv &
wait
echo "train - 5 flows"
python3 gen_train_nnx.py 5 -o tr9.csv &
python3 gen_train_nnx.py 5 -o tr10.csv &
wait
python3 merge_csv.py tr1.csv tr2.csv tr3.csv tr4.csv tr5.csv tr6.csv tr7.csv tr8.csv tr9.csv tr10.csv train_data.csv
rm -rf tr[1,2,3,4,5,6,7,8,9,10].csv



counter=0
PROCS=6
for flows in 1 2 3 4 5 6 7 8 9 10 15 20 25 50 75 100
do
    echo "test: $flows flow(s)"
    for run in {1..10}
    do
        python3 gen_test_nnx.py $flows -o t$run.csv &
        counter=$counter+1
        if ! (( counter % PROCS ))
        then
            wait
        fi
    done
    python3 merge_csv.py t1.csv t2.csv t3.csv t4.csv t5.csv t6.csv t7.csv t8.csv t9.csv t10.csv test_data_$flows\_flow.csv
    rm -rf t[1,2,3,4,5,6,7,8,9,10].csv
done