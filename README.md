# GPS Trajectories into GPS Traces:
used an entropy-based-histogram to divide GPS trajectories into GPS traces.

## Requirements
1. Install Python (3.9 recommended) [Download link](https://www.python.org/downloads/).
2. Install required packages using pip: `pip3.9 install numpy pandas pathlib csv-reader scipy`.

## Usage
1. Download or clone repository.
2. Download the dataset from [GeoLife GPS Trajectories](https://www.microsoft.com/en-us/download/details.aspx?id=52367)
3. Edit the data_path and out_data_path in `main.py`.
4. Set the number_of_train_files in `main.py`.
5. Run the code using `python3.9 main.py`.
6. After training, you can see the threshold and the GPS trajectories will divide into GPS traces
7. Enjoy!

## Explanation
[Screen Recording](https://drive.google.com/file/d/1NDR88tCj_SD2h_zGI2Q3hm1vrmOBv26A/view?usp=sharing)

## Documentation - Steps
1. Use os.walk in `main.py` to find all GPS trajectories in data_path
2. Read Trajectoreis using pandas Dataframe
3. After reading all files:

    3.1. Calculate time differences between all consecutive reading in seconds

    3.2. Find all unique seconds with their frequency

    3.3. Calculate the probabilities using frequency / sum_of_total_frequencies

    3.4. Calculate all states of entroies by dividing the probability array into to parts with t1 to tn and store them

    3.5. Find the location where entopy was maximum in the sample rates

    3.6. Here you have the threshold
  
4. Use the calculated threshold to read GPS trajectories and divide them into GPS traces. each trace will be saved with an index in out_put directory.