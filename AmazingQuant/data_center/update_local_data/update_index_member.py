# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/13
# @Author  : gao
# @File    : update_index_member.py
# @Project : AmazingQuant 
# ------------------------------

from datetime import datetime

import pandas as pd
from mongoengine import connection

from AmazingQuant.constant import DatabaseName
from AmazingQuant.config.database_info import MongodbConfig
from AmazingQuant.data_center.database_field.field_a_share_index_members import AShareIndexMembers


class GetIndexMember(object):
    def __init__(self):
        self.index_members_df = pd.DataFrame.empty
        self.index_members_all = []

    def get_index_members(self, index_code):
        database = DatabaseName.STOCK_BASE_DATA.value
        connection.connect(db=database, host=MongodbConfig.host, port=MongodbConfig.port,
                           password=MongodbConfig.password, username=MongodbConfig.username, retryWrites=False)
        index_members_data = AShareIndexMembers.objects(index_code=index_code).as_pymongo()
        connection.disconnect()

        field_list = ['index_code', 'security_code', 'in_date', 'out_date']
        self.index_members_df = pd.DataFrame(list(index_members_data)).reindex(columns=field_list)
        self.index_members_all = list(set(self.index_members_df["security_code"]))
        self.index_members_df = self.index_members_df.fillna(datetime.now())
        return self.index_members_df, self.index_members_all

    def get_index_member_in_date(self, members_date=datetime.now()):
        """
        取指定日期的指数成分股
        :param members_date:
        :return:
        """
        index_members_in_date_df = self.index_members_df[
            (self.index_members_df.in_date <= members_date) & (self.index_members_df.out_date >= members_date)]
        return list(index_members_in_date_df["security_code"])


if __name__ == '__main__':
    index_member_obj = GetIndexMember()
    index_members_df, index_members_all = index_member_obj.get_index_members('000002.SH')
    index_member_in_date = index_member_obj.get_index_member_in_date()


