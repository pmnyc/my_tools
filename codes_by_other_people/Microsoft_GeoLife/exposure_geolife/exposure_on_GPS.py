# -*- coding:UTF-8 -*-
#####################################################################################################
### this program allows you to find out the significant place of targeted people#####
#####################################################################################################

__author__ = 'Guixing Wei'
import psycopg2
# import exposure
import numpy as np
from sklearn import metrics
from sklearn.cluster import DBSCAN



class traj_pattern():
    def __init__(self):
        self.host = 'localhost'
        self.database = 'geolife'
        self.user = 'postgres'
        self.passwd = 'pgsql2015'
        # self.expo = exposure()

    def conn(self):
        self.conn = None
        try:
            self.conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.passwd)
            self.cur = self.conn.cursor()
        except Exception as err:
            print "---------->error happened at opening geolife database"
            print err.message

    def del_conn(self):
        if self.conn:
            self.conn.close()
            print "-------->the database is closed now"


    def find_home(self):
        try:
            self.cur.execute("select seri,st_astext(geop_p) from geolife.gps_points where uid=0 and hour_day>'2:00:00'and hour_day<'5:00:00'and day_week<5 and speed=0")
            rows= self.cur.fetchall()
        except Exception as err:
            print '----->error happened during retrieving location of possible home points'
            print err.message



    def exposure_hist_mom(self, uid, time):
        pass

    def exposure_curr_mom(self, uid):
        pass

    def exposure_his_range(self, uid, time, time_end):
        pass


if __name__ == "__main__":
    traj_obj = traj_pattern()
    traj_obj.conn()
    traj_obj.find_home()
    traj_obj.del_conn()
