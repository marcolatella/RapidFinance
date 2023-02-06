def compute_MA(data, period, column="adjclose"):
    if column == 'adjclose' and column not in data.columns:
        column = 'close'
        print("[!] Warning! Column 'adjclose' not in dataframe. Using 'close'.")
    col = data[column]
    data['MA'+str(period)] = col.rolling(window=period).mean()
    return data

