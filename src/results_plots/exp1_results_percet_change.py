import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statannot import add_stat_annotation
from src.commons.process_dataframe import rename_df_col, insert_new_col, insert_new_col_from_two_cols

if __name__ == '__main__':
    save_plot = False
    # read data
    PATH = "../../data//exp1_rerun_data/"
    DATA = "cleanedTotalData_fullinfo_v3.xlsx"
    data = pd.read_excel(PATH + DATA)
    # process the cols
    rename_df_col(data, "Unnamed: 0", "n")

    # average percent_change for each condition per participant
    data_1 = data.groupby(["participant_N", "winsize", "crowdingcons"])["percent_change"].agg(["mean", "std"]).reset_index(level = ["participant_N", "winsize", "crowdingcons"])
    rename_df_col(df = data_1, old_col_name = "mean", new_col_name = "mean_percent_change")

    x = "winsize"
    y = "mean_percent_change"
    data = data_1
    hue = "crowdingcons"

    fig, ax = plt.subplots(figsize = (6, 4.5))
    ax = sns.barplot(x = x,
                     y = y,
                     data = data,
                     hue = hue,
                     capsize = .05,
                     palette = ["royalblue", "orangered"],
                     alpha = 0.5,
                     ci = 68)

    ax = sns.swarmplot(x = x,
                       y = y,
                       data = data,
                       hue = hue,
                       palette = ["royalblue", "orangered"],
                       dodge = True,
                       alpha = 0.65)

    box_pairs = [((0.4, 0), (0.4, 1)),
                 ((0.5, 0), (0.5, 1)),
                 ((0.6, 0), (0.6, 1)),
                 ((0.7, 0), (0.7, 1)),
                 ((0.3, 0), (0.6, 1)),
                 ((0.3, 0), (0.7, 1))]
    text_annot_custom = ["*", "*", "*", "*", "*", "*"]

    # add asterisk and pairs
    add_stat_annotation(ax, data = data, x = x, y = y, hue = hue, box_pairs = box_pairs,
                        text_annot_custom = text_annot_custom,
                        perform_stat_test = False,
                        pvalues = [0, 0, 0, 0, 0, 0],
                        loc = 'inside', verbose = 0)

    # customize the plot
    xlabel = "Numerosity"
    ylabel = "Percent Changes"
    ax.set_xlabel(xlabel, fontsize = 15, labelpad = 12)
    ax.set_ylabel(ylabel, fontsize = 15)
    ax.set_ylim([-0.5, 0.5])
    ax.set_xticklabels(["21-25", "31-35", "41-45", "49-53", "54-58"])
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    # customize legend
    handles, labels = ax.get_legend_handles_labels()
    labels = ["tangential", "radial"]
    ax.legend(handles[2:], labels, loc = "lower center", ncol = 2, fontsize = 12)
    # hide borders
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    # add liney = 0
    ax.axhline(y = 0, color = "k", linewidth = 0.5)
    plt.show()
    if save_plot:
        fig.savefig("exp1_results_plot.svg", bbox_inches = 'tight')