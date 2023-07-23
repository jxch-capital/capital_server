import datetime


def date_range(begin, end):
    range_list = []
    d = begin
    delta = datetime.timedelta(days=1)
    while d <= end:
        range_list.append(d)
        d += delta
    return range_list


def xaxes(begin, end, data):
    dr = date_range(begin, end)
    dr_str = list(map(lambda x: x.strftime("%Y-%m-%d"), dr))
    # 获取所有交易日
    data_str = list(map(lambda x: x.strftime("%Y-%m-%d"), data.index.tolist()))
    # 获取所有非交易日
    return list(filter(lambda x: x not in data_str, dr_str))
