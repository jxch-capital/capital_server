from fastdtw import fastdtw
from sklearn.preprocessing import normalize
import numpy as np


def find_similar_sub_sequences(arr, ref, threshold):
    base_len = len(ref)
    arr = np.array(arr)
    ref = np.array(ref)
    item_arr, result = [], []
    for index in range(len(arr)):
        item_arr.extend([arr[index:i] for i in range(index + base_len, len(arr) + 1)])

    for item in item_arr:
        dist, _ = fastdtw(normalize(item), normalize(ref))
        if dist < threshold:
            result.append(item.tolist())
    return result


def find_similar_sequences(arr, ref, threshold):
    base_len = len(ref)
    arr = np.array(arr)
    ref = np.array(ref)

    result = []
    for index in range(len(arr) - base_len):
        item = arr[index:index + base_len]

        dist, _ = fastdtw(normalize(item), normalize(ref))
        if dist < threshold:
            result.append({
                'k': item,
                'dist': dist,
                'index': index
            })

    result.sort(key=lambda p: p['dist'])
    return result

