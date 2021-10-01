from gps_trajectories import GPSTrajectoriesTest, GPSTrajectoriesTrain
import glob
import os

data_path = '/Users/mahdi/Desktop/GeolifeTrajectories1.3/Data/'
out_data_path = '/Users/mahdi/Desktop/GeolifeTrajectories1.3/Output/'


def find_and_process_trajectories(number_of_train_files, path, extension, output):
    gps_train_threshold = GPSTrajectoriesTrain()
    count = 0
    threshold = 0
    for root, dirnames, filenames in os.walk(path):
        for filename in glob.glob(os.path.join(os.path.join(root), '*.' + extension)):
            count += 1
            if count > number_of_train_files:
                name = filename.replace(root + "/", "")
                directory = root.replace(data_path, "").replace("/Trajectory", "")
                gps_trajectories = GPSTrajectoriesTest(data_path=filename, name=name, directory=directory, output=output)
                gps_trajectories.read_and_analyze_trajectory()
                #gps_trajectories.entropy_based_threshold_calculation()
                gps_trajectories.set_threshold(threshold)
                gps_trajectories.divide_gps_trajectories_into_gps_traces()
            else:
                gps_train_threshold.read_trajectory(filename)
                if count is number_of_train_files:
                    gps_train_threshold.calculate_frequencies_and_probabilities()
                    threshold = gps_train_threshold.entropy_based_threshold_calculation()
                    print(threshold)


find_and_process_trajectories(100, data_path, 'plt', out_data_path)
