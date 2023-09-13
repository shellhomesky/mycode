import xlrd, xlwt, time
from xlutils.copy import copy
from re import sub


def read_excel(sheet, col_start, col_end):
    # 通过sheet的索引去获得sheet对象
    # sheet =xls.sheet_by_index(0)
    # 定义一个空的列表，用于读取后存入数据
    datalist = []
    for row in range(1, sheet.nrows):  # 从第2行开始循环去读
        # 获取整行的内容
        # print(sheet.row_values(rows))
        # 定义一个暂存列表
        temptlist = []
        for col in range(col_start - 1, col_end):  # 从第1列循环去读取列，读到倒数第3列，倒数2列，分别是用于写入测试时间、测试结果
            temptlist.append(sheet.cell_value(row, col))  # 否则 获取单元格内容
        datalist.append(temptlist)  # 把每一次循环读完一行的所有列之后，将数据追加到datalist列表中
    return datalist


def write_excel(excel_path, sheet_name, rows, cols, value):
    # 获取当前的系统时间，并格式化
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 打开excel, 保留原始格式
    xls = xlrd.open_workbook(excel_path, formatting_info=True)
    # 复制excel
    # 需要先安装xlutils工具包`pip install xlutils`，才能导入copy模块，具体导入方式为`from xlutils.copy import copy`
    xls_copy = copy(xls)
    # 通过sheet名称获取sheet对象
    sheet = xls_copy.get_sheet(sheet_name)
    if value == "fail":
        sheet.write(rows, cols, value, style=xlwt.easyxf('pattern: pattern solid, fore_colour %s;' % "red"))
    elif value == "ignore":
        sheet.write(rows, cols, value, style=xlwt.easyxf('pattern: pattern solid, fore_colour %s;' % "blue_gray"))
    else:
        sheet.write(rows, cols, value)
    # 设置倒数第二列的宽度和赋值为当前时间
    sheet.col(cols - 1).width = 5000
    sheet.write(rows, cols - 1, current_time)
    # 保存excel
    xls_copy.save(excel_path)


def xlwtwrite(worksheet, row, col, value):
    # 创建一个workbook对象，就相当于创建了一个Excel文件
    workbook = xlwt.Workbook(encoding='utf-8', style_compression=0)  # encoding:设置编码，可写中文；style_compression:是否压缩，不常用
    # 创建一个sheet对象，相当于创建一个sheet页
    worksheet = workbook.add_sheet('这是sheet1', cell_overwrite_ok=True)  # cell_overwrite_ok:是否可以覆盖单元格，默认为False
    # 向sheet页中添加数据：worksheet.write(行,列,值)
    worksheet.write(row, col, value)
    # 将以上内容保存到指定的文件中
    workbook.save('测试文件.xls')


if __name__ == "__main__":
    # 首先打开excel表，formatting_info=True 代表保留excel原来的格式
    xls = xlrd.open_workbook(r"F:\风险应对\2023\苏州银行\数据\content.xls", formatting_info=True)
    sheet = xls.sheet_by_name("2021")
    # 打开目录excel表
    xlspz = xlrd.open_workbook(r"F:\风险应对\2023\苏州银行\数据\19-21日记账凭证.xls")
    sheetpz = xlspz.sheet_by_name("第一批")
    # 查询匹配列
    datalist = read_excel(sheet, 1, 1)
    # 创建一个workbook对象，就相当于创建了一个Excel文件
    workbook = xlwt.Workbook(encoding='utf-8', style_compression=0)  # encoding:设置编码，可写中文；style_compression:是否压缩，不常用
    # 创建一个sheet对象，相当于创建一个sheet页
    worksheet = workbook.add_sheet('这是sheet1', cell_overwrite_ok=True)

    row_w = 0
    col = 0
    for id in range(0, len(datalist)):
        page_c = 0
        page_e = 0
        row_s = 0
        while row_s < sheetpz.nrows:
            if sheetpz.cell_value(row_s, 0) == '苏州银行 记账凭证':
                valuepz = sheetpz.cell_value(row_s + 3, 5)[10:29]
                if datalist[id][0] == valuepz:
                    worksheet.write(row_w, 0, valuepz)
                    ywxcf_hj = 0
                    jxsj_hj = 0
                    xxsj_hj = 0
                    for row5 in range(row_s + 6, row_s + 12):
                        value5 = sheetpz.cell_value(row5, 5)
                        if value5[9:14] == "业务宣传费":
                            ywxcf_hj = ywxcf_hj + float(sub(r'[^\d.]', '', str(sheetpz.cell_value(row5, 10))))
                        if value5[9:13] == "进项税额":
                            jxsj_hj = jxsj_hj + float(sub(r'[^\d.]', '', str(sheetpz.cell_value(row5, 10))))
                        if value5[9:13] == "销项税额":
                            xxsj_hj = xxsj_hj + float(sub(r'[^\d.]', '', str(sheetpz.cell_value(row5, 13))))
                    worksheet.write(row_w, 1, ywxcf_hj)
                    worksheet.write(row_w, 2, jxsj_hj)
                    worksheet.write(row_w, 3, xxsj_hj)
                    row_s = row5 + 4
                    row_w += 1
                else:
                    row_s = row_s + 13

            else:
                row_s = row_s + 1
    workbook.save(r"F:\风险应对\2023\苏州银行\数据\contentout1.xls")
