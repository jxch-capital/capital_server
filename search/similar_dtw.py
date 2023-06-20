from scipy.spatial.distance import euclidean
from fastdtw import fastdtw


def normalize_segment(df):
    normalized_df = (df - df.min()) / (df.max() - df.min())
    return normalized_df


def calculate_similarity(arr1, arr2):
    distance, _ = fastdtw(arr1, arr2, dist=euclidean)
    return 1 / (1 + distance)


def find_similar_segments(input_arr, large_arr, window_size=None, threshold=0.2):
    window_size = window_size if window_size else len(input_arr)
    n_input_arr = normalize_segment(input_arr)
    similarity_dict = {}
    for i in range(large_arr.shape[0] - window_size + 1):
        sub_arr = normalize_segment(large_arr[i:i + window_size])
        similarity = calculate_similarity(n_input_arr, sub_arr)
        if similarity > threshold:
            similarity_dict[i] = similarity
    return similarity_dict


def find_index(similarity_dict, threshold):
    return [index for index, similarity in similarity_dict.items() if similarity > threshold]


def find_index_sorted(similarity_dict):
    return [index for index, similarity in sorted(similarity_dict.items(), key=lambda x: x[1], reverse=True)]
