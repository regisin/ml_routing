# echo "train - 1 flow"
# python3 gen_train_nnx.py 1 -o tr1.csv &
# python3 gen_train_nnx.py 1 -o tr2.csv &
# wait
# echo "train - 2 flows"
# python3 gen_train_nnx.py 2 -o tr3.csv &
# python3 gen_train_nnx.py 2 -o tr4.csv &
# wait
# echo "train - 3 flows"
# python3 gen_train_nnx.py 3 -o tr5.csv &
# python3 gen_train_nnx.py 3 -o tr6.csv &
# wait
# echo "train - 4 flows"
# python3 gen_train_nnx.py 4 -o tr7.csv &
# python3 gen_train_nnx.py 4 -o tr8.csv &
# wait
# echo "train - 5 flows"
# python3 gen_train_nnx.py 5 -o tr9.csv &
# python3 gen_train_nnx.py 5 -o tr10.csv &
# wait
# python3 merge_csv.py tr1.csv tr2.csv tr3.csv tr4.csv tr5.csv tr6.csv tr7.csv tr8.csv tr9.csv tr10.csv train_data.csv
# rm -rf tr[1,2,3,4,5,6,7,8,9,10].csv














# echo "test - 1 flow"
# python3 gen_test_nnx.py 1 -o t1.csv &
# python3 gen_test_nnx.py 1 -o t2.csv &
# python3 gen_test_nnx.py 1 -o t3.csv &
# python3 gen_test_nnx.py 1 -o t4.csv &
# python3 gen_test_nnx.py 1 -o t5.csv &
# wait
# python3 gen_test_nnx.py 1 -o t6.csv &
# python3 gen_test_nnx.py 1 -o t7.csv &
# python3 gen_test_nnx.py 1 -o t8.csv &
# python3 gen_test_nnx.py 1 -o t9.csv &
# python3 gen_test_nnx.py 1 -o t10.csv &
# wait
# python3 merge_csv.py t1.csv t2.csv t3.csv t4.csv t5.csv t6.csv t7.csv t8.csv t9.csv t10.csv test_data_1_flow.csv
# rm -rf t[1,2,3,4,5,6,7,8,9,10].csv


# echo "test - 2 flows"
# python3 gen_test_nnx.py 2 -o t1.csv &
# python3 gen_test_nnx.py 2 -o t2.csv &
# python3 gen_test_nnx.py 2 -o t3.csv &
# python3 gen_test_nnx.py 2 -o t4.csv &
# python3 gen_test_nnx.py 2 -o t5.csv &
# wait
# python3 gen_test_nnx.py 2 -o t6.csv &
# python3 gen_test_nnx.py 2 -o t7.csv &
# python3 gen_test_nnx.py 2 -o t8.csv &
# python3 gen_test_nnx.py 2 -o t9.csv &
# python3 gen_test_nnx.py 2 -o t10.csv &
# wait
# python3 merge_csv.py t1.csv t2.csv t3.csv t4.csv t5.csv t6.csv t7.csv t8.csv t9.csv t10.csv test_data_2_flow.csv
# rm -rf t[1,2,3,4,5,6,7,8,9,10].csv


# echo "test - 3 flows"
# python3 gen_test_nnx.py 3 -o t1.csv &
# python3 gen_test_nnx.py 3 -o t2.csv &
# python3 gen_test_nnx.py 3 -o t3.csv &
# python3 gen_test_nnx.py 3 -o t4.csv &
# python3 gen_test_nnx.py 3 -o t5.csv &
# wait
# python3 gen_test_nnx.py 3 -o t6.csv &
# python3 gen_test_nnx.py 3 -o t7.csv &
# python3 gen_test_nnx.py 3 -o t8.csv &
# python3 gen_test_nnx.py 3 -o t9.csv &
# python3 gen_test_nnx.py 3 -o t10.csv &
# wait
# python3 merge_csv.py t1.csv t2.csv t3.csv t4.csv t5.csv t6.csv t7.csv t8.csv t9.csv t10.csv test_data_3_flow.csv
# rm -rf t[1,2,3,4,5,6,7,8,9,10].csv


