# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/20
# @Author  : gao
# @File    : transfer_field.py
# @Project : AmazingQuant 
# ------------------------------


def transfer_field(path):
    with open(path) as f:
        data = f.readlines()
        out_put = []
        for i in range(0, len(data), 3):
            # line_list = data.lower().split('\t')
            data_type = 'error error error error error error error error error '
            if 'number(' in data[i+2].lower():
                data_type = 'FloatField(required=True, null=True)'
            elif 'varchar' in data[i+2].lower():
                data_type = 'StringField(required=True, null=True)'
            out_put.append('# ' + data[i] + '\t' + data[i+1].lower().split()[0] + ' = ' + data_type + '\n')
        with open(path, 'r+') as file_to_read:
            file_to_read.writelines(out_put)


def get_field_str_list(path):
    with open(path, encoding='UTF-8') as f:
        data = f.readlines()
        field_str_list = []
        for i in data:
            if 'StringField' in i:
                field_str_list.append(i.split('=')[0].split()[0])
        return field_str_list


if __name__ == '__main__':
    field_path = '../config/field_a_share_profit_notice.txt'
    # transfer_field(field_path)
    print(get_field_str_list(field_path))

