# Layoffs Decoded

Demo website

http://ec2-3-94-101-23.compute-1.amazonaws.com:3000/

## Introduction

This project aimed at providing valuable insights into this recent layoffs phenomenon and helping job seekers and public audiences navigates the uncertainty of the current job market. It utilizes a data-driven approach to analyze relevant data, such as financial data, employee data, and performance data, to deduce inferences and conclusions about the underlying reasons for the layoffs and the impacts of the layoffs on the company and its employees.

## Questions:

1. How did the COVID-19 pandemic affect layoffs in the US? 
    - Were there more layoffs before, during, or after COVID-19? 
    - Identifying the factors affecting the layoffs. Like company size, and financial data like revenue, cost of revenue, etc.


2. Analyze possible factors affecting layoffs in the recent years and predicting future layoffs based on those factors.

3. What are the employee profiles (title, department, location) impacted by recent layoffs in the tech industry?


## Folders:<br>

- `airflow_dags` : This folder contains files that are used to create directed acyclic graphs (DAGs) in Airflow.<br>

- `analysis` : This folder contains Jupyter notebooks that are used to perform various analyses on the data.<br>

- `backend` : This folder contains the server-side code for the project, implemented using Node.js and Express.js. This code provides an API that can be used by the frontend code to interact with the server<br>

- `data_preparation` : This folder contains code and scripts for preparing and cleaning data

    - `data_preparation/cleaning` : This folder contains scripts and code for cleaning and preprocessing data, such as removing duplicates, fixing formatting issues, or converting data types.
    - `data_preparation/er` : This folder contains scripts and code for performing entity resolution, which is the process of identifying and merging records on employee
    profile
    - `data_preparation/scraping` : This folder contains scripts and code for web scraping, which is the process of automatically extracting data from web pages.

- `frontend` : This folder contains the client-side code for the project, implemented using React and TypeScript. This code interacts with the server-side API provided by the backend code.<br>

## How to run the code for Q1:

1. How did the COVID-19 pandemic affect layoffs in the US? What are the top 10 factors that impacted layoffs during precovid, covid, and postcovid period?

We merged warn.csv dataset with nasdaq.csv dataset to map companies present in warn with their symbol names present in NASDAQ which was crucial to get financial data of each company through these symbol names using financial modelling prep API. In order to do that we had to do Entity Resolution as the company names were present in different manners across both these datasets. 

- Run `data_preparation/er/er.py` use the command below:

`spark-submit --jars /opt/hadoop/share/hadoop/tools/lib/aws-java-sdk-bundle-1.12.262.jar,/opt/hadoop/share/hadoop/tools/lib/hadoop-aws-3.3.4.jar er.py`

We executed this on SFU cluster `cluster.cs.sfu.ca` to utilize the elasticity and scale of resources on SFU cluster needed to execute 45k rows of warn. This produced the output file with matching company names and we kept all companies whose jaccard value>0.5. We wrote this warn_jaccard_0.5_cleaned.csv to AWS S3 after inspection. 

- Run `analysis/q1_train_data.ipynb` notebook where warn dataset is merged with financial dataset, covid dataset, comapny industry dataset, size of the company dataset which all come from different API sources like https://site.financialmodelingprep.com/developer/docs/ and https://ourworldindata.org/coronavirus. The notebook merged and divided all the data into different dataframes for precovid, covid and postcovid which is all written back to AWS S3. In case you run into errors related to import statements use below commands:
`pip3 install s3fs` and `pip3 install scikit-learn`

From here, we get 100+ column features for each time frame. We then apply different embedded, filter, wrapper method tehniques on them for feature selection to detemine top 10 factors as per different techniques that impacted layoffs during precovid, covid and postovid period. 

- Run `analysis/filter_method_extraction.ipynb` to apply Pearson and Spearman technique and get top features based on whose coefficient value is the highest. 
- Run `analysis/embedded_method_extraction.ipynb` to apply Ridge, Lasso, LogisticRegression, ElasticNet, DecisionTreeRegressor technique and get top features based on whose coefficient value is the highest.
- Run `analysis/wrapper_method_extraction.ipynb` to apply Forward Elimination, Backward Elimination, and Stepwise Elimination technique and get top features.
- Run `analysis/q1_overall_result.ipynb` file which aggregates all the number of workers laid off for each time period during precoid, covid and postcovid period and the result is fed into Athena tables.

All the output from above notebook is then written to AWS S3 from where it is fed into AWS Athena tables which is used by UI to render the output. The above answers our first question of which period saw the maximum number of layoffs in USA and what were the top factors that caused the layoff during each of covid, precovid and postcovid time period. 

## How to run the code for Q2:

## How to run the code for Q3:

1. Install the dependencies:

    `pip install -r requirement.txt`

2. Execute python files

Extract the employee profile data and transform into standardized locations

    python ./data_preparation/cleaning/employee_location.py

Extract the employee profile data and transform into standardized titles

    python ./data_preparation/er/1_standardize_title_employee_profile.py

Extract the employee profile data and transform into standardized departments

    python ./data_preparation/er/2_function_token_matching.py

    python ./data_preparation/er/3_token_department_combiner.py

