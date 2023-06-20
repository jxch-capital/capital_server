import numpy as np
import pandas as pd
from numba import njit


@njit
def calculate_correlation(input_array, sub_array):
    input_mean = input_array.sum(axis=0) / input_array.shape[0]
    sub_mean = sub_array.sum(axis=0) / sub_array.shape[0]
    numerator = ((input_array - input_mean) * (sub_array - sub_mean)).sum(axis=0)
    denominator = np.sqrt(((input_array - input_mean) ** 2).sum(axis=0) * ((sub_array - sub_mean) ** 2).sum(axis=0))
    correlation = (numerator / denominator).mean()
    return correlation


def find_similar_segments(input_df, large_df, window_size, threshold):
    the_similarity_indices = []
    input_array = input_df.to_numpy()
    for i in range(len(large_df) - window_size + 1):
        sub_df = large_df.iloc[i:i + window_size]
        sub_array = sub_df.to_numpy()
        correlation = calculate_correlation(input_array, sub_array)
        if correlation > threshold:
            the_similarity_indices.append(i)
    return the_similarity_indices


def normalize_segment(df):
    normalized_df = (df - df.min()) / (df.max() - df.min())
    return normalized_df
