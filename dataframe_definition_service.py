import dask.dataframe as dd
import cleaning_service as cs
import argparse

subdir = "F:/Storage/analytics_engineer/data/"
# year to date
year = 2022
# Define default Dataframes
adspend_df = cs.read_and_clean_csv(subdir, 'adspend.csv')
payout_df = cs.read_and_clean_csv(subdir, 'payouts.csv')
revenue_df = cs.read_and_clean_csv(subdir, 'revenue.csv')
installs_df = cs.read_and_clean_csv(subdir, 'installs.csv')
# Define Agg Dataframes
revenue_by_install = cs.ytd_read_and_clean_csv(subdir, 'revenue.csv', year, 'install_id')
payouts_by_install = cs.ytd_read_and_clean_csv(subdir, 'payouts.csv', year, 'install_id')
adspend_by_country = cs.ytd_read_and_clean_csv(subdir, 'adspend.csv', year, 'country_id')
adspend_by_network = cs.ytd_read_and_clean_csv(subdir, 'adspend.csv', year, 'network_id')
adspend_by_client = cs.ytd_read_and_clean_csv(subdir, 'adspend.csv', year, 'client_id')
install_dim = cs.read_and_clean_dim(subdir, 'installs.csv')
install_dim['id'] = install_dim['install_id'].astype(str)
install_dim.drop(['install_id'], axis=1)
# Define Time Series
revenue_by_date = cs.ytd_read_and_clean_csv(subdir, 'revenue.csv', year, 'event_date')
payouts_by_date = cs.ytd_read_and_clean_csv(subdir, 'payouts.csv', year, 'event_date')
adspend_by_date = cs.ytd_read_and_clean_csv(subdir, 'adspend.csv', year, 'event_date')
revenue_by_week = cs.date_to_iso_week(revenue_by_date, 'id')
payouts_by_week = cs.date_to_iso_week(payouts_by_date, 'id')
adspend_by_week = cs.date_to_iso_week(adspend_by_date, 'id')
# Clean metrics
revenue_sum = cs.format_currency(revenue_by_install['value_usd'].sum())
revenue_average = cs.format_currency(revenue_by_install['value_usd'].mean())
payouts_sum = cs.format_currency(payouts_by_install['value_usd'].sum())
payouts_average = cs.format_currency(payouts_by_install['value_usd'].mean())
adspend_country_sum = cs.format_currency(adspend_by_country['value_usd'].sum())
profit_sum = cs.format_currency(revenue_by_install['value_usd'].sum() - payouts_by_install['value_usd'].sum() - adspend_by_country['value_usd'].sum())
# Define Top 10
top_spenders = revenue_by_install.nlargest(10, 'value_usd')
top_payouts = payouts_by_install.nlargest(10, 'value_usd')
# Define Merged Dataframe
merged_df = dd.merge(revenue_by_install, payouts_by_install, on='id', suffixes=('_revenue', '_payouts')).reset_index()
merged_df = dd.merge(merged_df, install_dim, on='id').reset_index()
# Define Install Dim Aggregates
rev_country_df = cs.clean_and_aggregate(merged_df,'country_id','value_usd_revenue')
pay_country_df = cs.clean_and_aggregate(merged_df,'country_id','value_usd_payouts')
rev_network_df = cs.clean_and_aggregate(merged_df,'network_id','value_usd_revenue')
pay_network_df = cs.clean_and_aggregate(merged_df,'network_id','value_usd_payouts')
rev_os_df = cs.clean_and_aggregate(merged_df,'device_os_version','value_usd_revenue')
pay_os_df = cs.clean_and_aggregate(merged_df,'device_os_version','value_usd_payouts')
# Define Adspend Dim Aggregates
rev_adspend_country_df = dd.merge(rev_country_df, adspend_by_country, on='id', suffixes=('_rev', '_adspend')).reset_index()
rev_adspend_network_df = dd.merge(rev_network_df, adspend_by_network, on='id', suffixes=('_rev', '_adspend')).reset_index()
pay_adspend_country_df = dd.merge(pay_country_df, adspend_by_country, on='id', suffixes=('_pay', '_adspend')).reset_index()
pay_adspend_network_df = dd.merge(pay_network_df, adspend_by_network, on='id', suffixes=('_pay', '_adspend')).reset_index()
rev_pay_country_df = dd.merge(rev_country_df, pay_country_df, on='id', suffixes=('_rev', '_pay')).reset_index()
rev_pay_network_df = dd.merge(rev_network_df, pay_network_df, on='id', suffixes=('_rev', '_pay')).reset_index()
rev_pay_os_df = dd.merge(rev_os_df, pay_os_df, on='id', suffixes=('_rev', '_pay')).reset_index()
# Define Unsupervised learning data frame
full_df = dd.merge(installs_df, adspend_df, on=['event_date', 'country_id', 'network_id'], how='left', suffixes=('', '_adspend'))
full_df = dd.merge(merged_df, revenue_df, on='install_id', how='left', suffixes=('', '_revenue'))
full_df = dd.merge(merged_df, payout_df, on='install_id', how='left', suffixes=('', '_payout'))

