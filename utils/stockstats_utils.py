import stockstats


def stockstats_default(old_df):
    ss = stockstats.StockDataFrame.retype(old_df)
    df = ss[['open', 'close', 'high', 'low', 'volume',
             'tr', 'atr', 'close_-1_d', 'close_5_sma', 'close_20_sma', 'close_60_sma', 'close_120_sma', 'close_200_sma',
             'close_20_sma_-1_d', 'close_60_sma_-1_d', 'close_120_sma_-1_d', 'close_5_ema',
             'close_20_ema', 'close_60_ema', 'close_120_ema', 'close_20_ema_-1_d', 'close_200_ema',
             'macd', 'macds', 'macdh', 'kdjk', 'kdjd', 'kdjj']]
    df['rate_sma20'] = df['close_20_sma'] / (df['close_20_sma'] - df['close_20_sma_-1_d'])
    df['rate_ema20'] = df['close_20_ema'] / (df['close_20_ema'] - df['close_20_ema_-1_d'])
    df['rate_sma60'] = df['close_60_sma'] / (df['close_60_sma'] - df['close_60_sma_-1_d'])
    df['rate_ema60'] = df['close_60_ema'] / (df['close_60_ema'] - df['close_60_ema_-1_d'])
    df['rate_sma120'] = df['close_120_sma'] / (df['close_120_sma'] - df['close_120_sma_-1_d'])
    df['rate_ema120'] = df['close_120_ema'] / (df['close_120_ema'] - df['close_120_ema_-1_d'])
    df['rate_sma200'] = df['close_200_sma'] / (df['close_200_sma'] - df['close_200_sma_-1_d'])
    df['rate_ema200'] = df['close_200_ema'] / (df['close_200_ema'] - df['close_200_ema_-1_d'])
    ss = stockstats.StockDataFrame.retype(df)
    df['rate_ema20_5_ema'] = ss[['rate_ema20', 'rate_ema20_5_ema']]['rate_ema20_5_ema']
    df['rate_ema60_5_ema'] = ss[['rate_ema60', 'rate_ema60_5_ema']]['rate_ema60_5_ema']
    df['rate_ema120_5_ema'] = ss[['rate_ema120', 'rate_ema120_5_ema']]['rate_ema120_5_ema']
    df['rate_ema200_5_ema'] = ss[['rate_ema200', 'rate_ema200_5_ema']]['rate_ema200_5_ema']
    df.reset_index(inplace=True)
    return df
