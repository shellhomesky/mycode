import re

import pandas as pd
import xlwings as xw


def xlookup(lookup_value, lookup_array, return_array, if_not_found: str = ''):
    match_value = return_array.loc[lookup_array == lookup_value]
    if match_value.empty:
        return f'"{lookup_value}" 没有找到！' if if_not_found == '' else if_not_found
    else:
        return match_value.tolist()[0]


path = './data/11.xlsx'
app = xw.App(visible=True, add_book=False)  # 启动Excel程序窗口，但不新建工作簿。
# visible是否可见。False表示后台运行。 add_book 是否新建一个工作簿
# wb=app.books.add()  #在当前app下创建工作簿
# wb=xw.Book()  #创建一个新的App，并在新App中新建一个Book
# wb.display_alerts=False #是否开启提示，如保存提示等。
# wb.screen_updating=True #是否更新显示变动内容，若设为False则看不到文档的打开或变化
# books = xw.books #当前活动App的工作簿集合
# books = app.books #指定的App的所有工作簿的集合，返回一个列表。
# wb.save([path])  #path省略，则保存；不省略，则可另存为。

wb = app.books.open(path)  # path为相对或绝对路径
# wb=xw.Book(path)
# wb.activate(steal_focus=False)
# wb.activate(steal_focus=True) #如果steal_focus=True, 则把窗口显示到最上层，并且把焦点从Python切换到Excel
sh1 = wb.sheets['Table 1']  # 根据工作表名称选中工作表
sh2 = wb.sheets[1]  # 根据工作表序号选中工作表
sh3 = wb.sheets[2]
# sh1 = wb.sheets.active  # 引用当前工作簿活动工作表
# sh1 = xw.sheets.active  # 引用当前app活动工作表
# worksheet1 = xw.sheets  # 返回当前活动工作簿的所有工作表
# worksheet1 = wb.sheets  # 返回指定工作簿中所有工作表
# sh2 = wb.sheets.add('new sheet', after=sh1)
rng = sh2.range('a1').expand('table')
nrowsd = rng.rows.count
ncolsd = rng.columns.count
a = sh2[0, :ncolsd - 1].value
sh3[0, :ncolsd - 1].value = a
nrows = sh1.used_range.last_cell.row
ncolumns = sh1.used_range.last_cell.column
ls_data = []
is_key = []
for i in range(nrows):
    if bool(re.search(r'\d+[.]', sh1[i, 0].value)) if sh1[i, 0].value else False:
        data = re.findall(r'\d+', sh1[i, 0].value)[0]
        ls_data.append(data)
        is_key.append(i)
for n, row in enumerate(is_key):
    if row == is_key[-1]:
        d = sh1[row:nrows, :ncolumns].value
    else:
        d = sh1[row:is_key[n + 1], :ncolumns].value
    d = pd.DataFrame(d)
    for j in range(ncolsd):
        find = ''
        if j == 0:
            find = re.findall(r'\d+', d[0][0])[0]
        else:
            find = xlookup(sh2[0, j].value, d[sh2[1, j].value - 1], d[sh2[2, j].value - 1])
        sh3[n + 2, j].value = find
        print(j)
    print(n)
app.kill()  # 终止进程，强制退出。
app.quit()  # 在不保存的情况下，退出excel程序。
