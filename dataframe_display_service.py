import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import dask.dataframe as dd
import dask_ml.model_selection as dcv
from dask_ml.linear_model import LinearRegression
from dask_ml.metrics import mean_squared_error, r2_score



def dataframe_tab(notebook, df, title, label_col='id', value_col='value_usd'):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=title)
    # Round the values of the value_col
    df[value_col] = df[value_col].round(2)

    # Aggregate the 'value_usd' column
    aggregated_data = df.groupby(label_col)[value_col].sum().reset_index()

    # Create the bar chart
    figure = plt.Figure(figsize=(5, 4), dpi=100)
    ax = figure.add_subplot(111)
    aggregated_data.plot(kind='bar', x=label_col, y=value_col, ax=ax)
    ax.set_title(title)
    chart = FigureCanvasTkAgg(figure, frame)
    chart.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Create the Treeview
    treeview = ttk.Treeview(frame)
    treeview["columns"] = list(df.columns)
    treeview["show"] = "headings"

    for column in df.columns:
        treeview.heading(column, text=column, anchor=tk.W)
        treeview.column(column, anchor=tk.W)

    for index, row in df.iterrows():
        treeview.insert("", "end", values=list(row))

    treeview.pack(expand=True, fill="both")

    return treeview

def dataframe_tab_2_values(notebook, df, title, label_col='id', value_col1='value_usd_rev', value_col2='value_usd_adspend'):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=title)
    # Round the values of the value_col
    df[value_col1] = df[value_col1].round(2)
    df[value_col2] = df[value_col2].round(2)

    # Aggregate the value columns
    aggregated_data = df.groupby(label_col)[[value_col1, value_col2]].sum().reset_index()

    # Create the bar chart
    figure = plt.Figure(figsize=(5, 4), dpi=100)
    ax = figure.add_subplot(111)
    aggregated_data.plot(kind='bar', x=label_col, y=value_col1, ax=ax, label=value_col1, position=0, width=0.4, color='blue')
    aggregated_data.plot(kind='bar', x=label_col, y=value_col2, ax=ax, label=value_col2, position=1, width=0.4, color='red')
    ax.set_title(title)
    ax.legend()
    chart = FigureCanvasTkAgg(figure, frame)
    chart.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Create the Treeview
    treeview = ttk.Treeview(frame)
    treeview["columns"] = list(df.columns)
    treeview["show"] = "headings"

    for column in df.columns:
        treeview.heading(column, text=column, anchor=tk.W)
        treeview.column(column, anchor=tk.W)

    for index, row in df.iterrows():
        treeview.insert("", "end", values=list(row))

    treeview.pack(expand=True, fill="both")

    return treeview

def line_chart_tab(notebook, title, df1, df2, df3, iso_week_col='iso_week', value_col='value_usd'):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=title)

    # Create the line chart
    figure = plt.Figure(figsize=(5, 4), dpi=100)
    ax = figure.add_subplot(111)
    df1.plot(x=iso_week_col, y=value_col, ax=ax, label='revenue_by_week', color='blue')
    df2.plot(x=iso_week_col, y=value_col, ax=ax, label='payouts_by_week', color='red')
    df3.plot(x=iso_week_col, y=value_col, ax=ax, label='adspend_by_week', color='green')
    ax.set_title(title)
    ax.legend()
    chart = FigureCanvasTkAgg(figure, frame)
    chart.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    return chart

def eda_tab(df, tab_control):
    eda_results = perform_eda(df)

    # Create a new tab for EDA
    eda_tab = ttk.Frame(tab_control)
    tab_control.add(eda_tab, text="EDA")
    tab_control.pack(expand=1, fill="both")

    # Create a canvas and scrollbar inside the new tab
    canvas = tk.Canvas(eda_tab)
    scrollbar = tk.Scrollbar(eda_tab, orient="vertical", command=canvas.yview)
    content_frame = ttk.Frame(canvas)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    canvas.create_window((0, 0), window=content_frame, anchor="nw", tags="content_frame")
    content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Display EDA results in the content_frame
    row = 0
    for key, value in eda_results.items():
        label = ttk.Label(content_frame, text=key, font=("Helvetica", 12, "bold"))
        label.grid(row=row, column=0, sticky="w")
        row += 1

        if isinstance(value, dd.DataFrame) or isinstance(value, dd.DataFrame):
            text = tk.Text(content_frame, wrap=tk.WORD)
            text.insert(tk.END, value.to_string())
            text.grid(row=row, column=0, sticky="w")
        elif isinstance(value, dict):
            for k, v in value.items():
                text = tk.Text(content_frame, wrap=tk.WORD)
                text.insert(tk.END, f"{k}:\n{v.to_string()}")
                text.grid(row=row, column=0, sticky="w")
                row += 1
        else:
            text = tk.Text(content_frame, wrap=tk.WORD)
            text.insert(tk.END, str(value))
            text.grid(row=row, column=0, sticky="w")

        row += 1

def perform_eda(df):
    eda_results = {}

    # Compute summary statistics for numerical columns
    numerical_columns = ['value_usd', 'value_usd_revenue', 'value_usd_payouts']
    stats = df[numerical_columns].describe().compute()
    eda_results["Summary Statistics"] = stats

    # Analyze the distribution of categorical columns
    categorical_columns = ['country_id', 'app_id', 'network_id', 'device_os_version', 'id']
    distributions = {}
    for col in categorical_columns:
        distributions[col] = df[col].value_counts().compute()
    eda_results["Categorical Columns Distribution"] = distributions

    # Look for missing values in the data
    missing_values = df.isnull().sum().compute()
    eda_results["Missing Values"] = missing_values

    return eda_results

def linear_regression_tab(df, col1, col2, tab_control, title):
    # Drop rows with missing values
    df = df.dropna(subset=[col1, col2])

    # Prepare the feature matrix (X) and target vector (y)
    X = df[[col1]].to_dask_array(lengths=True)
    y = df[col2].to_dask_array(lengths=True)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = dcv.train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a linear regression model and fit it to the training data
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions on the test data
    y_pred = model.predict(X_test)

    # Calculate the mean squared error and R-squared score
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Create a new tab for linear regression results
    lr_tab = ttk.Frame(tab_control)
    tab_control.add(lr_tab, text=title)
    tab_control.pack(expand=1, fill="both")

    # Display the results in the new tab
    results = f"Mean Squared Error: {mse:.2f}\nR-squared Score: {r2:.2f}"
    results_text = tk.Text(lr_tab, wrap=tk.WORD)
    results_text.insert(tk.END, results)
    results_text.pack(fill=tk.BOTH, expand=True)