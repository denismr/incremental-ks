# Fast Unsupervised Online Drift Detection - Supplementary Material

This repository contains supplemental material for the paper.

Paper download: http://www.kdd.org/kdd2016/papers/files/rpp0427-dos-reisA.pdf .

**Update (17/12/2019)**
I updated the codebase. The most notable improvements are:
  * Python code is finally properly documented;
  * All versions have methods to generate proper thresholds for the KS test, given any p-value. Finding the p-value given the KS statistic is easily achievable with a binary search in the interval `(0, 1)` using such new methods;
  * Python code was splitted into two options: pure python (not recommended) and FFI (must compile the C++ wrapper as a dynamic library. I'll release the latest version for Windows and MacOS). Both versions have the same interface and can be swapped;
  * All versions support values in the form of tuples containing a random value to resolve ties between observations. This is intented as an workaround for the important note below. `testing_single_stream_rnd_factor.py` exemplifies how to do this, in Python;
  * Incremental KS - Sliding Window (`IKSSW.py`) was completely rewritten (although it is interface-compatible with the previous version). The new version implements the strategy of coupling observations with random numbers for ties. This fact is transparent to the user.


**Important note:** IKS runs on the assumption that all the observations are unique. If it is not the case, the computed D statistic may not be exact (it can be higher than it should). Datasets with real numbers have mostly unique values. However, this assumption is always compromised when we have a reference window and a sliding window that starts with the same values as the reference window. Two possible workarounds for this setting:
  1. use standard KS test while there is overlap between the sliding window and the reference window; 
  2. make all observations pairs where the second value is a randomized number to avoid ties (preferable).

## Performance Example

Benchmark file is `testing_parallel_streams.py`. Look it up for more details. In summary, two streams of 5000 values and two corresponding sliding windows of 500 values. I'm using the FFI version. The CPU where the code ran is an i7 4790.

```
Elapsed time for IKS to process stream: 0.05 sec
Elapsed time for ks_2samp to process stream: 1.57 sec
Maximum difference between IKS and ks_2samp: 1.1102230246251565e-16
```

## Paper-related Errata

the version of Arabic that was used in the paper was utterly broken due to wrong preprocessing. This repository contains the fixed version. The corrects results are the following:

| Measurament            | BL1   | MR    | AB    | TL    |
| ---------------------- | ----- | ----- | ----- | ----- |
| Accuracy               | 61.77 | 78.11 | 72.88 | 78.24 |
| % Required True Labels |  5.68 | 45.45 | 11.36 | 100.0 |
| # Model Replacements   |     0 |     7 |     1 |  8300 |
| # AB Adaptations       |     0 |     0 |   183 |     0 |


## Current Contents

- Datasets that were used in the experiments
- Incremental Kolmogorov-Smirnov implementation
  - Treap with lazy propagation implementation

## F.A.Q.

1. How the alpha/beta transformation is done?
*Answer:* f(v) = (v - mu\_ref) \* sigma\_cur / sigma\_ref + mu\_cur, where mu\_ref and mu\_cur are the means for the reference and current samples, respectively, and sigma\_ref and sigma\_cur are the standard deviations for the reference and current samples, respectively.
