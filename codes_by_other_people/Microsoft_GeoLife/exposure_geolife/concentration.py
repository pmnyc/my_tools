# -*- coding:UTF-8 -*-
__author__ = 'Guixing Wei'

import random


class exposure():

    def __init__(self):
        pass
    def model_traffic(self,lati,longti,alti,time_p):
        pass
    def model_industry(self,lati,longti,alti,time_p):
        pass

    def model_temp(self,lati,longti,time_p):
        self.expo_value = random.uniform(0,20)


if __name__ =="__main__":
    exposure_obj = exposure()
    exposure_obj.model_temp(39.22,116.32,'')
    print exposure_obj.expo_value









