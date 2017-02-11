from __future__ import division

import pandas as pd
import numpy as np
from scipy import spatial, ndimage
from collections import Counter
from os import path, listdir
import multiprocessing as mp
import sys


class Features:
    def __init__(self, df, features):
        
        # Trip data frame and features (as string) that should be
        # extracted for this trip 
        self.df = df 
        self.features = features 

        # Driver and trip number of this data frame
        self.driver = df.index.get_level_values('Driver')[0]
        self.trip = df.index.get_level_values('Trip')[0]

        # Below are the fields that are calculated one in order to speed up
        # processing time

        # Successive differences between x and y values
        self.xDiff = np.diff(self.df.x)
        self.yDiff = np.diff(self.df.y)

        # Important points of a trip (start and finish)
        self.x_start = df['x'][0]
        self.y_start = df['y'][0]
        self.x_finish = df['x'][-1]
        self.y_finish = df['y'][-1]

        # Differences between successive points in time of the trip
        self.euclidean_distances = self.euclidean_helper()

        # Total time in seconds of this trip
        self.total_time = self.trip_time()

        # Mean speed in mph for this trip
        self.mean_speed = self.mean_speed_helper()

        # Accelerations and declerations
        self.acc_and_dec = np.diff(self.euclidean_distances)
        self.accelerations = self.acc_and_dec[self.acc_and_dec > 0]
        self.decelerations = self.acc_and_dec[self.acc_and_dec < 0]

        # Masks that determine the possible current road style (i.e. city, rural, or freeway) 
        self.city_mask = (self.euclidean_distances > 5) & (self.euclidean_distances < 45)
        self.rural_mask = (self.euclidean_distances > 40) & (self.euclidean_distances < 60)
        self.freeway_mask = (self.euclidean_distances > 55) & (self.euclidean_distances < 120)
        
        # Speed distribution fort the different road styles
        self.city_speeds = self.euclidean_distances[self.city_mask]
        self.rural_speeds = self.euclidean_distances[self.rural_mask]
        self.freeway_speeds = self.euclidean_distances[self.freeway_mask]
        
        # Acceleration and deceleration masks for the road forms
        self.city_acc_and_dec = self.acc_and_dec[self.city_mask[:-1]]
        self.rural_acc_and_dec = self.acc_and_dec[self.rural_mask[:-1]]
        self.freeway_acc_and_dec = self.acc_and_dec[self.freeway_mask[:-1]]
        
        self.rural_acc_mask = (self.rural_acc_and_dec > 0)
        self.rural_dec_mask = (self.rural_acc_and_dec < 0)

        self.city_acc_mask = (self.city_acc_and_dec > 0)
        self.city_dec_mask = (self.city_acc_and_dec < 0)
        
        self.freeway_acc_mask = (self.freeway_acc_and_dec > 0)
        self.freeway_dec_mask = (self.freeway_acc_and_dec < 0)

        # Acceleration and deceleration profiles for the road forms
        self.rural_accs = self.rural_acc_and_dec[self.rural_acc_mask]
        self.rural_decs = self.rural_acc_and_dec[self.rural_dec_mask]

        self.city_accs = self.city_acc_and_dec[self.city_acc_mask]
        self.city_decs = self.city_acc_and_dec[self.city_dec_mask]

        self.freeway_accs = self.freeway_acc_and_dec[self.freeway_acc_mask]
        self.freeway_decs = self.freeway_acc_and_dec[self.freeway_dec_mask]

        # 

        self.angles = np.array(self.angles_helper())
        self.stop_time = self.total_stop_time()
        self.pauses = self.pauses_helper()



        self.corner_mask = self.corner_mask_helper(np.pi/32)
        self.straight_mask = np.logical_not(self.corner_mask)

        self.sta = self.euclidean_distances[self.acceleration_mask()] * self.accelerations

        self.euclidean_distances_2 = self.euclidean_helper_2()        

        self.curve_mask = self.curve_mask_helper(np.pi / 16)        
        self.radial_accel = self.radial_accel(50)

    def curve_mask_helper(self, threshold):
        
        angles = np.abs(np.arccos(((self.euclidean_distances[0:-1]**2) + 
                                   (self.euclidean_distances[1:]**2) - 
                                   (self.euclidean_distances_2[0:] ** 2)) / 
                                  (2*self.euclidean_distances[0:-1]*self.euclidean_distances[1:])))
                        
        return np.array(np.logical_and(angles <= (15 * threshold), angles >= threshold))
        
    def radial_accel(self, speed_threshold):
        
        side_a = self.euclidean_distances[0:-1][self.curve_mask]
        side_b = self.euclidean_distances[1:][self.curve_mask]
        side_c = self.euclidean_distances_2[0:][self.curve_mask]
        
        s = (side_a + side_b + side_c) / 2
        
        area = np.sqrt(s * (s - side_a) * (s - side_b) * (s - side_c))
        
        radii = (side_a * side_b * side_c)/(4 * area)
        
        smooth_mask = np.logical_and(radii > 0, side_c < (speed_threshold * 2))     
        
        return (((side_c[smooth_mask] * 0.5) ** 2) / radii[smooth_mask])
        

    #### Helpers

    def zero_or_mean(self, values, default = 0):

        if len(values) == 0:
            return default
        else:
            return np.mean(values)

    def zero_or_median(self, values, default = 0):

        if len(values) == 0:
            return default
        else:
            return np.median(values)

    def zero_or_std(self, values, default = 0):

        if len(values) == 0:
            return default
        else:
            return np.std(values)

    def zero_or_max(self, values, default = 0):

        if len(values) == 0:
            return default
        else:
            return np.percentile(values, 97)

    def euclidean_helper(self):
        """
        Calculate euclidean distance
        """
        # Calculate miles per hour (I assume it's somewhere in the US)
        return np.sqrt(self.xDiff ** 2 + self.yDiff ** 2) * 2.2369

    def euclidean_helper_2(self):
        """
        Calculate euclidean distance between point t and point t+2
        """
        diff1 = np.subtract(self.df.x[2:], self.df.x[0:-2])
        diff2 = np.subtract(self.df.y[2:], self.df.y[0:-2])
        return np.sqrt(diff1 ** 2 + diff2 ** 2)

    def angles_helper(self):
        return np.degrees(np.arctan2(np.diff(self.df.y), np.diff(self.df.x)))

    def mean_speed_helper(self):
        return np.mean(self.euclidean_distances)

    def acceleration_mask(self):
        return (self.acc_and_dec > 0)

    def pauses_helper(self):
        """ create bool array that is true if car moves"""
        return np.array(self.euclidean_distances > 0.001)

    def normalize_angles(self, x):
        if x > 180:
            return np.abs(360 - x)
        else:
            return x

    def angles_helper(self):
        angles = np.abs(np.diff(np.degrees(np.arctan2(np.diff(self.df.y), np.diff(self.df.x)))))
        vfunc = np.vectorize(self.normalize_angles)
        return vfunc(angles)


    ## Features

    def radial_accel_mean(self):
        return self.zero_or_mean(self.radial_accel)
        
    def radial_accel_median(self):
        return self.zero_or_median(self.radial_accel)
                
    def radial_accel_max(self):
        return self.zero_or_max(self.radial_accel)

    def radial_accel_std(self):
        return self.zero_or_std(self.radial_accel)


    def city_radial_accel_mean(self):
        return self.zero_or_mean(self.radial_accel)
        
    def city_radial_accel_median(self):
        return self.zero_or_median(self.radial_accel)
                
    def city_radial_accel_max(self):
        return self.zero_or_max(self.radial_accel)

    def city_radial_accel_std(self):
        return self.zero_or_std(self.radial_accel)


    def rural_accel_mean(self):
        return self.zero_or_mean(self.radial_accel)
        
    def rural_accel_median(self):
        return self.zero_or_median(self.radial_accel)
                
    def rural_accel_max(self):
        return self.zero_or_max(self.radial_accel)

    def rural_accel_std(self):
        return self.zero_or_std(self.radial_accel)


    def freeway_accel_mean(self):
        return self.zero_or_mean(self.radial_accel)
        
    def freeway_accel_median(self):
        return self.zero_or_median(self.radial_accel)
                
    def freeway_accel_max(self):
        return self.zero_or_max(self.radial_accel)

    def freeway_accel_std(self):
        return self.zero_or_std(self.radial_accel)


                
    def break_distance(self):
        ls, num = ndimage.measurements.label(self.euclidean_distances)
        return np.sum(self.euclidean_distances) / num

    def mean_speed_2(self):
        return self.mean_speed ** 2

    def mean_speed_3(self):
        return self.mean_speed ** 3
        
    def onicescu_energy_speed(self):
        dists = np.round(np.array(self.euclidean_distances)).astype(int)
        probs = np.bincount(dists) / self.total_time
        onicescu = (probs ** 2).sum()
        return np.log(onicescu)

    def onicescu_energy_acc(self):
        dists = np.round(np.array(self.accelerations)).astype(int)
        probs = np.bincount(dists) / len(self.accelerations)
        onicescu = (probs ** 2).sum()
        return onicescu

    def onicescu_energy_dec(self):
        dists = np.absolute(np.round(np.array(self.decelerations))).astype(int)
        probs = np.bincount(dists) / len(self.decelerations)
        onicescu = (probs ** 2).sum()
        return onicescu

    def trip_time(self):
        """
        Calculate total trip time in seconds
        """
        return len(self.df.index)

    def trip_air_distance(self):
        """"
        Calculate air distance from starting point to end point
        """
        start = [[self.x_start, self.y_start]]
        finish = [[self.x_finish, self.y_finish]]

        dist = spatial.distance.cdist(start, finish, 'euclidean')
        return dist[0][0]

    def trip_air_distance_manhattan(self):
        """"
        Calculate air distance from starting point to end point
        """

        start = [[self.x_start, self.y_start]]
        finish = [[self.x_finish, self.y_finish]]

        dist = spatial.distance.cdist(start, finish, 'minkowski', 1)
        return dist[0][0]

    def trip_distance(self):
        """
        Calculate speed quantiles
        """
        return self.euclidean_distances.sum()

    def median_speed(self):
        """
        Calculate speed quantiles
        """
        return np.median(self.euclidean_distances)

    def median_acceleration(self):
        acc = np.median(self.accelerations)
        return acc

    def median_acceleration_city(self):

        return self.zero_or_mean(self.city_accs)

    def median_acceleration_rural(self):

        return self.zero_or_mean(self.rural_accs)

    def median_acceleration_freeway(self):
        return self.zero_or_mean(self.freeway_accs)

    def median_deceleration_city(self):
        return self.zero_or_mean(self.city_decs)

    def median_deceleration_rural(self):
        return self.zero_or_mean(self.rural_decs)

    def median_deceleration_freeway(self):
        return self.zero_or_mean(self.freeway_decs)

    def median_deceleration(self):
        acc = np.median(self.decelerations)
        return acc

    def max_speed(self):
        return np.percentile(self.euclidean_distances, 90)

    def max_acceleration(self):
        return np.percentile(self.accelerations, 95)

    def max_deceleration(self):
        return np.percentile(self.decelerations, 95)

    def angle_sum(self):
        return self.angles.sum()

    def angle_mean(self):
        return self.angles.mean()

    def angle_acceleration_mean(self):
        return np.mean(self.angles[self.acceleration_mask()]/self.accelerations)

    def angle_speed_mean(self):
        return np.mean(self.angles/self.euclidean_distances)

    def corners(self):
        return len(self.angles[self.angles > 30])
                
    def pauses_length_mean(self):
        return self.zero_or_mean(self.pauses) 

    def pauses_length_mean_rural(self):
        return self.zero_or_mean(self.pauses[self.rural_mask])

    def pauses_length_mean_city(self):
        return self.zero_or_mean(self.pauses[self.city_mask])

    def pauses_length_mean_freeway(self):
        return self.zero_or_mean(self.pauses[self.freeway_mask])

    def sd_acceleration(self):
        return np.std(self.accelerations)

    def sd_deceleration(self):
        return np.std(self.decelerations)

    def sd_deceleration_city(self):
        return self.zero_or_std(self.city_decs)

    def sd_deceleration_rural(self):
        return self.zero_or_std(self.rural_decs)

    def sd_deceleration_freeway(self):
        return self.zero_or_std(self.freeway_decs)

    def sd_acceleration_city(self):

        return self.zero_or_std(self.city_accs)

    def sd_acceleration_rural(self):

        return self.zero_or_std(self.rural_accs)

    def sd_acceleration_freeway(self):
        return self.zero_or_std(self.freeway_accs)

    def sd_speed(self):
        return np.std(self.euclidean_distances)

    def minimum_deceleration(self):
        return np.percentile(self.decelerations, 2)

    def acceleration_time(self):
        return len(self.accelerations) / self.total_time

    def acceleration_time_city(self):

        return len(self.city_accs) / self.total_time

    def acceleration_time_rural(self):
        return len(self.rural_accs) / self.total_time

    def acceleration_time_freeway(self):

        return len(self.freeway_accs) / self.total_time

    def deceleration_time_city(self):

        return len(self.city_decs) / self.total_time

    def deceleration_time_rural(self):

        return len(self.rural_decs) / self.total_time

    def deceleration_time_freeway(self):

        return len(self.freeway_decs) / self.total_time

    def deceleration_time(self):
        return len(self.decelerations) / self.total_time

    def mean_speed_city(self):

        return self.zero_or_mean(self.city_speeds, 20)

    def mean_speed_rural(self):

        return self.zero_or_mean(self.rural_speeds, 40)

    def mean_speed_freeway(self):

        return self.zero_or_mean(self.freeway_speeds, 65)

    def mean_speed_sd_city(self):

        return self.zero_or_std(self.city_speeds)

    def mean_speed_sd_rural(self):
        return self.zero_or_std(self.rural_speeds)

    def mean_speed_sd_freeway(self):
        return self.zero_or_std(self.freeway_speeds)

    def city_time_ratio(self):
        return len(self.city_speeds) / self.total_time

    def rural_time_ratio(self):
        return len(self.rural_speeds) / self.total_time

    def freeway_time_ratio(self):

        time = self.freeway_speeds
        return len(time) / self.total_time

    def speed_times_acc_mean(self):

        return self.sta.mean()

    def speed_times_acc_max(self):

        return self.sta.max()

    def speed_times_acc_min(self):

        return self.sta.min()

    def speed_times_acc_std(self):

        return np.std(self.sta)

    def total_stop_time(self):
        mask = self.euclidean_distances < 5
        return len(self.euclidean_distances[mask])

    def stop_time_ratio(self):
        return self.stop_time / self.total_time

    def zero_acceleration_ratio_city(self):

        zero_acc_mask = (self.city_acc_and_dec > - 1.5) & (self.city_acc_and_dec < 1.5)

        return len(self.city_acc_and_dec[zero_acc_mask]) / self.total_time

    def zero_acceleration_ratio_rural(self):

        zero_acc_mask = (self.rural_acc_and_dec > - 1.5) & (self.rural_acc_and_dec < 1.5)

        return len(self.rural_acc_and_dec[zero_acc_mask]) / self.total_time

    def zero_acceleration_ratio_freeway(self):

        zero_acc_mask = (self.freeway_acc_and_dec > -1.5) & (self.freeway_acc_and_dec < 1.5)

        return len(self.freeway_acc_and_dec[zero_acc_mask]) / self.total_time

    def hausdorff(self):
        D = spatial.distance.pdist(self.df, 'euclidean')
        H1 = np.max(np.min(D, axis = 1))
        H2 = np.max(np.min(D, axis = 0))

        return (H1 + H2) / 2.

    def corner_mask_helper(self, threshold):
        # If the difference in angles on point x,y is greater than the threshold then
        # x,y is a corner point
        mask = np.abs(np.diff(np.arctan2(self.xDiff, self.yDiff))) >= (threshold)

        # Append False for first and last point
        mask = np.concatenate(([False], mask, [False]))

        # Remove single point corners
        return ndimage.binary_opening(mask, [True, True])


    def extract_all_features(self):

        """
        Extract all relevantfeatures for a given trip
        """

        # Data frame for collecting the features
        series_features = pd.Series()
        series_features['Driver'] = self.driver
        series_features['Trip'] = self.trip

        for feature in self.features:

            # Determine which feature are to be extracted
            feature_method = getattr(self, feature)

            # Calculate value of feature
            series_features[feature] = feature_method()

        return series_features


