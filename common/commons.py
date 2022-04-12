# coding:utf-8

import os, time, json

base_pa = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
base_path = base_pa.replace('\\', '/')
log_path = base_path + '/'  + 'logs'
report_html = base_path + '/' + 'report'
read_xlrd = base_path + '/' + 'data'


class Commom():

    def mkdir_path(self, base_page):
        local_time1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        year = time.strftime('%Y', time.localtime(time.time()))
        month = time.strftime('%m', time.localtime(time.time()))
        day = time.strftime('%d', time.localtime(time.time()))
        base_page = base_page
        fileyear = base_page + '/' + year
        filemonth = fileyear + '/' + month
        fileday = filemonth + '/' + day
        if not os.path.exists(fileyear):
            os.mkdir(fileyear)
            os.mkdir(filemonth)
            os.mkdir(fileday)
        else:
            if not os.path.exists(filemonth):
                os.mkdir(filemonth)
                os.mkdir(fileday)
            else:
                if not os.path.exists(fileday):
                    os.mkdir(fileday)
        file_years = fileyear.replace('\\', '/')
        file_days = fileday.replace('\\', '/')
        file_months = filemonth.replace('\\', '/')  # 将路径中'\'转译为‘/’
        return file_days, file_months, file_years

    # 封装日志方法
    def get_logs(self, path=log_path):
        import logging, time
        logs = logging.getLogger()
        logs.setLevel(logging.DEBUG)
        path1 = self.mkdir_path(path)
        path = path1[0] + '/' + time.strftime('%Y-%m-%d-%H-%M-%S') + '.log'
        write_file = logging.FileHandler(path, 'a+', encoding='utf-8')
        write_file.setLevel(logging.DEBUG)
        set_logs = logging.Formatter('%(asctime)s -- %(funcName)s - %(levelname)s - %(message)s')
        write_file.setFormatter(set_logs)
        pycharm_text = logging.StreamHandler()
        pycharm_text.setFormatter(set_logs)
        if not logs.handlers:
            logs.addHandler(write_file)
            logs.addHandler(pycharm_text)
        return logs

    # 封装读取excel表格方法，将其转换为字典格式，方便json格式读取接口数据
    def ReadExcelTypeDict(self, file_name, path=read_xlrd):
        path = path + '/' + file_name
        import xlrd
        work_book = xlrd.open_workbook(path)  # 打开excel表格
        sheets = work_book.sheet_names()  # 读取所有的sheet页
        DataList = []
        for sheet in sheets:
            sheets = work_book.sheet_by_name(sheet)
            nrows = sheets.nrows
            for i in range(0, nrows):
                values = sheets.row_values(i)
                DataList.append(values)
        title_list = DataList[0]
        cotent_list = DataList[1:]
        new_list = []
        for content in cotent_list:
            dic = {}
            for i in range(len(content)):
                dic[title_list[i]] = content[i]
            new_list.append(dic)
        return new_list

    def ReadJson(self, filename, path=read_xlrd):
        path = path + '/' + filename
        with open(path, encoding='utf-8') as f:
            jlist = []
            while True:
                line = f.readline()
                if not line:
                    break
                jlist.append(line)
            # js = json.dumps(jlist)
        # rint(jlist)
        return jlist

    # 封装生成Html报告方法
    def GETHtmlResult(self, suite, title, path=report_html):
        import HTMLTestReportCN
        path = self.mkdir_path(path)
        fileday = (path[0])
        path = fileday + '/' + time.strftime('%Y-%m-%d-%H-%M-%S') + '.html'
        # print(path)
        with open(path, 'wb+') as f:
            run = HTMLTestReportCN.HTMLTestRunner(stream=f, description='用户相关接口测试报告', tester='mingzhu', title=title)
            run.run(suite)

