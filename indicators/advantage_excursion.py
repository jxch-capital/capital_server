def calculate(df, length=20):
    bull_ae_arr = []
    bear_ae_arr = []

    for index, row in df.iterrows():
        try:
            if index < len(df) - length:
                high = df.iloc[df.iloc[index:index + length]['high'].idxmax()]['high']
                low = df.iloc[df.iloc[index:index + length]['low'].idxmin()]['low']
                bull_mfe = (high - row['high']) / row['atr']
                bull_mae = (row['high'] - low) / row['atr']

                bear_mfe = (row['low'] - low) / row['atr']
                bear_mae = (high - row['low']) / row['atr']

                bull_ae = bull_mfe / bull_mae
                bear_ae = bear_mfe / bear_mae

                bull_ae_arr.append(bull_ae)
                bear_ae_arr.append(bear_ae)
            else:
                bull_ae_arr.append(None)
                bear_ae_arr.append(None)
        except BaseException:
            pass

    df['bull_ae'] = bull_ae_arr
    df['bear_ae'] = bear_ae_arr
    return df
