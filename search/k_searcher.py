import numpy as np
import pandas as pd


def normalize_segment(df):
    normalized_df = (df - df.min()) / (df.max() - df.min())
    return normalized_df


def find_similar_segments(input_df, large_df, window_size, threshold):
    the_similarity_indices = []
    for i in range(len(large_df) - window_size + 1):
        sub_df = large_df.iloc[i:i + window_size]
        correlation = input_df.corrwith(sub_df, axis=1).mean()
        if correlation > threshold:
            the_similarity_indices.append(i)
    return the_similarity_indices
