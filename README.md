# udacity-machine-learning-engineer


Scripts: <br>


1. data_preprocessing.py:
  a. For preprocessing MRT traffic data.
  b. Extract data of to Taipei Main Station and Taipei City Hall only

2. traffic_data_ex2.ipynb
  a. Use dataset generated from data_preprocessing
     and create traffic_tms_all.csv, traffic_tch_all.csv for model
  b. Data explore and visualization

3. weather_data_ex2.ipynb:
  a. Use weather dataset
     and create weather_tms_all.csv, weather_tch_all.csv for model
  b. Data explore and visualization

4. Benchmark_DeepAR.ipynb
  a. Generate benchmark using DeepAR

5-1. SVR_model.ipynb
  a. Split train and test dataset
  b. Generate SVR model

5-2. param_tuning.ipynb
  a. Generate SVR model and tuning the parameters

6. performance.ipynb (opt)
   a. Check RMSE

Folders:
1. data: data for models, generated by script 2 and 3
2. json_traffic_data: data generated by 4.Benchmark_DeepAR.ipynb
3. tch_data and tms_data: data enerated by script 5-1
4. source_sklearn: training script for running on SageMaker
5. raw_data: Due to the file size, the folder is empty,
   the raw data can be found on https://data.gov.tw/dataset/128506
