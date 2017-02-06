# -*- coding:UTF-8 -*-
#####################################################################################################
### this program allows you to define and identify human's mobility pattern and inhalation rate#####
#####################################################################################################


__author__ = 'wgx'
import psycopg2
import numpy as np
from gps_dump_home import gps_dump
from sklearn import cluster
from sklearn.cluster import DBSCAN
import re


class activity(gps_dump):

    def __init__(self):
        gps_dump.__init__(self)
        gps_dump.conn(self)
        self.nop_weekday = 0
        self.nop_weekend =0
        self.rows_p=[]
        self.rows= None
        self.xy=[]
        self.labels =0



    # def calc_nop(self):#determine the #mini for cluster of NBSC algorithm
    #     if self.nop_weekday == 0:
    #         self.cur.execute(r'select count(*) from geolife.gps_points where uid=0 and day_week<5')
    #         rows = self.cur.fetchall()
    #         self.nop_weekday = rows
    #     if self.nop_weekend ==0:
    #         self.cur.execute(r'select count(*) from geolife.gps_points where uid=0 and day_week>4')
    #         rows = self.cur.fetchall()
    #         self.nop_weekend = rows

    def find_home(self):
        try:
            self.cur.execute(r"SELECT seri,st_astext(geop_p) FROM geolife.gps_points WHERE uid= 0 "
                             r"and hour_day>'03:00:00' and hour_day<'05:00:00' "
                             r"and day_week<5"
                             r"and speed=0")
            self.rows = self.cur.fetchall()
            len_rows = len()
            for i in self.rows:
                self.rows_p.append(i[1])
            xy_pattern = re.compile(r'[0-9]+\.[0-9]+')
            for i in self.rows_p:
                matches = re.findall(xy_pattern,i)
                x = float(matches[0])
                y = float(matches[1])
                xy_temp=[x,y]
                self.xy.append(xy_temp)
            xy_np = np.array(self.xy)
            db = DBSCAN(eps=15,min_samples=100).fit(xy_np)
            self.labels = db.labels_
            print self.labels
            self.n_clusters = len(set(self.labels))-(1 if -1 in self.labels else 0)
            print self.n_clusters
            print db.core_sample_indices_






        except Exception as err:
            print "------>something wrong happened during inferring home cluster"
            print err.message


if __name__ =="__main__":
    act_obj = activity()
    #act_obj.calc_nop()
    act_obj.find_home()