# echo "test - 4 flows"
# python3 gen_test_nnx.py 4 -o t1.csv &
# python3 gen_test_nnx.py 4 -o t2.csv &
# python3 gen_test_nnx.py 4 -o t3.csv &
# python3 gen_test_nnx.py 4 -o t4.csv &
# python3 gen_test_nnx.py 4 -o t5.csv &
# wait
# python3 gen_test_nnx.py 4 -o t6.csv &
# python3 gen_test_nnx.py 4 -o t7.csv &
# python3 gen_test_nnx.py 4 -o t8.csv &
# python3 gen_test_nnx.py 4 -o t9.csv &
# python3 gen_test_nnx.py 4 -o t10.csv &
# wait
# python3 merge_csv.py t1.csv t2.csv t3.csv t4.csv t5.csv t6.csv t7.csv t8.csv t9.csv t10.csv test_data_4_flow.csv
# rm -rf t[1,2,3,4,5,6,7,8,9,10].csv


# echo "test - 5 flows"
# python3 gen_test_nnx.py 5 -o t1.csv &
# python3 gen_test_nnx.py 5 -o t2.csv &
# python3 gen_test_nnx.py 5 -o t3.csv &
# python3 gen_test_nnx.py 5 -o t4.csv &
# python3 gen_test_nnx.py 5 -o t5.csv &
# wait
# python3 gen_test_nnx.py 5 -o t6.csv &
# python3 gen_test_nnx.py 5 -o t7.csv &
# python3 gen_test_nnx.py 5 -o t8.csv &
# python3 gen_test_nnx.py 5 -o t9.csv &
# python3 gen_test_nnx.py 5 -o t10.csv &
# wait
# python3 merge_csv.py t1.csv t2.csv t3.csv t4.csv t5.csv t6.csv t7.csv t8.csv t9.csv t10.csv test_data_5_flow.csv
# rm -rf t[1,2,3,4,5,6,7,8,9,10].csv


# echo "test - 6 flows"
# python3 gen_test_nnx.py 6 -o t1.csv &
# python3 gen_test_nnx.py 6 -o t2.csv &
# python3 gen_test_nnx.py 6 -o t3.csv &
# python3 gen_test_nnx.py 6 -o t4.csv &
# python3 gen_test_nnx.py 6 -o t5.csv &
# wait
# python3 gen_test_nnx.py 6 -o t6.csv &
# python3 gen_test_nnx.py 6 -o t7.csv &
# python3 gen_test_nnx.py 6 -o t8.csv &
# python3 gen_test_nnx.py 6 -o t9.csv &
# python3 gen_test_nnx.py 6 -o t10.csv &
# wait
# python3 merge_csv.py t1.csv t2.csv t3.csv t4.csv t5.csv t6.csv t7.csv t8.csv t9.csv t10.csv test_data_6_flow.csv
# rm -rf t[1,2,3,4,5,6,7,8,9,10].csv


# echo "test - 7 flows"
# python3 gen_test_nnx.py 7 -o t1.csv &
# python3 gen_test_nnx.py 7 -o t2.csv &
# python3 gen_test_nnx.py 7 -o t3.csv &
# python3 gen_test_nnx.py 7 -o t4.csv &
# python3 gen_test_nnx.py 7 -o t5.csv &
# wait
# python3 gen_test_nnx.py 7 -o t6.csv &
# python3 gen_test_nnx.py 7 -o t7.csv &
# python3 gen_test_nnx.py 7 -o t8.csv &
# python3 gen_test_nnx.py 7 -o t9.csv &
# python3 gen_test_nnx.py 7 -o t10.csv &
# wait
# python3 merge_csv.py t1.csv t2.csv t3.csv t4.csv t5.csv t6.csv t7.csv t8.csv t9.csv t10.csv test_data_7_flow.csv
# rm -rf t[1,2,3,4,5,6,7,8,9,10].csv


