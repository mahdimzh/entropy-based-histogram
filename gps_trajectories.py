import pandas as pd
import numpy as np
from csv import reader
from scipy.stats import entropy
from dateutil import parser
from numpy import log as ln
import os


def find_first_line(data_path):
    with open(data_path, 'r') as read_obj:
        csv_reader = reader(read_obj)
        skip_line = 0
        for row in csv_reader:
            skip_line += 1
            if len(row) == 1 and row[0] == '0':
                return skip_line
    return skip_line


def entropy(pks):
    summation = 0
    for pk in pks:
        summation += (pk * ln(pk))
    return (-1) * summation


def pd_to_file(data_frame, path, name):
    if not os.path.exists(path):
        os.makedirs(path)
    data_frame.to_csv(path + "/" + name, index=False)


class GpsTrajectories:
    def __init__(self):
        self.data_path = None
        self.name = None
        self.directory = None
        self.output = None
        self.data = pd.DataFrame({
            'LATITUDE': [],
            'LONGITUDE': [],
            'UNKNOWN': [],
            'ALTITUDE': [],
            'DATE': [],
            'DATE_STRING': [],
            'TIME_STRING': [],
        })
        self.consecutive_interval_differences, self.sample_rates, self.sample_rate_frequencies, self.pi = ([
        ],) * 4
        self.n = 0
        self.threshold = 0

    def set_threshold(self, t):
        self.threshold = t

    def set_data_path(self, d):
        self.data_path = d

    def set_name(self, n):
        self.name = n

    def set_directory(self, d):
        self.directory = d

    def set_output(self, o):
        self.output = o

    def read_trajectory(self, data_path=None):
        path = data_path if data_path is not None else self.data_path
        skip_line = find_first_line(path)
        df = pd.read_csv(path,
                         names=['LATITUDE', 'LONGITUDE', 'UNKNOWN',
                                'ALTITUDE', 'DATE', 'DATE_STRING', 'TIME_STRING'],
                         sep=',', skiprows=skip_line)
        self.data = self.data.append(df)

        return self.data

    def calculate_consecutive_time_interval_differences(self):
        prev_date = None
        consecutive_interval_differences = []
        for index, row in self.data.iterrows():
            date = parser.parse(row['DATE_STRING'] + ' ' + row['TIME_STRING'])
            if prev_date is not None:
                diff = date - prev_date
                seconds = int(round(diff.seconds))
                consecutive_interval_differences.append(seconds)
            prev_date = date

        return consecutive_interval_differences

    def calculate_frequencies_and_probabilities(self):
        self.consecutive_interval_differences = self.calculate_consecutive_time_interval_differences()
        self.sample_rates, self.sample_rate_frequencies = np.unique(
            np.array(self.consecutive_interval_differences), return_counts=True)
        self.n = sum(self.sample_rate_frequencies)
        self.pi = self.sample_rate_frequencies / self.n

    def entropy_based_threshold_calculation(self):
        # dict(zip(self.unique, self.counts))
        e = []
        start = 1 if len(self.pi) > 1 else 0
        for t in range(start, len(self.pi)):
            # e1 = entropy(self.pi[:t] / sum(self.pi[:t]));
            # e2 = entropy(self.pi[t:] / sum(self.pi[t:]));
            e1 = entropy(self.pi[:t] / sum(self.pi[:t]))
            e2 = entropy(self.pi[t:] / sum(self.pi[t:]))
            e.append(e1 + e2)

        self.threshold = self.sample_rates[np.argmax(e)]
        return self.threshold


class GPSTrajectoriesTest(GpsTrajectories):
    def __init__(self, data_path, name, directory, output):
        super().__init__()
        super().set_data_path(data_path)
        super().set_name(name)
        super().set_directory(directory)
        super().set_output(output)
        print("GPS trajectories to traces for " + data_path)

    def divide_gps_trajectories_into_gps_traces(self):
        start_index = 0
        file_index = 1
        path = self.output + self.directory

        for index, interval in enumerate(self.consecutive_interval_differences):
            if interval > self.threshold:
                pd_to_file(self.data[start_index:index + 1],
                           path, self.name + "." + str(file_index))
                start_index = index + 1
                file_index += 1

        if start_index is not (len(self.consecutive_interval_differences) + 1):
            pd_to_file(self.data[start_index:], path,
                       self.name + "." + str(file_index))


class GPSTrajectoriesTrain(GpsTrajectories):
    def __init__(self):
        super().__init__()
        print("Start Training ...")
