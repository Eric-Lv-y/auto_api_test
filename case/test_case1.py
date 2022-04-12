#coding:utf-8
import  unittest
import  ddt
import time
import  common.commons as common
import common.send_emails as send_mail
from base.Base_Page import  Base
import json

r = common.Commom().ReadExcelTypeDict('test.xls')#读取具体的EXCEL表格
d = common.Commom().ReadExcelTypeDict('data_test.xls')
j = common.Commom().ReadJson('test_login.json')
# print('json内容:',j)
@ddt.ddt        #导入ddt模块
class Testlogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:#setupclass类方法，全部开始用例前执行一次
        cls.logs = common.Commom().get_logs() # 导入日志方法
        cls.logs.debug('自动化测试用例开始！！！')

    @classmethod
    def tearDownClass(cls) -> None:
        cls.logs.debug('自动化测试用例结束！！！')

    def setUp(self) -> None:
        self.start_time = time.time()
        self.logs.debug('开始执行本条用例')

    def tearDown(self) -> None:
        end_time = time.time()
        self.logs.debug('本条用例执行完毕,用例执行时间：'+str(self.start_time-end_time))

    @ddt.data(*r)
    # @unittest.skip
    # @unittest.skipIf(1==1)
    # 引入ddt模块，读取拿到的数据
    def test_status(self,pars):  #用例方法名必须以test开头，pars参数为接受的表数据值
        dic = json.loads(pars['body参数值'])  #将Excel数据中心的参数值转变为json格式
        url = pars['接口地址']      #拿到请求url
        test_name = pars['用例标题']
        header = json.loads(pars['请求头'])
        yuqi = pars['预期结果']
        fs = pars['请求方式']
        self.logs = common.Commom().get_logs()
        #self.logs.debug('开始执行本条用例：'+test_name)
        result = Base().requests_type(method= fs, url = url,headers = header, data= dic)
        self.logs.debug('result:' + result.text)
        # self.assertEqual(len(result.headers),17,msg='响应头长度不符')
        self.assertEqual(result.status_code,yuqi,msg='响应状态码错误！'+str(yuqi)+'!='+str(result.status_code))

    # @ddt.data(*d)
    @unittest.skip
    def test_data(self,pars):
        dic = json.loads(pars["body参数值"])
        url = pars["接口地址"]
        test_name = pars['用例标题']
        header = json.loads(pars['请求头'])
        yuqi = str(pars['预期结果'])
        fs = pars['请求方式']
        self.logs = common.Commom().get_logs()
        self.logs.debug('开始执行本条用例：' + test_name)
        result = Base().requests_type(method=fs, url=url, headers=header, data=dic)
        self.logs.debug('result:' + result.text)
        result1 = result.json()
        #self.logs.debug(result1)
        self.assertEqual(result1['data']['openId'],yuqi,msg='openID比对错误！')

    # @ddt.data(*j)
    @unittest.skip
    def test_json(self,par):
        par = json.loads(par)
        header = par["headers"]
        url = par["url"]
        body = par["body"]
        fs = par["fs"]
        expect = par["expect"]
        #print(url,body,header)
        self.logs = common.Commom().get_logs()
        result = Base().requests_type(url=url,method = fs,data= body,headers=header)
        self.logs.debug('result:'+result.text)
        result1 = result.json()
        t = result.elapsed     # 响应时间
        self.assertLess (t,1,msg='响应时间大于1秒')    # lessequal小于等于则返回TRUE
        self.assertGreater(t,1,msg='响应时间小于1秒')  # greaterequal大于等于则返回TRUE
        self.assertEqual(result1['data']['openId'],expect,msg='openId比对错误！')


if __name__ == '__main__':
    load = unittest.TestLoader().loadTestsFromTestCase(Testlogin)   #使用loader加载方式，来寻找所有以test开头的用例
    suite = unittest.TestSuite([load,])     #执行测试用例
    common.Commom().GETHtmlResult(suite,'登录测试用例')   #生成测试报告
    send_mail.send_mail() #发送测试报告到邮箱

