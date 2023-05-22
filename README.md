# Data Analysis and Visualization with Tkinter

This project demonstrates how to perform some basic data analysis and create visualizations using Python, Tkinter, and Dask. The application allows users to explore multiple dataframes and perform exploratory data analysis, linear regression, and create various plots. Due to the size i was unable to upload the data i was working with. Refer to the data model pdf for what files and columns the application is expecting.

This application and use case i found online regarding mobile gaming and monetization. This was a very fun project to work on as it focused on some development aspects that i have not focused on in the past.

## Features

- Display multiple dataframes in separate tabs
- Perform exploratory data analysis (EDA) on a given dataframe
- Linear regression between two columns of a dataframe
- Generate bar and line charts for selected columns
- Customize text alignment, font size, and formatting in data tables
- Merge dataframes based on specified columns

## Prerequisites

Before running the application, make sure you have the following Python packages installed:

- pandas
- dask
- dask[dataframe]
- dask-ml
- matplotlib
- tk

You can install the required packages using pip:

```bash
pip install pandas dask[distributed] dask[dataframe] dask-ml matplotlib tk
```
### Insturctions to run the application
- Update the path where your data is stored in the variable subdir in dataframe_definition_service.py In a future iteration this would be a command line arguement but for now update this manually
- Run the main file from command line or open the maina file in your IDE and run that way.
