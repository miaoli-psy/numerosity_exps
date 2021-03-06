# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-01-15 17:26
IDE: PyCharm
Introduction:
"""
import statistics
from collections import Counter

from src.commons.process_number import get_weighted_mean
from src.commons.process_str import str_to_list
from src.point.polar_point import get_polar_coordinates


def get_angle_range(polar_posi_list, ini_start_angle = 0, ini_end_angle = 6):
    """
    :param polar_posi_list: a list of polar positions
    :param ini_start_angle: the first beam start edge, where to start
    :param ini_end_angle: : the first beam end edge
    :return: a list of range (place holder)
    """
    angle_size = ini_end_angle - ini_start_angle
    range_list = [(ini_start_angle, ini_end_angle)]

    start_angle = ini_start_angle
    for polar_posi in polar_posi_list:
        if polar_posi[0] > start_angle:
            start_angle = polar_posi[0]
            end_angle = start_angle + angle_size
            if end_angle < 360:
                range_list.append((start_angle, end_angle))
            if end_angle > 360:
                range_list.append((start_angle, end_angle - 360))
                break
    return range_list


def get_angle_range_no_overlap(input_overlap_range_list, start_n):
    """
    :param input_overlap_range_list: range that overlaps
    :param start_n: where the first range edge is
    :return: no-overlap range
    给定一个起始点start_n，逆时针扫。保证从逆时针方向离起始点最近
    的点优先扫到。
    """
    # 除了从最后一个开始扫的其它情况
    if not start_n == len(input_overlap_range_list) - 1:
        no_overlap_range = [input_overlap_range_list[start_n]]
        thrshld = input_overlap_range_list[start_n][1] # angle of start_n
        # 向后扫, 逆时针
        for range in input_overlap_range_list[start_n + 1:]:
            if range[0] > thrshld:
                no_overlap_range.append(range)
                thrshld = range[1]

        # 向前扫， 顺时针
        # Edge case: if it is start_n == 0, then we don't need to go 顺时针, because start_n_0 前面没有点了
        if start_n == 0:
            return no_overlap_range
        thrshld = input_overlap_range_list[start_n][0]
        for range in input_overlap_range_list[start_n - 1::-1]:
            if range[1] < thrshld:
                no_overlap_range.append(range)
                thrshld = range[0]
    # 从最后一个开始扫的情况
    else:
        no_overlap_range = [input_overlap_range_list[start_n]]
        thrshld = input_overlap_range_list[start_n][0]
        # 直接往回扫, 逆时针
        for range in input_overlap_range_list[start_n - 1::-1]:
            if range[1] < thrshld:
                no_overlap_range.append(range)
                thrshld = range[0]
    return no_overlap_range


def count_ndisc_in_range(polar_posi_list, range_start, range_end):
    """
    :param polar_posi_list: a list of polar positions
    :param range_start: angle of the starting edge
    :param range_end: angle of the ending edge
    :return: the number of discs within the region
    """
    if range_start < range_end:
        count = 0
        for polar_posi in polar_posi_list:
            if range_start <= polar_posi[0] < range_end:
                count += 1
        return count
    else:
        count = 0
        for polar_posi in polar_posi_list:
            if range_start <= polar_posi[0] < 360:
                count += 1
            elif 0 <= polar_posi[0] < range_end:
                count += 1
    return count


def counter2list(input_counter):
    return [input_counter[1], input_counter[2], input_counter[3], input_counter[4], input_counter[5], input_counter[6]]


def cal_alignment_value(beam_n, count_edge = 3):
    if count_edge == 4:
        return beam_n[3] + beam_n[4] + beam_n[5]
    elif count_edge == 3:
        return beam_n[2] + beam_n[3] + beam_n[4] + beam_n[5]


def get_avrg_alignment_v(input_posi_list, angle_size, count_edge = 3):
    """
    :param overlap_range: if False, no overlap beam regions
    :param input_posi_list: col from display dataframe, list like str
    :param angle_size: beam size that use to scan the whole displays
    :return: number of beams that contained 1-6 discs
    """
    # convert the str to list
    input_posi_list = str_to_list(input_posi_list)
    # get the polar coordinate of all positions
    polar_posis = get_polar_coordinates(input_posi_list)
    # the initial start edge
    ini_start_angle = polar_posis[0][0]
    # the end edge
    ini_end_angle = ini_start_angle + angle_size
    # get result ranges
    ranges_overlap = get_angle_range(polar_posis, ini_start_angle = ini_start_angle, ini_end_angle = ini_end_angle)
    align_v_list = list()
    for i in range(0, len(ranges_overlap)):
        ranges = get_angle_range_no_overlap(ranges_overlap, start_n = i)
        # for each region, calculate the number of discs
        ndisc_list = list()
        for beam in ranges:
            ndisc = count_ndisc_in_range(polar_posis, beam[0], beam[1])
            ndisc_list.append(ndisc)
        # count the occurrence
        count_beams = Counter(ndisc_list)
        count_beams_output = counter2list(count_beams)
        align_v = cal_alignment_value(count_beams_output, count_edge = count_edge)
        align_v_list.append(align_v)
    alignment_v = statistics.mean(align_v_list)
    return alignment_v


def get_beam_n(input_posi_list, angle_size):
    # convert the str to list
    input_posi_list = str_to_list(input_posi_list)
    # get the polar coordinate of all positions
    polar_posis = get_polar_coordinates(input_posi_list)
    # the initial start edge
    ini_start_angle = polar_posis[0][0]
    # the end edge
    ini_end_angle = ini_start_angle + angle_size
    # get result ranges
    ranges_overlap = get_angle_range(polar_posis, ini_start_angle = ini_start_angle, ini_end_angle = ini_end_angle)
    ndisc_list = list()
    for beams in ranges_overlap:
        n_disc = count_ndisc_in_range(polar_posis, beams[0], beams[1])
        ndisc_list.append(n_disc)
    count_beams = Counter(ndisc_list)
    count_beams_output = counter2list(count_beams)
    return count_beams_output


def get_one_beam_n_from_list(beam_n_list, n):
    return beam_n_list[n]


