# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2020-12-30 21:58
IDE: PyCharm
Introduction:
"""
import math


def get_weighted_mean(distribution: list, weights: list) -> float:
    """
    :param distribution: list of int or float to calculate the weighted mean
    :param weights: weights list
    :return: the weighted mean of distribution list
    """
    numerator = sum([distribution[i] * weights[i] for i in range(len(distribution))])
    denominator = sum(weights)
    return round(numerator/denominator, 4)


def cal_eccentricity(posi: tuple) -> int:
    """This function returns the distance between the input position and (0,0)"""
    return math.sqrt(posi[0]**2+posi[1]**2)
