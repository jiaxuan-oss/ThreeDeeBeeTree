from __future__ import annotations
from threedeebeetree import Point
from ratio import Percentiles


def make_ordering(my_coordinate_list: list[Point]) -> list[Point]:


    if len(my_coordinate_list) <= 17:
        return my_coordinate_list
    else:
        return get_root(my_coordinate_list, [])


def get_root(coordinate_list, lst):
    if len(coordinate_list) <= 1:
        lst.append(coordinate_list[0])
        return lst

    root = get_ratio_item(coordinate_list)
    if root is not None:
        lst.append(root)
        coordinate_list.remove(root)    #O(n) complexity for removing
        return find_octant_child(root, coordinate_list, lst)


def find_octant_child(root, coordinate_list, lst):
    list_octants = separate_octants(root,coordinate_list, 0,[])
    for list_item in list_octants:
        if len(list_item) != 0:
            lst = get_root(list_item, lst)
    return lst


def separate_octants(root: Point, coordinate_list, indicator, list_oct):
    elems_0, elems_1 = [], []
    for item in coordinate_list:
        if item[indicator] >= root[indicator]:
            elems_0.append(item)
        else:
            elems_1.append(item)
    if indicator == 2:
        list_oct.append(elems_0)
        list_oct.append(elems_1)
        return list_oct

    list_oct = separate_octants(root, elems_0, indicator + 1, list_oct)
    list_oct = separate_octants(root, elems_1, indicator + 1, list_oct)
    return list_oct


def get_ratio_item(coordinate_list):
    if len(coordinate_list) <= 1:
        return coordinate_list[0]

    a = 12.5
    lst = []
    x_p, y_p, z_p = Percentiles(), Percentiles(), Percentiles()
    for item in coordinate_list:
        x_p.add_point(item[0])
        y_p.add_point(item[1])
        z_p.add_point(item[2])

    x_list, y_list, z_list = x_p.ratio(a, a), y_p.ratio(a, a), z_p.ratio(a, a)

    for item in coordinate_list:
        if item[0] in x_list and item[1] in y_list and item[2] in z_list:
            return item
    return coordinate_list[0]

