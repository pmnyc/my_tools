# DP_means
Dirichlet Process K-means

### Description

DP K-means is a bayesian non-parametric extension of the K-means algorithm based on small variance assymptotics (SVA) approximation of the Dirichlet Process Mixture Model.

<p align="center">
<img src="https://github.com/vsmolyakov/DP_means/blob/master/matlab/figures/dp_means.png?raw=true"/>
</p>

It doesn't require prior knowledge of the number of clusters K. The cluster penalty parameter lambda is set based on the data by taking the maximum distance to the K++ means initialization. Normalized Mutual Information (NMI) is used to compare posterior cluster assignments with the ground truth.

### Reference

B. Kulis and M. Jordan, "Revisiting k-means: New Algorithms via Bayesian Nonparametrics"
 
### Dependencies

Matlab 2015a  
Python 2.7  
Eigen3
