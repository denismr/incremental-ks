# Datasets

This folder contains the datasets that were used in our experimental evaluation.
All files are in the following format: each line is an instance with comma-separated features, where the last one is the class value.
A short description of each of each dataset follows.

- **Arabic \[3\]** contains audio features of $88$ people pronouncing Arabic digits between 0 and 9. 44 are females and 44 are males.
The task is to predict which digit was pronounced. The dataset was originally i.i.d. To artificially introduce drift, we separated the data stream in 4 parts of equal size.
These parts alternate between male and female voices. The stream has 8800 instances.
The original version of the dataset can be obtained through this [link](https://archive.ics.uci.edu/ml/datasets/Spoken+Arabic+Digit);
- **Posture \[4\]** contains data from a sensor that is carried by 5 different people. The task is to predict which movement is performed, among 11 possibilities.
This is the only dataset that is not balanced across all classes, thus we note that the proportion of the majority class is 33%. There are 164860 instances.
The dataset was originally i.i.d. To artificially introduce drift, the stream have segments of data that were produced by the same person.
The original version of the dataset can be obtained through this [link](https://archive.ics.uci.edu/ml/datasets/Localization+Data+for+Person+Activity);
- **Bike \[2\]** contains hourly count of rental bikes between years 2011 and 2012 in Capital bikeshare system with the corresponding weather and seasonal information.
The task is to predict whether there is high or low demand. We expect concept drift due to seasonality. It contains 17389 instances.
The original version of the dataset can be obtained through this [link](https://archive.ics.uci.edu/ml/datasets/Bike+Sharing+Dataset);
- **Keystroke \[5\]** contains features from five people typing the same password many times along the stream.
The task is to predict who is typing the password.
We expect concept drift since a person may type a password faster once they get used to it. there are 1600 instances;
- **Insects \[1\]** contains features from a laser sensor. The task is to identify the specimen of flying insect that is passing through the laser in a controlled environment,
among 5 possibilities.
Preliminary analysis showed that there is no drift in the feature space, however the prior distribution of the classes changes gradually over time. There are 5325 instances;
- **Abrupt Insects** is a modified version of the Insects dataset.
We shuffled the data to eliminate prior distribution changes.
After, we split the stream into $3$ segments. In the middle one, we shuffled all the features to introduce abrupt drift in the feature space, without inserting additional artifacts in the data.

## References

1. V. M. de Souza, D. F. Silva, G. E. Batista, et al. Clasification of data streams applied to insect recognition: Initial results. In _BRACIS_, pages 76--81. IEEE, 2013.
2. H. Fanaee-T and J. a. Gama. Event labeling combining ensemble detectors and background knowledge. _Progress in Artificial Intelligence_, pages 113--127, 2013.
3. N. Hammami and M. Bedda. Improved tree model for arabic speech recognition. In _ICCSIT_, volume 5, pages 521--526, 2010.
4. B. Kaluza, V. Mirchevska, E. Dovgan, M. Lustrek, and M. Gams. An agent-based approach to care in independent living. In _Aml_, pages 177--186. 2010.
5. V. M. de Souza, D. F. Silva, J. a. Gama, and G. E. Batista. Data streams classification guided by clustering on nonstationary environments and extreme verification latency. In _SDM_, pages 873--881. SIAM, 2015.