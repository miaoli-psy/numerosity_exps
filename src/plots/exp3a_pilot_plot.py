# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2020-12-22 21:15
IDE: PyCharm
Introduction:
"""
import matplotlib.pyplot as plt
import pandas as pd


def __get_label4plot(condi: str) -> str:
    if condi == "rc_pc":
        return "crowding reference and crowding probe"
    elif condi == "rc_pnc":
        return "crowding reference and no-crowding probe"
    elif condi == "rnc_pc":
        return "no-crowding reference and crowding probe"
    elif condi == "rnc_pnc":
        return "no-crowding reference and no-crowding probe"
    else:
        raise Exception(f"the condi {condi} does not exist.")


def __get_title4plot(row_number: int) -> str:
    if row_number == 12:
        return "all participants"
    elif row_number == 13:
        return "probe first group"
    elif row_number == 14:
        return "ref first group"
    elif row_number <= 5:
        return "pp%s probe first" % (row_number + 1)
    elif 6 <= row_number <= 11:
        return "pp%s ref first" % (row_number + 1)
    else:
        raise Exception(f"the select y values {row_number} was incorrect.")


def drawplot(result_df: pd.DataFrame, x_val: list, condi_list: list, row_number: int, alpha = 0.5, marker = "o"):
    """
    :param result_df: result df generated from groupby() with multi-level index
    :param x_val: list of x values
    :param alpha: 0 to 1.0
    :param marker: possible marker supported by plt
    :param rowofmean: index of the row of df use as y-values
    :param condi_list: experiment conditions: usually from one level of multi-level index
    :return: None
    """
    fig, ax = plt.subplots()
    for condi in condi_list:
        ax.plot(x_val, result_df[condi].values[row_number], alpha = alpha, marker = marker,
                label = __get_label4plot(condi))
    ax.legend()
    ax.set_xlabel("probe numerosity")
    ax.set_ylim([0, 1.1])
    ax.set_ylabel("proportion response reference display more numerous")
    ax.set_title(__get_title4plot(row_number))
    plt.savefig("f%s.png" % (row_number))
    plt.show()