"""
@author: pm

The following are two examples of finding the best fitting
    distribution given the data.
It only works for continuous distributions.

Run the porgram only by replacing row 26 by the data you want to check

For Beta distribution, this will provide 4 parameter values
    a, b, loc, scale = beta.fit(x)
    even though it only specifies beta(a,b)

All funtions used here are on
    http://docs.scipy.org/doc/scipy-0.16.1/reference/stats.html
"""

import matplotlib.pyplot as plt
import scipy.stats as st
import numpy as np
from scipy.integrate import simps #for integration of area


"""
data is the series of data for testing distribution
"""
data = np.random.gamma(4.0,scale=1.0, size=100000)
data=np.random.uniform(size=100000)

# Other distribution to try
# data = np.random.normal(loc=4.0,scale=1.0,size=100000)
# data = np.random.gumbel(loc=4.0,scale=1.0,size=100000)
# data.sort()

"""
Below is the generic source codes for fitting distributions
"""
## Test distribution fitting using Maximum Likelihood Function
hist_gram_bin_size = 100
# set num of top candidate distribtuions to display
top_distr_num = 5
# list of candidate distributions to choose from
distributions = [st.gamma, st.beta, st.rayleigh, st.norm, 
                 st.pareto, st.lognorm, st.laplace, st.uniform,
                 st.cauchy, st.weibull_max, st.weibull_min,
                 st.expon, st.f, st.gausshyper,
                 st.gengamma, st.invgamma, st.invgauss, st.invweibull,
                 st.logistic, st.powernorm, st.gumbel_l, st.gumbel_r,
                 st.exponnorm, st.exponweib]


x = np.linspace(np.min(data), np.max(data), num=10000)
top_distr_num = min(top_distr_num, len(distributions))
# print "Distributions to choose can be %s \n" %str(dir(st))

mles = []
h = plt.hist(data, bins=np.linspace(np.min(data), np.max(data), num=hist_gram_bin_size), color='w')

data_cache = {}
for distribution in distributions:
    pars = distribution.fit(data)
    mle = distribution.nnlf(pars, data)  # nnlf is -sum(log(probaiblity)), the negative MLE, actually
    pdf_fitted = distribution.pdf(x, *pars[:-2], loc=pars[-2], scale=pars[-1])
    # remark simps(pdf_fitted, x) should be
    pdf_fitted_scaled = pdf_fitted * (simps(h[0], h[1][-1*(len(h[0])):]) / simps(pdf_fitted, x))
    data_cache[distribution.name] =  (x,pdf_fitted_scaled, mle, pars)
    #plt.plot(x,pdf_fitted, label=distribution.name)
    #plt.xlim(np.min(x), np.max(x))
    mles.append(mle)

results = map(lambda x: (x[0].name, x[1]), zip(distributions, mles))
all_fits = sorted(zip(distributions, mles), key=lambda d: d[1])
best_fit = all_fits[0]
print 'Best fit reached using {}, Parameters: {}, MLE value: {}'.format(best_fit[0].name, 
                                map(lambda t: '%.2f' %t, data_cache[best_fit[0].name][3]) , best_fit[1])

# Display the graphs of best fittings orderd by ranking
for i in range(top_distr_num):
    distributionname = all_fits[i][0].name
    data_plot = data_cache[distributionname]
    plt.plot(data_plot[0], data_plot[1], label=distributionname)
    plt.xlim(np.min(x), np.max(x))
    plt.ylim(0, np.max(h[0]*1.05))
#plt.legend(loc='upper right')
plt.legend(loc='best')
plt.show()

# Show ranking of all fittings with MLE
print "Fitting quality ranking is as follows: "
for i in range(len(all_fits)):
    print all_fits[i][0].name, '; MLE:', all_fits[i][1], '; Parameters: ', \
              map(lambda t: '%.2f' %t, data_cache[all_fits[i][0].name][3])

