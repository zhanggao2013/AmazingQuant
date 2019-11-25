# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/20
# @Author  : gao
# @File    : transfer_field.py
# @Project : AmazingQuant 
# ------------------------------

from mongoengine import document

from AmazingQuant.data_center.database_field.field_a_share_kline import Kline

def transfer_field(path):
    with open(path, encoding='UTF-8') as f:
        data = f.readlines()
        out_put = []

        for i in range(0, len(data), 3):
            # line_list = data.lower().split('\t')
            data_type = 'error error error error error error error error error '
            print(data)
            if 'number(' in data[i+2].lower():
                data_type = 'FloatField(required=True, null=True)'
            elif 'varchar' in data[i+2].lower():
                data_type = 'StringField(required=True, null=True)'
            out_put.append('# ' + data[i] + '\t' + data[i+1].lower().split()[0] + ' = ' + data_type + '\n')
        with open(path, 'r+') as file_to_read:
            file_to_read.writelines(out_put)


def get_collection_property_list(collection_name):
    return [i for i in list(set(collection_name.__dict__).difference(set(document.__dict__)))
            if i[0] != "_" and i not in ['DoesNotExist', 'objects', 'MultipleObjectsReturned', 'id', 'update_date']]


if __name__ == '__main__':
    field_path = '../config/field_a_share_ex_right_dividend.txt'
    # transfer_field(field_path)

    property_list = get_collection_property_list(Kline)
    for i in property_list:
        print(i)

