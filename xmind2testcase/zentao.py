#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import csv
import logging
import os
from xmind2testcase.utils import get_xmind_testcase_list, get_absolute_path

"""
Convert XMind fie to Zentao testcase csv file 

Zentao official document about import CSV testcase file: https://www.zentao.net/book/zentaopmshelp/243.mhtml 
"""


def xmind_to_zentao_csv_file(xmind_file):
    """Convert XMind file to a zentao csv file"""
    xmind_file = get_absolute_path(xmind_file)
    logging.info('Start converting XMind file(%s) to zentao file...', xmind_file)
    testcases = get_xmind_testcase_list(xmind_file)

    # 调整用例标题->用例名称
    # 修改前
    # fileheader = ["所属模块", "用例标题", "前置条件", "步骤", "预期", "关键词", "优先级", "用例类型", "适用阶段"]
    # 修改后
    fileheader = ["所属模块", "用例名称", "前置条件", "步骤", "预期", "关键词", "优先级", "用例类型", "适用阶段"]
    zentao_testcase_rows = [fileheader]
    for testcase in testcases:
        row = gen_a_testcase_row(testcase)
        zentao_testcase_rows.append(row)

    zentao_file = xmind_file[:-6] + '.csv'
    if os.path.exists(zentao_file):
        os.remove(zentao_file)
        # logging.info('The zentao csv file already exists, return it directly: %s', zentao_file)
        # return zentao_file

    # 修改前
    # with open(zentao_file, 'w', encoding='gbk') as f:
    # 修改后
    with open(zentao_file, 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(zentao_testcase_rows)
        logging.info('Convert XMind file(%s) to a zentao csv file(%s) successfully!', xmind_file, zentao_file)

    return zentao_file


def gen_a_testcase_row(testcase_dict):
    case_module = gen_case_module(testcase_dict['suite'])
    case_title = testcase_dict['name']
    case_precontion = testcase_dict['preconditions']
    case_step, case_expected_result = gen_case_step_and_expected_result(testcase_dict['steps'])
    # 此处可填写默认关键词，当前为空
    # case_keyword = ''
    # 修改：使用从XMind文件中读取的关键词，如果没有则使用模块名
    case_keyword = testcase_dict.get('keywords', '') or case_module
    case_priority = gen_case_priority(testcase_dict['importance'])
    case_type = gen_case_type(testcase_dict['execution_type'])
    # 调整默认测试阶段
    # 修改前
    # case_apply_phase = '迭代测试'
    # 修改后
    case_apply_phase = '功能测试阶段'
    row = [case_module, case_title, case_precontion, case_step, case_expected_result, case_keyword, case_priority, case_type, case_apply_phase]
    return row


def gen_case_module(module_name):
    if module_name:
        module_name = module_name.replace('（', '(')
        module_name = module_name.replace('）', ')')
    else:
        module_name = '/'
    return module_name


def gen_case_step_and_expected_result(steps):
    case_step = ''
    case_expected_result = ''
    # 修改后，把+ '. ' + 后的空格去掉  + '.' +
    for step_dict in steps:
        case_step += str(step_dict['step_number']) + '.' + step_dict['actions'].replace('\n', '').strip() + '\n'
        case_expected_result += str(step_dict['step_number']) + '.' + \
                                step_dict['expectedresults'].replace('\n', '').strip() + '\n' \
            if step_dict.get('expectedresults', '') else ''
    # 添加，去除每个单元格里最后一个换行符
    case_step = case_step.rstrip('\n')
    case_expected_result = case_expected_result.rstrip('\n')
    return case_step, case_expected_result


def gen_case_priority(priority):
    # 修改前
    # mapping = {1: '高', 2: '中', 3: '低'}
    # 修改后，修改用例等级
    mapping = {1: '1', 2: '2', 3: '3', 4: '4'}
    if priority in mapping.keys():
        return mapping[priority]
    else:
        # 修改前
        #return '中'
        #修改后
        return '2'


def gen_case_type(case_type):
    # 修改前
    # mapping = {1: '手动', 2: '自动'}
    # 修改后
    mapping = {1: '功能测试', 2: '性能测试',3:'配置相关',4:'安装部署',5:'安全相关',6:'接口测试',7:'其他'}
    if case_type in mapping.keys():
        return mapping[case_type]
    else:
        # 修改后
        return '功能测试'


if __name__ == '__main__':
    xmind_file = '../docs/zentao_testcase_template.xmind'
    zentao_csv_file = xmind_to_zentao_csv_file(xmind_file)
    print('Conver the xmind file to a zentao csv file succssfully: %s', zentao_csv_file)