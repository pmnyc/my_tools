# -*- coding:UTF-8 -*-
#####################################################################
###this program is used to dump GPS data into postgresql database#####
#####################################################################
__author__ = 'Guixng Wei'

import re
import copy
import psycopg2
import glob
import datetime


class gps_dump():

    def __init__(self):
        #self.dir = r'E:/Data/Geolife/geolife/Data/*'
        self.dir = r'D:/1_trajectory_data/geolife/Data/*'

        self.host = 'localhost'
        self.database ='geolife'
        self.user = 'postgres'
        self.passwd = 'pgsql2015'
        self.points_pattern = re.compile(r'(?<=\n0\n)(.+)',re.DOTALL)
        self.point_pattern = re.compile(r'(?<=\n)(.+?),(.+?),0,(.+?),(.+?),(.+?),(.+?)(?=\n)',re.DOTALL)
        self.dict_p={}
        self.list_ps=[]
        self.match_pattern = re.compile(r'[0-9]{3}')
        self.count = 0
        self.dict_p = {}
        self.list_uid=[]
        #self.lst_row =[]
        self.num_users=0

    def conn(self):
        self.conn = None
        try:
            self.conn = psycopg2.connect(host=self.host,database=self.database,user=self.user,password=self.passwd)
            self.cur = self.conn.cursor()
            print "conn has been successfully built"
        except Exception as err:
            print "---------->error happened at opening geolife database"
            print err.message

    def insert2table(self):
        try:
            # self.cur.executemany('INSERT INTO geolife.gps_points(uid,lati,longti,alti,days_passed,time_p) '
            #                      'SELECT %(uid)s,%(lati)s,%(longti)s,%(alti)s,%(days_passed)s,%(time_p)s WHERE NOT EXISTS '
            #                      '(SELECT * FROM geolife.gps_points as tem WHERE '
            #                      'tem.uid = %(uid)s and tem.time_p =%(time_p)s)',self.list_ps)
            self.cur.executemany('INSERT INTO geolife.gps_points(uid,lati,longti,alti,days_passed,time_p)'
                            'VALUES (%(uid)s,%(lati)s,%(longti)s,%(alti)s,%(days_passed)s,%(time_p)s)',self.list_ps)
            self.conn.commit()
            self.cur.execute('UPDATE geolife.gps_points SET geog_p=ST_SETSRID(ST_MAKEPOINT(longti,lati),4326)')
            self.conn.commit()
        except Exception as err:
            print "--------> error happened during point insertation!"
            print err.message

    def create_table(self):
        try:
            self.cur.execute('CREATE EXTENSION IF NOT EXISTS postgis SCHEMA public')
            self.cur.execute('CREATE SCHEMA IF NOT EXISTS geolife')
            self.conn.commit()
            self.cur.execute('CREATE TABLE IF NOT EXISTS geolife.gps_points'
                             '('
                             '  seri bigserial NOT NULL,'
                             '  uid integer NOT NULL,'
                             '  lati double precision NOT NULL,'
                             '  longti double precision NOT NULL,'
                             '  alti real NOT NULL,'
                             '  days_passed double precision NOT NULL,'
                             '  time_p timestamp without time zone NOT NULL,'
                             '  geog_p geometry(Point),'
                             '  CONSTRAINT pri_uid_time PRIMARY KEY (uid, time_p)'
                             ')'
                             'WITH ('
                             '  OIDS=TRUE'
                             ')')
            self.conn.commit()
            self.cur.execute("select column_name from information_schema.columns where table_schema = 'geolife' and table_name = 'gps_points'")
            rows = self.cur.fetchall()
            if ('day_week',) not in rows:
                self.cur.execute('ALTER TABLE geolife.gps_points ADD day_week INTEGER')
                self.conn.commit()
            if ('hour_day',) not in rows:
                self.cur.execute('ALTER TABLE geolife.gps_points ADD hour_day time without time zone')
                self.conn.commit()
            if ('speed',) not in rows:
                self.cur.execute('ALTER TABLE geolife.gps_points ADD speed REAL')
            if ('time_diff',) not in rows:
                self.cur.execute('ALTER TABLE geolife.gps_points ADD time_diff INTERVAL')
            if ('distance',) not in rows:
                self.cur.execute('ALTER TABLE geolife.gps_points ADD distance REAL')
        except Exception as err:
            print '----->error happened during table and schema creation'
            print err.message

    def read_file(self):
        files_list = glob.glob(self.dir)
        for f in files_list:
            file_uid = re.search(self.match_pattern,f).group(0)
            #dir_plt = r'E:/Data/Geolife/geolife/Data/'+file_uid+r'/Trajectory/*'
            dir_plt = r'D:/1_trajectory_data/geolife/Data/'+file_uid+r'/Trajectory/*'
            plt_list = glob.glob(dir_plt)
            for f_plt in plt_list:
                if '200811' in f_plt:
                    continue
                else:
                    print ("---->the current processed file is: "+f_plt)
                    with open(f_plt,'r') as f:
                        points_str = f.read()
                        match = re.search(self.points_pattern,points_str)
                        points = match.group(1)
                        matches = re.findall(self.point_pattern,points)
                        for ma in matches:
                            self.dict_p['uid'] = int(file_uid)
                            self.dict_p['lati'] = float(ma[0])
                            self.dict_p['longti'] = float(ma[1])
                            self.dict_p['alti'] = float(ma[2])
                            self.dict_p['days_passed'] = float(ma[3])
                            self.dict_p['time_p'] =ma[4]+' '+ ma[5]
                            if self.list_ps.__len__()==0:
                                self.list_ps.append(copy.deepcopy(self.dict_p))
                            else:
                                n = self.list_ps.__len__()
                                if self.dict_p['uid']==self.list_ps[n-1]['uid'] and self.dict_p['time_p']==self.list_ps[n-1]['time_p']:
                                    continue
                                else:
                                    self.list_ps.append(copy.deepcopy(self.dict_p))

                        self.insert2table()
                        del self.list_ps[:]

    def num_uid(self):
        try:
            self.cur.execute('SELECT DISTINCT uid FROM geolife.gps_points')
            rows = self.cur.fetchall()
            self.num_users =rows.__len__()
            rows_2 =[]
            for i in range(0,self.num_users,1):
                rows_2.append(rows[i][0])
            self.list_uid = rows_2

        except Exception as err:
            print "----->something wrong happened during querying the number of users"
            print err.message


    def day_week(self):
        try:
            while True:
                self.cur.execute('SELECT * FROM geolife.gps_points WHERE day_week is NULL limit 1')
                row = self.cur.fetchone()
                if not row:
                    break
                else:
                    self.count += 1
                    index_uid = row[1]
                    index_time = row[6]
                    index_day = index_time.weekday()
                    self.cur.execute("UPDATE geolife.gps_points SET day_week={0} "
                                     "WHERE uid={1} AND time_p='{2}'".format(index_day,index_uid,str(index_time)))
                    self.conn.commit()
                    print "the current processing user is {0} and his weekday is {1}".format(index_uid,index_day)
                    print "the total processed # is {0}".format(self.count)
        except Exception as err:
            print '----->error happened during week_day insertation'
            print err.message

    def hour_day(self):
        try:
            while True:
                self.cur.execute('SELECT * FROM geolife.gps_points WHERE  hour_day is NULL limit 1')
                row = self.cur.fetchone()
                if not row:
                    break
                else:
                    self.count += 1
                    index_uid = row[1]
                    index_time = row[6]
                    index_hour = index_time.time()
                    self.cur.execute("UPDATE geolife.gps_points SET hour_day='{0}' "
                                     "WHERE uid={1} AND time_p='{2}'".format(index_hour,index_uid,str(index_time)))
                    self.conn.commit()
                    print "the current processing user is {0} and his hour is {1}".format(index_uid,index_hour)
                    print "the total processed # is {0}".format(self.count)
        except Exception as err:
            print '----->error happened during week_day insertation'
            print err.message

    def del_conn(self):
        if self.conn:
            self.conn.close()
            print "-------->the database is closed now"

    def time_interval(self):
        if self.list_uid.__len__() == 0:
            self.num_uid()
        try:
            for j in self.list_uid:
                self.cur.execute('update geolife.gps_points set time_diff=m.b '
                                 'from(select seri, b.time_p-lag(b.time_p) over (partition by b.day_week order by b.time_p ASC) as b '
                                 'from geolife.gps_points as b where uid=j) as m where geolife.gps_points.seri=m.seri'.format(j))
                self.conn.commit()
                print "time difference of the user {0} has been processed successfully".format(j)
            print "all time difference has been processed"
        except Exception as err:
            print '----->error happened during time difference calculation'
            print err.message

    def calc_distance(self):
        if self.list_uid.__length__ == 0:
            self.num_uid()
        try:
            for j in self.list_uid:
                self.cur.execute('Update geolife.gps_points set distance=m.b '
                                 'from (select seri,st_distance_sphere (geog_p,lag(geog_p) over (partition by day_week order by time_p ASC)) as b '
                                 'from geolife.gps_points where uid=j) as m where geolife.gps_points.seri=m.seri'.format(j))
                self.conn.commit()
                print "distance of the user {0} has been processed successfully".format(j)
            print "all distance has been processed"
        except Exception as err:
            print '----->error happened during distance calculation'
            print err.message
    def calc_speed(self):
        try:
            self.cur.execute('update geolife.gps_points as a set speed=(distance/extract(epoch from time_diff))')
            self.conn.commit()
            self.cur.execute("update geolife.gps_points as a set speed=Null where time_diff>’00:00:05’")
            self.conn.commit()
            print"all speed has been processed"
        except Exception as err:
            print '----->error happened during speed calculation'
            print err.message


if __name__ == "__main__":
    gps_obj = gps_dump()
    gps_obj.conn()
    gps_obj.create_table()
    gps_obj.read_file()
    #gps_obj.day_week()
    #gps_obj.hour_day()
    #gps_obj.time_interval()
    #gps_obj.calc_distance()
    #gps_obj.calc_speed()
    gps_obj.del_conn()



