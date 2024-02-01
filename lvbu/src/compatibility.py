import pandas as pd

# license_info = pd.read_csv('./data/许可证信息-v1.csv', encoding='utf-8', index_col='identifier')
# compatibility_list_source = pd.read_csv('./data/兼容性_使用源代码.csv', encoding = 'utf-8', index_col = 'License')
# compatibility_list_binary = pd.read_csv('./data/兼容性_使用库.csv', encoding = 'utf-8', index_col = 'License')

license_info = pd.read_excel('./data/许可证信息-v2.xlsx', index_col='identifier')
compatibility_list_source = pd.read_excel('./data/相容性列表（使用源代码）.xlsx', index_col = 'License')
compatibility_list_binary = pd.read_excel('./data/相容性列表（使用库）.xlsx', index_col = 'License')

def check_process(license_start, license_end, usage):
    print(license_start, license_end, usage)
    if usage == 'source code':
        result = has_conflict_source(license_start, license_end)
        if result[0] is not True:
            if check_compatibility(license_start, license_end) is True:
                s = ''
                if result[1] != '机器标注，非最终结果':
                    if compatibility_list_source.loc[license_start, license_end] != '相容':
                        s = compatibility_list_source.loc[license_start, license_end].split('，')[1]
                        s = '，' + s
                return {'license_start':license_start, 'license_end':license_end, 'result': '兼容' + s, 'remarks': result[1], \
                        'result_explain': '您的项目使用的许可证与您将要并入的许可证相容且更为严格'}
            else:
                return {'license_start':license_start, 'license_end':license_end, 'result': '相容，但不兼容', 'remarks': result[1], \
                'result_explain': '您的项目使用的许可证与您将要并入的许可证相容，但后者包含了前者并未要求的义务'}
        else:
            return {'license_start':license_start, 'license_end':license_end, 'result': '冲突', 'remarks': result[1],  \
                    'result_explain': '您的项目使用的许可证与您将要并入的许可证的义务或限制无法同时满足'}
    if usage == 'library':
        result = has_conflict_binary(license_start, license_end)
        if result[0] is not True:
            if check_compatibility(license_start, license_end) is True:
                s = ''
                if result[1] != '机器标注，非最终结果':
                    if compatibility_list_binary.loc[license_start, license_end] != '相容':
                        s = compatibility_list_binary.loc[license_start, license_end].split('，')[1]
                        s = '，' + s
                return {'license_start':license_start, 'license_end':license_end, 'result': '兼容' + s, 'remarks': result[1],\
                        'result_explain': '您的项目使用的许可证与您将要并入的许可证相容且更为严格'}
            else:
                return {'license_start':license_start, 'license_end':license_end, 'result': '相容，但不兼容', 'remarks': result[1],\
                        'result_explain': '您的项目使用的许可证与您将要并入的许可证相容，但后者包含了前者并未要求的义务'}
        else:
            return {'license_start':license_start, 'license_end':license_end, 'result': '冲突', 'remarks': result[1], \
                    'result_explain': '您的项目使用的许可证与您将要并入的许可证的义务或限制无法同时满足'}


def has_conflict_source(license_start, license_end):
    # compatibility_list = pd.read_csv('../data/兼容性_合并修改.csv', encoding = 'utf-8', index_col = 'License')
    index = list(compatibility_list_source.index.copy())
    columns = list(compatibility_list_source.columns.copy())
    if license_start in index and license_end in columns:
        if compatibility_list_source.loc[license_start, license_end] == '冲突':
            return (True, '人工分析')
        else:
            return (False, '人工分析')
    else:
        # license_info = pd.read_csv('../data/许可证信息-v1.csv', encoding='utf-8', index_col='identifier')
        sl_cate = license_info.loc[license_start, 'category']
        el_cate = license_info.loc[license_end, 'category']
        if (sl_cate == 'Copyleft' or sl_cate == 'Weak copyleft') and \
            (el_cate == 'Copyleft' or el_cate == 'Weak copyleft'):
            return (True, '机器标注，非最终结果')
        else:
            return (False, '机器标注，非最终结果')

def has_conflict_binary(license_start, license_end):
    # compatibility_list = pd.read_csv('../data/兼容性_使用库.csv', encoding = 'utf-8', index_col = 'License')
    # print(conflict_list.loc[license_start, license_end])
    index = list(compatibility_list_binary.index.copy())
    columns = list(compatibility_list_binary.columns.copy())
    if license_start in index and license_end in columns:
        if compatibility_list_binary.loc[license_start,license_end] == '冲突':
            return (True, '人工分析')
        else:
            return (False, '人工分析')
    else:
        # license_info = pd.read_csv('../data/许可证信息-v1.csv', encoding='utf-8', index_col='identifier')
        sl_cate = license_info.loc[license_start, 'category']
        el_cate = license_info.loc[license_end, 'category']
        if (sl_cate == 'Copyleft') and \
                (el_cate == 'Copyleft' or el_cate == 'Weak copyleft'):
            return (True, '机器标注，非最终结果')
        else:
            return (False, '机器标注，非最终结果')


def check_compatibility(license_start, license_end):
    # license_info = pd.read_csv('../data/许可证信息-v1.csv', encoding='utf-8', index_col='identifier')
    obligations = ['disclose source', 'license and copyright notice', 'Network use is distribution', 'same license', 'state changes']
    limitations = []

    # sl:start license   el:end license
    sl_info = {'obligation':[], 'limitation':[]}
    el_info = {'obligation': [], 'limitation': []}
    for obligation in obligations:
        if license_info.loc[license_start, obligation] != 'not mentioned':
            sl_info['obligation'].append(obligation)
        if license_info.loc[license_end, obligation] != 'not mentioned':
            el_info['obligation'].append(obligation)

    for obligation in sl_info['obligation']:
        if obligation not in el_info['obligation']:
            return False

    return True


if __name__ == '__main__':
    print(check_process('GPL-2.0-only', 'Apache-2.0', 'source code'))
