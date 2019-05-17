# Specification of 'normal' wind turbine operating behaviour for rapid anomaly detection: through the use of machine learning algorithms

by Nithiya Streethran (nmstreethran@gmail.com)

Files from my master's thesis, completed between May and August 2017 at Heriot-Watt University. I have now released these files under open-source licenses, so that anyone interested can make use of them. Please refer to the [contributing guidelines](/CONTRIBUTING.md) and [code of conduct](/CODE_OF_CONDUCT.md) if you would like to contribute, or contact me (nmstreethran@gmail.com) if you have any questions.

## Abstract

Maximising the economic effectiveness of a wind farm is essential in making wind a more economic source of energy. This effectiveness can be increased through the reduction of operation and maintenance costs, which can be achieved through continuously monitoring the condition of wind turbines. An alternative to expensive condition monitoring systems, which can be uneconomical especially for older wind turbines, is to implement classification algorithms on supervisory control and data acquisition (SCADA) signals, which are collected in most wind turbines. Several publications were reviewed, which were all found to use separate algorithms to predict specific faults in advance. In reality, wind turbines tend to have multiple faults which may happen simultaneously and have correlations with one another. This project focusses on developing a methodology to predict multiple wind turbine faults in advance simultaneously by implementing classification algorithms on SCADA signals for a wind farm with 25 turbines rated at 2,500 kW, spanning a period of 30 months. The data, which included measurements of wind speed, active power and pitch angle, was labelled using corresponding downtime data to detect normal behaviour, faults and varying timescales before a fault occurs. Three different classification algorithms, namely decision trees, random forests and k nearest neighbours were tested using imbalanced and balanced training data, initially to optimise a number of hyperparameters. The random forest classifier produced the best results. Upon conducting a more detailed analysis on the performance of specific faults, it was found that the classifier was unable to detect the varying timescales before a fault with accuracy comparable to that of normal or faulty behaviour. This could have been due to the SCADA data, which are used as features, being unsuitable for detecting the faults, and there is potential to improve this by balancing only these classes.

***Keywords***: wind turbine, classification algorithm, SCADA, fault detection, condition monitoring

## Description of files and folders

* [Final report](/Report.pdf) 
* [Code license](/LICENSE)
* [Report and image license](/LICENSE-CC-BY.md)
* [Jupyter notebooks with the codes used](/jupyter-notebooks/)
* [Images](/images/)

## Licenses

Unless otherwise stated:
* Code: [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
* Report and pictures: [![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
