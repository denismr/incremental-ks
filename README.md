# Fast Unsupervised Online Drift Detection - Supplementary Material

This repository contains supplementary material for the paper.

Paper information and download: http://www.kdd.org/kdd2016/subtopic/view/fast-unsupervised-online-drift-detection-using-incremental-kolmogorov-smirn .

## Current Contents

- Datasets that were used in the experiments
- Incremental Kolmogorov-Smirnov implementation
  - Treap with lazy propagation implementation

## TO DO List:

- insert new plots and additional experimental results
- upload code for all reported experiments

## F.A.Q.

1. How the alpha/beta transformation is done?
*Answer:* f(v) = (v - mu\_ref) \* sigma\_cur / sigma\_ref + mu\_cur, where mu\_ref and mu\_cur are the means for the reference and current samples, respectively, and sigma\_ref and sigma\_cur are the standard deviations for the reference and current samples, respectively.