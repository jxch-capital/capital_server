import numpy as np
import pandas as pd
from multiprocessing import Pool
import core.yahoo_core as yc
from concurrent.futures import ThreadPoolExecutor


def calculate_correlation(args):
    input_df, sub_df = args
    return input_df.corrwith(sub_df).mean()


def find_similar_segments(input_df, large_df, window_size=None, threshold=0.9):
    window_size = window_size if window_size else len(input_df)
    the_similarity_indices = []
    with ThreadPoolExecutor() as executor:
        args = [(input_df, large_df.iloc[i:i + window_size]) for i in range(len(large_df) - window_size + 1)]
        correlations = executor.map(calculate_correlation, args)
        for i, correlation in enumerate(correlations):
            if correlation > threshold:
                the_similarity_indices.append(i)
    return the_similarity_indices


def normalize_segment(df):
    normalized_df = (df - df.min()) / (df.max() - df.min())
    return normalized_df


def find_similar_segments_by_codes(input_code, input_start_date, input_end_date, codes, all_start_date, threshold=0.9):
    input_yc = yc.download_codes([input_code], start_str=input_start_date, end_str=input_end_date)[0][['open', 'close', 'high', 'low']]
    normalized_input_df = normalize_segment(input_yc)

    for code in codes:
        the_yc = yc.download_codes([code], start_str=all_start_date)[0]
        large = the_yc[['open', 'close', 'high', 'low']]
        normalized_large_df = normalize_segment(large)

        similarity_indices = find_similar_segments(normalized_input_df, normalized_large_df, threshold=threshold)
        print(similarity_indices)

    # print(input_yc)



