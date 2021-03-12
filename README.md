# DT2VIS: A focus+context answer generation system to facilitate visual exploration of tabular data

This repository contains source code used for visual dialogue analysis system in the DT2VIS paper. Note that the code was tested with Python 3. Please python 3 as your test environment.

## Web Demo
For convenience, we provide a app (server/app.py) that runs the visual dialogue analysis system, DT2VIS. We also provide [DT2VIS's project website](http://dt2vis.godoorsun.org:45186/) and [DT2VIS's alternate website.](http://dt2vis2.godoorsun.org:45186/)  
Overview of the online system is shown as follow.
![](https://github.com/jiangqicd/DT2VIS/blob/main/overview.png)
The user interface of DT2VIS system includes five views. User can select analysis dataset and overview the dataset in data detail view. Query sentence is input in query input view. User can view the details of the answer in main view, and side answer view provides other alternative answers. Recommendation view provide the follow up query recommended, Query history view shoews the history of user’s queries

## Introduction
DT2VIS takes a natural language query about a given dataset as input and outputs a focus+context answer, and conducts users to explore. The workflow of the system is as follow.
![](https://github.com/jiangqicd/DT2VIS/blob/main/pipline.png)

## **Install Dependencies**
The DT2VIS code has a few dependencies that can be installed using the requirement.txt file,
In addition, the system also needs stanford-parser.jar and stanford-parser-models.jar.

## Contact
If you have any questions, feel free to open an issue or contact [Guodao Sun](http://godoorsun.org).