#############################################
############# 2nd Part, Use it ##############
#############################################

# Feature list
features = ['trip_time'
          , 'trip_air_distance'
          , 'trip_distance'
          , 'trip_air_distance_manhattan'
          , 'median_speed'
          , 'max_speed'
          , 'max_acceleration'
          , 'max_deceleration'
          , 'median_acceleration_city'
          , 'median_acceleration_rural'
          , 'median_acceleration_freeway'
          , 'median_deceleration_city'
          , 'median_deceleration_rural'
          , 'median_deceleration_freeway'
          , 'median_acceleration'
          , 'median_deceleration'
          , 'sd_acceleration'
          , 'sd_deceleration'
          , 'sd_speed'
          , 'minimum_deceleration'
          , 'acceleration_time'
          , 'deceleration_time'
          , 'deceleration_time_city'
          , 'deceleration_time_rural'
          , 'deceleration_time_freeway'
          , 'acceleration_time_city'
          , 'acceleration_time_rural'
          , 'acceleration_time_freeway'
          , 'mean_speed_city'
          , 'mean_speed_rural'
          , 'mean_speed_sd_city'
          , 'mean_speed_sd_rural'
          , 'mean_speed_sd_freeway'
          , 'total_stop_time'
          , 'city_time_ratio'
          , 'rural_time_ratio'
          , 'freeway_time_ratio'
          , 'stop_time_ratio'
          , 'zero_acceleration_ratio_city'
          , 'zero_acceleration_ratio_rural'
          , 'zero_acceleration_ratio_freeway'
          , 'mean_speed_2'
          , 'mean_speed_3'
          , 'onicescu_energy_speed'
          , 'onicescu_energy_acc'
          , 'onicescu_energy_dec'
          , 'break_distance'
          , 'speed_times_acc_mean'
          , 'speed_times_acc_max'
          , 'speed_times_acc_std'
          , 'angle_sum'
          , 'angle_mean'
          , 'angle_acceleration_mean'
          , 'corners'
          , 'pauses_length_mean'
          , 'pauses_length_mean_rural'
          , 'pauses_length_mean_city'
          , 'pauses_length_mean_freeway'
          , 'break_distance'
          , 'radial_accel_mean'
          , 'radial_accel_median'
          , 'radial_accel_max'
          , 'radial_accel_std'            
          , 'sd_acceleration_city'
          , 'sd_acceleration_rural'
          , 'sd_acceleration_freeway'
          , 'sd_deceleration_city'
          , 'sd_deceleration_rural'
          , 'sd_deceleration_freeway']



def do_job(i, chunk, chunk_path):

    """
    Extract all features for one chunk and save to file
    """

    file_name = "features_{}.h5".format(i)
    df = pd.read_hdf(path.join(chunk_path, chunk), key='table')

    features_for_this_chunk = []

    for driver, trip in df.groupby(level=['Driver', 'Trip']):

        # Extract all features for each trip
        series_features = feat.Features(trip, features).extract_all_features()
        features_for_this_chunk.append(series_features)

    # Create a data frame with the features
    df_features_for_this_chunk = pd.DataFrame()
    df_features_for_this_chunk = df_features_for_this_chunk.from_dict(features_for_this_chunk)

    # Write data frames containing the features to HDF5 file
    df_features_for_this_chunk.to_hdf(file_name,
                                      'table')
    print("Written to", file_name)


def main():

  # Chunks (containing parts of the mega df)
    chunk_path = sys.argv[1]
    chunks = sorted(listdir(chunk_path))

    jobs = []

    # Parallely process chunks by using multiprocessing
    for i, chunk in enumerate(chunks):
        print(chunk)
        p = mp.Process(target = do_job, args = (i,chunk,chunk_path, ))
        jobs.append(p)
        p.start()

if __name__ == "__main__":
    main()
