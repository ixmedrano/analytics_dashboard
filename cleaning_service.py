import dask.dataframe as dd

def ytd_read_and_clean_csv(subdir, file, year, groupby_col):
    df = dd.read_csv(subdir + file)
    df['event_date'] = dd.to_datetime(df['event_date'])
    df = df[df['event_date'].dt.year == year]
    df = df.groupby(groupby_col)['value_usd'].sum().reset_index().compute()
    df['id'] = df[groupby_col].astype(str)
    df.drop(groupby_col, axis=1, inplace=True)
    return df

def read_and_clean_csv(subdir,file):
    df = dd.read_csv(subdir + file)
    df['event_date'] = dd.to_datetime(df['event_date'])
    return df

def format_currency(value):
    return "${:,.2f}".format(value)

def read_and_clean_dim(subdir, file):
    df = dd.read_csv(subdir + file)
    return df

def clean_and_aggregate(df, groupby_col, agg_col):
    df = df.groupby(groupby_col)[agg_col].sum().reset_index().compute()
    df[groupby_col] = df[groupby_col].astype(str)
    df['value_usd'] = df[agg_col]
    df['id'] = df[groupby_col]
    df.drop(groupby_col, axis=1, inplace=True)
    df.drop(agg_col, axis=1, inplace=True)
    return df

def date_to_iso_week(df, date_field):
    df['iso_week'] = dd.to_datetime(df[date_field]).apply(lambda x: x.isocalendar()[1])
    df.drop(date_field, axis=1, inplace=True)
    df = df.sort_values('iso_week')
    return df