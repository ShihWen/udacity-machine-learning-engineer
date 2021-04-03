import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import sys
import os
import re
import traceback

class trafficExtractor():
    '''
    1. Extract and clean traffic data from csv file downloaded from
       https://data.gov.tw/dataset/128506
    2. Select traffic data from specific stations
    3. Add station id for reference
    4. Tranform into dataframe
    5. Output as csv format

    '''
    def __init__(self, raw_data_path, extracted_stations, output_folder):
        self.data_path = raw_data_path
        self.extract_stations = extracted_stations
        self.cleaned_data = []
        self.extracted = []
        self.dataframe = None
        self.output_folder = output_folder
        self.output_data_month = ''

        self.run()

    #extract raw data
    def csv_extracter(self, file_name):
        extract_list = []
        count = 1
        with open('{}'.format(file_name), encoding="utf8") as csvfile:
            # read CSV
            rows = csv.reader(csvfile)
            # extract rows
            for row in rows:
                if count%10000 == 0:
                    sys.stdout.write('\rextracting row {}'.format(count))
                extract_list.append(row)
                count += 1
        sys.stdout.write('\nextracting finished\n')
        return extract_list

    #remove spacing
    def csv_cleaner(self, extract_list):
        # step 1. remove spacing
        cleaned = []
        count = 1
        for item in extract_list:
            if count%10000 == 0:
                sys.stdout.write('\rcleaning row {}'.format(count))
            new_row = []
            for row in item:
                new_row = ','.join(row.split())
                new_row = new_row.split(',')

            cleaned.append(new_row)
            count += 1
        sys.stdout.write('\ncleaning finished\n')

        # step 2. remove redundant rows
        remove_idx = []
        for i in range( len(cleaned) ):
            try:
                if len(cleaned[i][1]) > 2 or cleaned[i][1]=='時段':
                    #print('removed', i, cleaned[i])
                    remove_idx.append(i)
            except IndexError:
                #print('removed: index Error: ', cleaned[i])
                remove_idx.append(i)

        for i in range(len(cleaned)):
            if i not in remove_idx:
                self.cleaned_data.append(cleaned[i])
        cleaned = None

    def get_selected_station(self):
        sys.stdout.write('\rextracting...')
        for row in self.cleaned_data:
            if row[2] in self.extract_stations or row[3] in self.extract_stations:
                self.extracted.append(row)

    ##Station ID
    #Reference for station code and name
    def station_id(self):
        file_ID = 'station_id2.csv'
        with open(file_ID, 'r', encoding="utf-8") as fid:
            stationlist = csv.reader(fid)
            id_dict = {rows[1]:rows[0] for rows in stationlist}
        return id_dict

    def station_eng_name(self):
        file_ID = 'station_name.csv'
        with open(file_ID, 'r', encoding="utf-8") as fid:
            stationlist = csv.reader(fid)
            id_dict = {rows[0]:rows[3] for rows in stationlist}
        return id_dict

    def raw_to_df(self, cleaned_list, id_dict):
        #cleaning raw data
        sys.stdout.write('\rprocessing raw data...')
        df = pd.DataFrame(cleaned_list)
        #drop null column: cloumn 5
        df = df[[0,1,2,3,4]]

        #fix headers, drop "----"
        #df = df.drop([0,1])
        df.columns = ['date', 'time', 'entrance', 'exit', 'people']

        #drop null rows
        #df = df[df['people'] != 'Null']

        #converting to proper dtypes in order to save memories.
        print('converting raw dtypes...')
        df = df[df['time'].str.contains('[0-9]', na=False, regex=True) == True]
        df["time"] = df["time"].astype('int8')
        df["people"] = pd.to_numeric(df["people"], downcast='integer')
        df["entrance"] = df["entrance"].astype('category')
        df["exit"] = df["exit"].astype('category')

        #get code_id of stations from "station_id2.csv"
        print('adding station IDs...')
        df['code_entrance'] = df['entrance'].map(id_dict)
        df['code_exit'] = df['exit'].map(id_dict)

        df["code_entrance"] = df["code_entrance"].astype('category')
        df["code_exit"] = df["code_exit"].astype('category')

        #processing datetime, weeknum and weekday
        print('processing datetime, weeknum and weekday...')
        df['date'] = pd.to_datetime(df['date'],errors='coerce')
        df['weekday'] = df['date'].dt.weekday
        df["weekday"] = pd.to_numeric(df["weekday"], downcast='integer')

        df = df[df['date'].dt.year==2020]
        print('raw DataFrame DONE\n')
        self.dataframe=df

    def output_df(self):
        sys.stdout.write('\rexporting csv file...')
        pattern = re.compile('[0-9][0-9][0-9][0-9][0-9][0-9]')
        self.output_data_month = re.search(pattern, self.data_path).group(0)

        self.dataframe.to_csv('{}/processed_csv_{}.csv'.format(self.output_folder,self.output_data_month),index=False)


    def run(self):
        extracted = self.csv_extracter(self.data_path)
        self.csv_cleaner(extracted)
        extracted = None

        self.get_selected_station()
        station_id = self.station_id()
        self.raw_to_df(cleaned_list=self.extracted,
                             id_dict=station_id)
        self.output_df()
        sys.stdout.write('\nDone')


if __name__ == '__main__':
    data_month_list = ['202001','202002','202003',
                       '202004','202005','202006',
                       '202007','202008','202009']
    output_folder = 'processed_csv'
    extract_station_list = ['台北車站','市政府','板橋']

    for month in data_month_list:
        try:
            file_path = 'raw_data/臺北捷運每日分時各站OD流量統計資料_{}.csv'.format(month)
            sys.stdout.write('\nProcessing file month: {}\n\n'.format(month))
            obj = trafficExtractor(raw_data_path=file_path,
                                          extracted_stations=extract_station_list,
                                          output_folder=output_folder)
        except:
            traceback.print_exc()
