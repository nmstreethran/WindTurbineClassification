# WindTurbineClassification

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2875795.svg)](https://doi.org/10.5281/zenodo.2875795)

***Specification of 'normal' wind turbine operating behaviour for rapid anomaly detection: through the use of machine learning algorithms***

by Nithiya Streethran (nmstreethran at gmail dot com)

## Description of files

This repository is an archive of files created for my master's dissertation, which was completed between May and August 2017 at Heriot-Watt University and Natural Power Consultants. This was also my very first Python project. Unsurprisingly, these files needed some formatting to improve readability, which did after graduating with a master's degree in Renewable Energy Engineering. I did not make any major changes to the code, so this repository still contains a bunch of standalone scripts and not a package.

The `current` branch has the formatted code and dissertation files. The dissertation can be viewed [here](docs/nms_dissertation.pdf) [[PDF download](https://raw.githubusercontent.com/nmstreethran/WindTurbineClassification/current/docs/nms_dissertation.pdf)]. The original submission can be accessed using [this branch](https://github.com/nmstreethran/WindTurbineClassification/tree/b07072256df783c69c2736d1e38302d5df451887), or by downloading the [v1.0.0 archive](https://github.com/nmstreethran/WindTurbineClassification/releases/tag/v1.0.0) (also available on [Zenodo](https://doi.org/10.5281/zenodo.2875804)).

**Unfortunately, the datasets are proprietary and I do not own the rights to distribute them to the public.** As a result, I will not be making any further improvements to the code. If you would like me to explain the method I have used, or have any questions, please let me know, preferably through an [issue](https://github.com/nmstreethran/WindTurbineClassification/issues).

The list of dependencies can be found in `requirements.txt`. All Python scripts are organised into relevant directories in `scripts/`. The outputs of these scripts can be viewed in the Jupyter notebooks in `jupyter-notebooks/`. Tables and images used, in the form of `.png` and `.pdf` files, are in `images/`. The dissertation document, which is compiled using LaTeX, can be found in `docs/`.

## Document compilation

To compile the LaTeX document, use the following commands within the `docs` directory:

```sh
xelatex nms_dissertation.tex
biber nms_dissertation.tex
xelatex nms_dissertation.tex
xelatex nms_dissertation.tex
```

## Abstract

Maximising the economic effectiveness of a wind farm is essential in making wind a more economic source of energy. This effectiveness can be increased through the reduction of operation and maintenance costs, which can be achieved through continuously monitoring the condition of wind turbines. An alternative to expensive condition monitoring systems, which can be uneconomical especially for older wind turbines, is to implement classification algorithms on supervisory control and data acquisition (SCADA) signals, which are collected in most wind turbines. Several publications were reviewed, which were all found to use separate algorithms to predict specific faults in advance. In reality, wind turbines tend to have multiple faults which may happen simultaneously and have correlations with one another. This project focusses on developing a methodology to predict multiple wind turbine faults in advance simultaneously by implementing classification algorithms on SCADA signals for a wind farm with 25 turbines rated at 2,500 kW, spanning a period of 30 months. The data, which included measurements of wind speed, active power and pitch angle, was labelled using corresponding downtime data to detect normal behaviour, faults and varying timescales before a fault occurs. Three different classification algorithms, namely decision trees, random forests and k nearest neighbours were tested using imbalanced and balanced training data, initially to optimise a number of hyperparameters. The random forest classifier produced the best results. Upon conducting a more detailed analysis on the performance of specific faults, it was found that the classifier was unable to detect the varying timescales before a fault with accuracy comparable to that of normal or faulty behaviour. This could have been due to the SCADA data, which are used as features, being unsuitable for detecting the faults, and there is potential to improve this by balancing only these classes.

***Keywords:*** wind turbine, classification algorithm, SCADA, fault detection, condition monitoring

## License

Unless otherwise stated:

- Code and scripts are licensed under the [MIT License](https://opensource.org/licenses/MIT).
- the content, images and documentation are licensed under the [Creative Commons Attribution 4.0 International (CC BY 4.0) License](https://creativecommons.org/licenses/by/4.0/).
