def compute_MA(df, period, column="adjclose"):
    if column == 'adjclose' and column not in df.columns:
        column = 'close'
        print("[!] Warning! Column 'adjclose' not in dataframe. Using 'close'.")
    col = df[column]
    df['MA' + str(period)] = col.rolling(window=period).mean()
    return df