# echo "test - 8 flows"
# python3 gen_test_nnx.py 8 -o t1.csv &
# python3 gen_test_nnx.py 8 -o t2.csv &
# python3 gen_test_nnx.py 8 -o t3.csv &
# python3 gen_test_nnx.py 8 -o t4.csv &
# python3 gen_test_nnx.py 8 -o t5.csv &
# wait
# python3 gen_test_nnx.py 8 -o t6.csv &
# python3 gen_test_nnx.py 8 -o t7.csv &
# python3 gen_test_nnx.py 8 -o t8.csv &
# python3 gen_test_nnx.py 8 -o t9.csv &
# python3 gen_test_nnx.py 8 -o t10.csv &
# wait
# python3 merge_csv.py t1.csv t2.csv t3.csv t4.csv t5.csv t6.csv t7.csv t8.csv t9.csv t10.csv test_data_8_flow.csv
# rm -rf t[1,2,3,4,5,6,7,8,9,10].csv


# echo "test - 9 flows"
# python3 gen_test_nnx.py 9 -o t1.csv &
# python3 gen_test_nnx.py 9 -o t2.csv &
# python3 gen_test_nnx.py 9 -o t3.csv &
# python3 gen_test_nnx.py 9 -o t4.csv &
# python3 gen_test_nnx.py 9 -o t5.csv &
# wait
# python3 gen_test_nnx.py 9 -o t6.csv &
# python3 gen_test_nnx.py 9 -o t7.csv &
# python3 gen_test_nnx.py 9 -o t8.csv &
# python3 gen_test_nnx.py 9 -o t9.csv &
# python3 gen_test_nnx.py 9 -o t10.csv &
# wait
# python3 merge_csv.py t1.csv t2.csv t3.csv t4.csv t5.csv t6.csv t7.csv t8.csv t9.csv t10.csv test_data_9_flow.csv
# rm -rf t[1,2,3,4,5,6,7,8,9,10].csv


# echo "test - 10 flows"
# python3 gen_test_nnx.py 10 -o t1.csv &
# python3 gen_test_nnx.py 10 -o t2.csv &
# python3 gen_test_nnx.py 10 -o t3.csv &
# python3 gen_test_nnx.py 10 -o t4.csv &
# python3 gen_test_nnx.py 10 -o t5.csv &
# wait
# python3 gen_test_nnx.py 10 -o t6.csv &
# python3 gen_test_nnx.py 10 -o t7.csv &
# python3 gen_test_nnx.py 10 -o t8.csv &
# python3 gen_test_nnx.py 10 -o t9.csv &
# python3 gen_test_nnx.py 10 -o t10.csv &
# wait
# python3 merge_csv.py t1.csv t2.csv t3.csv t4.csv t5.csv t6.csv t7.csv t8.csv t9.csv t10.csv test_data_10_flow.csv
# rm -rf t[1,2,3,4,5,6,7,8,9,10].csv


echo "test - 15 flows"
python3 gen_test_nnx.py 15 -o t1.csv &
python3 gen_test_nnx.py 15 -o t2.csv &
python3 gen_test_nnx.py 15 -o t3.csv &
python3 gen_test_nnx.py 15 -o t4.csv &
python3 gen_test_nnx.py 15 -o t5.csv &
wait
python3 gen_test_nnx.py 15 -o t6.csv &
python3 gen_test_nnx.py 15 -o t7.csv &
python3 gen_test_nnx.py 15 -o t8.csv &
python3 gen_test_nnx.py 15 -o t9.csv &
python3 gen_test_nnx.py 15 -o t10.csv &
wait
python3 merge_csv.py t1.csv t2.csv t3.csv t4.csv t5.csv t6.csv t7.csv t8.csv t9.csv t10.csv test_data_15_flow.csv
rm -rf t[1,2,3,4,5,6,7,8,9,10].csv


echo "test - 20 flows"
python3 gen_test_nnx.py 20 -o t1.csv &
python3 gen_test_nnx.py 20 -o t2.csv &
python3 gen_test_nnx.py 20 -o t3.csv &
python3 gen_test_nnx.py 20 -o t4.csv &
python3 gen_test_nnx.py 20 -o t5.csv &
wait
python3 gen_test_nnx.py 20 -o t6.csv &
python3 gen_test_nnx.py 20 -o t7.csv &
python3 gen_test_nnx.py 20 -o t8.csv &
python3 gen_test_nnx.py 20 -o t9.csv &
python3 gen_test_nnx.py 20 -o t10.csv &
wait
python3 merge_csv.py t1.csv t2.csv t3.csv t4.csv t5.csv t6.csv t7.csv t8.csv t9.csv t10.csv test_data_20_flow.csv
rm -rf t[1,2,3,4,5,6,7,8,9,10].csv


