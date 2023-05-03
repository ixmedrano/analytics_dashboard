
import dataframe_display_service as dds
import tkinter as tk
from tkinter import ttk
from dataframe_definition_service import profit_sum, revenue_sum, payouts_sum, adspend_country_sum, revenue_average, payouts_average, top_payouts, top_spenders, adspend_by_client, rev_adspend_country_df, rev_adspend_network_df, rev_pay_country_df, pay_adspend_country_df, pay_adspend_network_df, rev_pay_network_df, rev_pay_os_df, revenue_by_week, payouts_by_week, adspend_by_week, full_df



def main():

    # Define Home Frame
    large_bold_font = ("Helvetica", 14, "bold")
    root = tk.Tk()
    root.title('Analytics Engine Case')
    notebook = ttk.Notebook(root)
    home_frame = tk.Frame(notebook)
    notebook.add(home_frame, text='Home')
    home_label = tk.Label(home_frame, text='Welcome to the Analytics Engine!', font=large_bold_font)
    home_label.pack(padx=10, pady=10)
    # Define EDA Tab
    window = tk.Tk()
    window.title("EDA")
    tab_control = ttk.Notebook(window)
    # Display Metrics in Home
    text_var4 = tk.StringVar()
    text_var4 = tk.StringVar()
    text_var4.set(f"YTD Profit: {profit_sum}")
    label4 = tk.Label(home_frame, textvariable=text_var4, font=large_bold_font)
    label4.pack(padx=20, pady=5, fill=tk.X)
    text_var1 = tk.StringVar()
    text_var1.set(f"YTD Revenue: {revenue_sum}")
    label1 = tk.Label(home_frame, textvariable=text_var1, font=large_bold_font)
    label1.pack(padx=20, pady=5, fill=tk.X)
    text_var2 = tk.StringVar()
    text_var2.set(f"YTD Payouts: {payouts_sum}")
    label2 = tk.Label(home_frame, textvariable=text_var2, font=large_bold_font)
    label2.pack(padx=20, pady=5, fill=tk.X)
    text_var3 = tk.StringVar()
    text_var3.set(f"YTD Adspend: {adspend_country_sum}")
    label3 = tk.Label(home_frame, textvariable=text_var3, font=large_bold_font)
    label3.pack(padx=20, pady=5, fill=tk.X)
    text_var5 = tk.StringVar()
    text_var5.set(f"Average Revenue By Install: {revenue_average}")
    label5 = tk.Label(home_frame, textvariable=text_var5, font=large_bold_font)
    label5.pack(padx=20, pady=5, fill=tk.X)
    text_var6 = tk.StringVar()
    text_var6.set(f"Average Payouts By Install: {payouts_average}")
    label6 = tk.Label(home_frame, textvariable=text_var6, font=large_bold_font)
    label6.pack(padx=20, pady=5, fill=tk.X)

    # Define Tabs
    dds.dataframe_tab(notebook, top_spenders, 'Top Spenders')
    dds.dataframe_tab(notebook, top_payouts, 'Top Payouts')
    dds.dataframe_tab(notebook, adspend_by_client, 'Adspend by Client')
    dds.dataframe_tab_2_values(notebook, rev_adspend_country_df, 'Rev Adspend by Country')
    dds.dataframe_tab_2_values(notebook, rev_adspend_network_df, 'Rev Adspend by Network')
    dds.dataframe_tab_2_values(notebook, pay_adspend_country_df, 'Pay Adspend by Country', value_col1='value_usd_pay', value_col2='value_usd_adspend')
    dds.dataframe_tab_2_values(notebook, pay_adspend_network_df, 'Pay Adspend by Network', value_col1='value_usd_pay', value_col2='value_usd_adspend')
    dds.dataframe_tab_2_values(notebook, rev_pay_country_df, 'Rev Pay by Country', value_col1='value_usd_rev', value_col2='value_usd_pay')
    dds.dataframe_tab_2_values(notebook, rev_pay_network_df, 'Rev Pay by Network', value_col1='value_usd_rev', value_col2='value_usd_pay')
    dds.dataframe_tab_2_values(notebook, rev_pay_os_df, 'Rev Pay by OS', value_col1='value_usd_rev', value_col2='value_usd_pay')
    dds.line_chart_tab(notebook, 'Weekly Time Series', revenue_by_week, payouts_by_week, adspend_by_week)
    dds.eda_tab(full_df, tab_control)
    dds.linear_regression_tab(full_df,'value_usd','value_usd_revenue', notebook, 'Adspend and Revenue')
    dds.linear_regression_tab(full_df,'value_usd_payouts','value_usd_revenue', notebook, 'Payouts and Revenue')
#    Create time series chart and time series anomoly detection chart
    style = ttk.Style()
    style.theme_use('clam')
    notebook.pack(expand=True, fill='both')
    root.mainloop()


if __name__ == '__main__':
    main()
