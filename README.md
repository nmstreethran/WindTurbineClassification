# WindTurbineClassification

[![DOI](images/badges/doi.svg)](https://doi.org/10.5281/zenodo.2875795)
[![View documentation (PDF)](images/badges/pdf.svg)](https://raw.githubusercontent.com/nmstreethran/WindTurbineClassification/current/docs/nms_dissertation.pdf)

***Specification of 'normal' wind turbine operating behaviour for rapid anomaly detection: through the use of machine learning algorithms***

by Nithiya Streethran (nmstreethran at gmail dot com)

This work is derived from my dissertation for the degree of Master of Science (MSc) in Renewable Energy Engineering at Heriot-Watt University, which was completed during a technical placement at Natural Power between May and August 2021.

**Unfortunately, the datasets are proprietary and I do not own the rights to distribute them to the public.** If you have any questions, please feel free to contact me, or start a discussion [here](https://github.com/nmstreethran/WindTurbineClassification/discussions).

## Abstract

Maximising the economic effectiveness of a wind farm is essential in making wind a more economic source of energy. This effectiveness can be increased through the reduction of operation and maintenance costs, which can be achieved through continuously monitoring the condition of wind turbines. An alternative to expensive condition monitoring systems, which can be uneconomical especially for older wind turbines, is to implement classification algorithms on supervisory control and data acquisition (SCADA) signals, which are collected in most wind turbines. Several publications were reviewed, which were all found to use separate algorithms to predict specific faults in advance. In reality, wind turbines tend to have multiple faults which may happen simultaneously and have correlations with one another. This project focusses on developing a methodology to predict multiple wind turbine faults in advance simultaneously by implementing classification algorithms on SCADA signals for a wind farm with 25 turbines rated at 2,500 kW, spanning a period of 30 months. The data, which included measurements of wind speed, active power and pitch angle, was labelled using corresponding downtime data to detect normal behaviour, faults and varying timescales before a fault occurs. Three different classification algorithms, namely decision trees, random forests and k nearest neighbours were tested using imbalanced and balanced training data, initially to optimise a number of hyperparameters. The random forest classifier produced the best results. Upon conducting a more detailed analysis on the performance of specific faults, it was found that the classifier was unable to detect the varying timescales before a fault with accuracy comparable to that of normal or faulty behaviour. This could have been due to the SCADA data, which are used as features, being unsuitable for detecting the faults, and there is potential to improve this by balancing only these classes.

***Keywords:*** wind turbine, classification algorithm, SCADA, fault detection, condition monitoring

## Document compilation

To compile the LaTeX document, use the following command within the `docs` directory:

```sh
arara nms_dissertation.tex
```

## License

Unless otherwise stated:

- Code and scripts are licensed under the [MIT License](https://opensource.org/licenses/MIT).
- Content, images, and documentation are licensed under a [Creative Commons Attribution 4.0 International (CC-BY-4.0) License](https://creativecommons.org/licenses/by/4.0/).

Project badges are generated using [Shields.io](https://shields.io/) and [Simple Icons](https://simpleicons.org/).