echo "test - 25 flows"
python3 gen_test_nnx.py 25 -o t1.csv &
python3 gen_test_nnx.py 25 -o t2.csv &
python3 gen_test_nnx.py 25 -o t3.csv &
python3 gen_test_nnx.py 25 -o t4.csv &
python3 gen_test_nnx.py 25 -o t5.csv &
wait
python3 gen_test_nnx.py 25 -o t6.csv &
python3 gen_test_nnx.py 25 -o t7.csv &
python3 gen_test_nnx.py 25 -o t8.csv &
python3 gen_test_nnx.py 25 -o t9.csv &
python3 gen_test_nnx.py 25 -o t10.csv &
wait
python3 merge_csv.py t1.csv t2.csv t3.csv t4.csv t5.csv t6.csv t7.csv t8.csv t9.csv t10.csv test_data_25_flow.csv
rm -rf t[1,2,3,4,5,6,7,8,9,10].csv


echo "test - 50 flows"
python3 gen_test_nnx.py 50 -o t1.csv &
python3 gen_test_nnx.py 50 -o t2.csv &
python3 gen_test_nnx.py 50 -o t3.csv &
python3 gen_test_nnx.py 50 -o t4.csv &
python3 gen_test_nnx.py 50 -o t5.csv &
wait
python3 gen_test_nnx.py 50 -o t6.csv &
python3 gen_test_nnx.py 50 -o t7.csv &
python3 gen_test_nnx.py 50 -o t8.csv &
python3 gen_test_nnx.py 50 -o t9.csv &
python3 gen_test_nnx.py 50 -o t10.csv &
wait
python3 merge_csv.py t1.csv t2.csv t3.csv t4.csv t5.csv t6.csv t7.csv t8.csv t9.csv t10.csv test_data_50_flow.csv
rm -rf t[1,2,3,4,5,6,7,8,9,10].csv


echo "test - 75 flows"
python3 gen_test_nnx.py 75 -o t1.csv &
python3 gen_test_nnx.py 75 -o t2.csv &
python3 gen_test_nnx.py 75 -o t3.csv &
python3 gen_test_nnx.py 75 -o t4.csv &
python3 gen_test_nnx.py 75 -o t5.csv &
wait
python3 gen_test_nnx.py 75 -o t6.csv &
python3 gen_test_nnx.py 75 -o t7.csv &
python3 gen_test_nnx.py 75 -o t8.csv &
python3 gen_test_nnx.py 75 -o t9.csv &
python3 gen_test_nnx.py 75 -o t10.csv &
wait
python3 merge_csv.py t1.csv t2.csv t3.csv t4.csv t5.csv t6.csv t7.csv t8.csv t9.csv t10.csv test_data_75_flow.csv
rm -rf t[1,2,3,4,5,6,7,8,9,10].csv


echo "test - 100 flows"
python3 gen_test_nnx.py 100 -o t1.csv &
python3 gen_test_nnx.py 100 -o t2.csv &
python3 gen_test_nnx.py 100 -o t3.csv &
python3 gen_test_nnx.py 100 -o t4.csv &
python3 gen_test_nnx.py 100 -o t5.csv &
wait
python3 gen_test_nnx.py 100 -o t6.csv &
python3 gen_test_nnx.py 100 -o t7.csv &
python3 gen_test_nnx.py 100 -o t8.csv &
python3 gen_test_nnx.py 100 -o t9.csv &
python3 gen_test_nnx.py 100 -o t10.csv &
wait
python3 merge_csv.py t1.csv t2.csv t3.csv t4.csv t5.csv t6.csv t7.csv t8.csv t9.csv t10.csv test_data_100_flow.csv
rm -rf t[1,2,3,4,5,6,7,8,9,10].csv
