# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/12/13
# @Author  : gao
# @File    : get_index_member.py
# @Project : AmazingQuant 
# ------------------------------


def get_index_members(self, index):
    index_members = self.session.query(AINDEXMEMBERS).filter(AINDEXMEMBERS.S_INFO_WINDCODE == index)
    self.index_members_df = pd.read_sql(index_members.statement, self.engine)
    self.index_members_all = list(set(self.index_members_df["S_CON_WINDCODE"]))
    self.index_members_df = self.index_members_df.fillna(datetime.datetime.now().strftime("%Y%m%d"))


def get_index_member_in_date(self, members_date):
    index_members_in_date_df = self.index_members_df[
        (self.index_members_df.S_CON_INDATE <= members_date) & (self.index_members_df.S_CON_OUTDATE >= members_date)]
    return list(index_members_in_date_df["S_CON_WINDCODE"])