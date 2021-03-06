__author__ = 'Jiaobei Zhang'
from pandas import DataFrame
from pandas import Series
import numpy as np
import pandas as pd
from scipy.optimize import leastsq
import datetime

from MonteCarloSimulators.Vasicek.VasicekAffine import VasicekAffine
from Curves.OIS.OISDaily import OIS
from Products.Credit.CDS.CDS import CDS

startdate = '2005-01-10'
enddate = '2010-01-10'
dateperiod = pd.date_range('2005-01-10','2010-01-10',freq='D')
x = [0.1,0.005,0.03,0.03]
y = [3,0.05,0.09,0.08]
recovery = 0.4
t_series = np.round(np.arange(0,365.001*30+6.001,1))
start=datetime.datetime(2005,1,10)
base = datetime.datetime.today()
datelist = [start + datetime.timedelta(days=x) for x in t_series]
datelist = [x.date() for x in datelist]

real_cds = pd.read_csv("BB CDS spread.csv", index_col="date", parse_dates=True)
real_cds = real_cds.fillna(method='ffill')
brz_cds = real_cds['Brazil']


def lsqR(para):
    ois = OIS(trim_start = startdate, trim_end = enddate)
    Affine = VasicekAffine(x, para, datelist)
    diff = np.subtract(ois.interpolationois(),Affine.calR())
    return diff

def lsqQ(para):
    ois = OIS(trim_start = startdate, trim_end = enddate)
    Affine = VasicekAffine(x, para, datelist)
    myCDS = CDS(ois.interpolationois(), datelist, Affine.calQ(), recovery)
    diff = np.subtract(brz_cds,myCDS.MTM())

calParaR = leastsq(lsqR,y)
calParaQ = leastsq(lsqQ,x)
