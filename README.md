# Layoffs Decoded

Demo website

http://ec2-3-94-101-23.compute-1.amazonaws.com:3000/

Introduction

This project aimed at providing valuable insights into this recent layoffs phenomenon and helping job seekers and public audiences navigates the uncertainty of the current job market. It utilizes a data-driven approach to analyze relevant data, such as financial data, employee data, and performance data, to deduce inferences and conclusions about the underlying reasons for the layoffs and the impacts of the layoffs on the company and its employees.

Questions:

1. How did the COVID-19 pandemic affect layoffs in the US? 
    - Were there more layoffs before, during, or after COVID-19? 
    - Identifying the factors affecting the layoffs. Like company size, and financial data like revenue, cost of revenue, etc.


2. Analyze possible factors affecting layoffs in the recent years and predicting future layoffs based on those factors.

3. What are the employee profiles (title, department, location) impacted by recent layoffs in the tech industry?




How to run the code for Q3:

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

