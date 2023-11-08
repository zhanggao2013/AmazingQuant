# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/22
# @Author  : gao
# @File    : get_calender.py
# @Project : AmazingQuant 
# ------------------------------

from AmazingQuant.constant import LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.utils.get_data import get_local_data


class GetCalendar(object):
    def __init__(self):
        pass

    def get_calendar(self, market):
        folder_name = LocalDataFolderName.CALENDAR.value
        path = LocalDataPath.path + folder_name + '/'
        data_name = 'calendar_' + market + '.h5'
        data = get_local_data(path, data_name)
        return list(data[0])


if __name__ == '__main__':
    calendar_obj = GetCalendar()
    result = calendar_obj.get_calendar('SH')
    print(result)
