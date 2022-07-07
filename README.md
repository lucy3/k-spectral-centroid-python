# K-Spectral Centroid: Cluster Time Series by Shape, in Python

This algorithm is first introduced in the WSDM 2011 paper, "Patterns of Temporal Variation in Online Media" by Jaewon Yang and Jure Leskovec. 

This rewrites the MATLAB implementation found here: http://snap.stanford.edu/data/ksc.html

This implementation is invariant to time. That is, it does not search through different values of $q$, as defined in the original paper: http://ilpubs.stanford.edu:8090/984/1/paper-memeshapes.pdf. Feel free to submit a pull request to add this if you need it. 

Future possible improvements to this repo: 
- support for visualizing the centroid and time series in a pretty way 
