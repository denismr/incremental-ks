# Fast Unsupervised Online Drift Detection - Supplementary Material

This repository contains supplementary material for the paper.

Paper information and download: http://www.kdd.org/kdd2016/subtopic/view/fast-unsupervised-online-drift-detection-using-incremental-kolmogorov-smirn .

*Important note:* IKS runs on the assumption that all the observations are unique. If it is not the case, the computed D statistic may not be exact (it can be higher than it should).

*Important note 2:* the version of Arabic that was used in the paper was utterly broken. This repository contains the fixed version. The corrects results are the following:

| Measurament            | BL1   | MR    | AB    | TL    |
| ---------------------- | ----- | ----- | ----- | ----- |
| Accuracy               | 52.00 | 60.12 | 58.83 | 59.78 |
| % Required True Labels |  5.68 | 28.41 |  5.68 | 100.0 |


## Important changes

- Added support to Kuiper's Test
- Fixed a bug where using non-unique observations could permanently damage the IKS

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