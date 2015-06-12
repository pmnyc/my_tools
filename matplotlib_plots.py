#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
@author: pm

This program is for plotting the Usage Histogram and CDF curve
"""

import numpy as np
import pandas as pd
import copy as copy
import matplotlib.pyplot as plt
import pylab as P
from matplotlib.backends.backend_pdf import PdfPages
from sqlalchemy import create_engine
from pandasql import sqldf

def lineBarPlot(bill_data_by_period,
                region, 
                customerType,
                year, 
                energyType, 
                periodType, 
                NumofBins, 
                BaseLine_to_Average, 
                pdfFilename,
                pdfsize,
                logscale_ind = False,
                BaseLine_Label = 'Upper Bound \nOf Tier 0',
                plot_baseline_ind = False,
                UpperPercentile_UsageCap = 99.5):
    ######## Sample  Parameters #########
    # bill_data_by_period = 5500.0 + 2500.0 * np.random.randn(10000) #Just randomly generated 10k monthly
    #                     # usage data within winter or summer period

    # region = 'MyRegion'
    # customerType = 'House'
    # year = 2013
    # energyType = 'Electric' # it nees to be one of either Electric or Gas
    # periodType = 'Winter' # it needs to be one of Winter or Summer

    # NumofBins = 16
    # BaseLine_to_Average = 0.5 #This defines the % of average used as baseline/Tier0
    # BaseLine_Label = 'Upper Bound \nOf Tier 0' #Defines the label name for the vertical base line
    # plot_baseline_ind = False #This specifies whether we put a vertical baseline or not
    # pdfFilename = 'plot01' #Output PDF file's name
    # pdfsize = (11,8.5) #PDF output file size, letter size is 8.5X11
    # logscale_ind = False #This defines whether we take log of target value when forming bins or not
    # UpperPercentile_UsageCap = 99 #It defines the percentile to cap the upper limit of usage to prevent
                                    # extreme usage case
    #####################################

    if energyType == 'Electric':
        energyUnit = 'kWh'
    else:
        energyUnit = 'Therm'

    title = region + ' ' + customerType + ' ' + energyType + ', ' \
                + periodType + ' Period \n Year ' + str(year)
    left_column_title = 'Number of Customers'
    right_column_title = 'Cumulative Percent by Bin'
    right_column_title2 = 'Cumulative \nPercent by Bin'
    bottom_title = 'Monthly Energy(' + energyUnit + ')'

    Total_Customer_Count = len(bill_data_by_period)
    Avg_of_Kwh = np.mean(bill_data_by_period)
    BaseLine = Avg_of_Kwh * BaseLine_to_Average

    title += '   (Average Monthly Usage is ' + str(int(Avg_of_Kwh)) + ' ' + energyUnit +')'

    bill_data_by_period_mock = map(lambda t: (t > 5) * t + 2.5 * (t <= 5),bill_data_by_period)
    if logscale_ind:
        bill_data_by_period_mock = map(lambda t: np.log(t),bill_data_by_period_mock)
    # The following is to cap the usage by 98 percentile to prevent extreme case
    pertile_cap = np.percentile(bill_data_by_period_mock,UpperPercentile_UsageCap)
    bill_data_by_period_mock = map(lambda t: (t > pertile_cap) * (pertile_cap + 0.1) + t * (t <= pertile_cap),bill_data_by_period_mock)

    hist, bin_edges = np.histogram(bill_data_by_period_mock, bins=NumofBins)
    cdf_perc = (np.cumsum(hist, axis=0) + 0.0) / (np.cumsum(hist, axis=0)[-1] + 0.0)

    bincenters = 0.5*(bin_edges[1:]+bin_edges[:-1])

    ## Plots ##
    fig = plt.figure()
    fig.set_size_inches(pdfsize[0],pdfsize[1])
    ax = fig.add_subplot(111)
    barplot = ax.hist(bill_data_by_period_mock, bins=NumofBins, color='lightgreen', rwidth=0.6, alpha=0.75)
    P.ylim(0, np.max(hist)*1.1)

    # add count info to the top of bar
    textcenters = 0.2*bin_edges[1:]+0.8*bin_edges[:-1]
    for i in range(len(hist)):
        txt = hist[i]
        xloc = textcenters[i]
        yloc = hist[i] + hist.std()*0.05
        ax.text(xloc, yloc, hist[i], fontsize=10)

    ax.grid(True)

    ax.set_title(title, fontsize=12)
    ax.set_ylabel(left_column_title, fontsize=12)
    ax.set_xlabel(bottom_title)

    # add xtick marks
    #xTickMarks = ['Group'+str(i) for i in range(1,17)]
    if logscale_ind:
        xTickMarks = [(str(int(np.sign(i) * np.exp(bin_edges[i]))) + '~' + str(int(np.exp(bin_edges[i+1]))) + '' + energyUnit) for i in range(NumofBins)]
        xTickMarks[-1] = str(int(np.exp(bin_edges[NumofBins-1]))) + '+ ' + energyUnit
    else:
        xTickMarks = [(str(int(np.sign(i) * bin_edges[i])) + '~' + str(int(bin_edges[i+1])) + '' + energyUnit) for i in range(NumofBins)]
        xTickMarks[-1] = str(int(bin_edges[NumofBins-1])) + '+ ' + energyUnit

    tickercenter = textcenters[:1]
    tickercenter_ = tickercenter.tolist()
    tickercenter2_ = bin_edges[1:-1]
    tickercenter2_ = tickercenter2_.tolist()
    tickercenter_.extend(tickercenter2_)
    ax.set_xticks(np.array(tickercenter_))
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=30, fontsize=8)

    # Add CDF curve to ax2
    ax2 = ax.twinx()
    cdfplot = ax2.plot(bincenters, cdf_perc, lw=2, color='darkgray', label=right_column_title2)
    plt.yticks(map(lambda x: 0.01 * x, range(0, 101, 10)), [str(x) + "%" for x in range(0, 101, 10)], fontsize=10)
    ax2.set_ylabel(right_column_title, fontsize=12)

    # Add a vertical line as baseline
    if plot_baseline_ind:
        vline = ax.axvline(x=BaseLine,ymin=0,ymax=np.max(hist),linewidth=1.2, color='red')
        vline.set_label(BaseLine_Label)
        ax.legend(loc=2,bbox_to_anchor=(0,0.92))
    ax2.legend(loc=0)

    ## Save Plot to PDF ##
    with PdfPages(pdfFilename+'.pdf') as pdf:
        pdf.savefig()
        plt.close()

# Extract Data from PostgreSQL and export to pandas data frame
def getDF(postgrestable = "data.mydata",
        engine = 'postgresql://user:pwd@hostserver:5432/mydatabase'):
    engine = create_engine(engine)
    return pd.read_sql_query('SELECT * FROM ' + postgrestable + ' where a > 1',con=engine)


if __name__ == '__main__':
    alldata = getDF(postgrestable = "data.mydata")
    alldata.to_csv("mydata.csv",index=False)
    #alldata = pd.read_csv("mydata.csv")
    alldata.rename(columns={'rept_year':'year','season':'periodType'
                    ,'flg_res':'customerType'}, inplace=True)
    alldata.loc[alldata['periodType'] == 'W',['periodType']] = 'Winter'
    alldata.loc[alldata['periodType'] == 'S',['periodType']] = 'Summer'

    customerType_ = alldata.customerType.unique()
    customerType_ = customerType_.tolist()
    year_ = alldata.year.unique()
    periodType_ = alldata.periodType.unique()
    periodType_ = periodType_.tolist()
    year_ = sorted(year_, reverse=True)

    # Replace year '9999' by '2011~2015'
    # for n,item in enumerate(year_):
    #     if item=='9999':
    #         year_[n]='2011~2015'
    # try:
    #     del n, item
    # except:
    #     pass

    counter=100
    for customerType in customerType_:
        for year in year_:
            for periodType in periodType_:
                sqlcmd = "select * from alldata "
                sqlcmd += "where customerType = '" + customerType + "' and "
                sqlcmd += "year = " + str(int(year)) + " and "
                sqlcmd += "periodType = '" + periodType + "';"
                bill_df = sqldf(sqlcmd, locals())
                year2 = str(int(year))
                if year2 == '9999':
                    year2 = '2011~2015'
                counter += 1

                UpperPercentile_UsageCap = 99.5 #Default Usage Cap Percentile
                logscale_ind = False
                NumofBins = 16
                if customerType == 'Building':
                    UpperPercentile_UsageCap = 99
                    logscale_ind = True
                    NumofBins = 16

                # Create Plots
                lineBarPlot(bill_data_by_period = np.array(bill_df['use_per_month']),
                                region = 'MyRegion', 
                                customerType = customerType,
                                year = year2, 
                                energyType = 'Electric', 
                                periodType = periodType, 
                                NumofBins = NumofBins, 
                                BaseLine_to_Average = 0.5, 
                                pdfFilename = 'plots_' + str(counter),
                                logscale_ind = logscale_ind,
                                pdfsize = (11,8.5),
                                BaseLine_Label = 'Upper Bound \nOf Tier 0',
                                plot_baseline_ind = False,
                                UpperPercentile_UsageCap = UpperPercentile_UsageCap)
