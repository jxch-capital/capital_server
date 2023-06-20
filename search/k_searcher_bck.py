import numpy as np
import pandas as pd


def rolling_mean_std(df, window_size):
    cumsum = df.cumsum()
    cumsum_sq = (df ** 2).cumsum()
    sum_ = cumsum.iloc[window_size - 1:] - pd.concat([cumsum.iloc[:-window_size], pd.DataFrame([0] * df.shape[1], index=df.columns).T]).reset_index(drop=True)
    sum_sq = cumsum_sq.iloc[window_size - 1:] - pd.concat([cumsum_sq.iloc[:-window_size], pd.DataFrame([0] * df.shape[1], index=df.columns).T]).reset_index(drop=True)
    mean = sum_ / window_size
    variance = np.maximum(sum_sq / window_size - mean ** 2, 0)
    std = np.sqrt(variance)
    return mean, std


def find_similar_segments(input_df, large_df, window_size, threshold):
    the_similarity_indices = []
    input_mean, input_std = input_df.mean(), input_df.std()
    large_mean, large_std = rolling_mean_std(large_df, window_size)
    for i in range(len(large_df) - window_size + 1):
        sub_df = large_df.iloc[i:i + window_size]
        sub_mean, sub_std = large_mean.iloc[i], large_std.iloc[i]
        numerator = ((input_df - input_mean) * (sub_df - sub_mean)).sum()
        denominator = np.sqrt(((input_df - input_mean) ** 2).sum() * ((sub_df - sub_mean) ** 2).sum())
        correlation = (numerator / denominator).mean()
        if correlation > threshold:
            the_similarity_indices.append(i)
    return the_similarity_indices


def normalize_segment(df):
    normalized_df = (df - df.min()) / (df.max() - df.min())
    return normalized_df
