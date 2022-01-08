import pandas as pd

from src.commons.process_dataframe import insert_new_col, insert_new_col_from_two_cols
from src.commons.process_number import cal_SEM


def get_percent_triplets(percentpairs):
    if percentpairs == 1:
        return 0
    elif percentpairs == 0.5:
        return 0.5
    elif percentpairs == 0:
        return 1
    else:
        raise Exception(f"percentpair {percentpairs} is unexpected")


if __name__ == '__main__':
    to_excel = False

    # read data
    PATH = "../data/ms2_uniform_mix_3_data/"
    DATA = "preprocessed_uniform_mix_3.xlsx"
    data = pd.read_excel(PATH + DATA)

    # convert percentpairs to percent_triplets
    insert_new_col(data, "perceptpairs", "percent_triplets", get_percent_triplets)

    dv = "deviation_score"
    dv2 = "percent_change"

    indv = "numerosity"
    indv2 = "protectzonetype"
    indv3 = "winsize"
    indv4 = "percent_triplets"
    indv5 = "participant"

    # average data: average deviation and percent change for each condition per participant
    data_1 = data.groupby([indv, indv2, indv3, indv4, indv5])[[dv, dv2]] \
        .agg({dv: ['mean', 'std'], dv2: ['mean', 'std']}) \
        .reset_index(level = [indv, indv2, indv3, indv4, indv5])

    # transfer column name
    data_1.columns = [''.join(x) for x in data_1.columns]

    data_1["samplesize"] = [4] * data_1.shape[0]  # each participant repeat each condition 4 times (4 displays)
    insert_new_col_from_two_cols(data_1, "deviation_scorestd", "samplesize", "SEM_deviation_score", cal_SEM)
    insert_new_col_from_two_cols(data_1, "percent_changestd", "samplesize", "SEM_percent_change", cal_SEM)

    # averaged across participant
    data_2 = data.groupby([indv, indv2, indv3, indv4])[[dv, dv2]] \
        .agg({dv: ['mean', 'std'], dv2: ['mean', 'std']}) \
        .reset_index(level = [indv, indv2, indv3, indv4])

    # transfer column name
    data_2.columns = [''.join(x) for x in data_2.columns]

    data_2["samplesize"] = [19*4] * data_2.shape[0]  # 4 displays * 19 participants
    insert_new_col_from_two_cols(data_2, "deviation_scorestd", "samplesize", "SEM_deviation_score", cal_SEM)
    insert_new_col_from_two_cols(data_2, "percent_changestd", "samplesize", "SEM_percent_change", cal_SEM)

    # average data: average deviation and percent change for for different winsize per participant
    data_3 = data.groupby([indv2, indv3, indv4, indv5])[[dv, dv2]] \
        .agg({dv: ['mean', 'std'], dv2: ['mean', 'std']}) \
        .reset_index(level = [indv2, indv3, indv4, indv5])

    # transfer column name
    data_3.columns = [''.join(x) for x in data_3.columns]

    data_3["samplesize"] = [12] * data_3.shape[0]  # 4 displays * 3 clustering
    insert_new_col_from_two_cols(data_3, "deviation_scorestd", "samplesize", "SEM_deviation_score", cal_SEM)
    insert_new_col_from_two_cols(data_3, "percent_changestd", "samplesize", "SEM_percent_change", cal_SEM)

    # average per winsize across participant
    data_4 = data.groupby([indv2, indv3, indv4])[[dv, dv2]] \
        .agg({dv: ['mean', 'std'], dv2: ['mean', 'std']}) \
        .reset_index(level = [indv2, indv3, indv4])

    # transfer column name
    data_4.columns = [''.join(x) for x in data_4.columns]

    data_4["samplesize"] = [12*19] * data_4.shape[0]  # 4 displays * 3 clustering * 19 participants
    insert_new_col_from_two_cols(data_4, "deviation_scorestd", "samplesize", "SEM_deviation_score", cal_SEM)
    insert_new_col_from_two_cols(data_4, "percent_changestd", "samplesize", "SEM_percent_change", cal_SEM)

    if to_excel:
        data_1.to_excel("ms2_uniform_mix_3_data_each_pp.xlsx", index = False)
        data_2.to_excel("ms2_uniform_mix_3.xlsx", index = False)
        data_3.to_excel("ms2_uniform_mix_3_combine_num_each_pp.xlsx", index = False)
        data_4.to_excel("ms2_uniform_mix_3_combine_num.xlsx", index = False)
