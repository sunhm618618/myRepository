#!/usr/bin/python
# -*- coding: UTF-8 -*-


from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import json
# import datetime


class ServerHTTP(BaseHTTPRequestHandler):
    def send_res(self, response, status_code):
        # 发送一个响应头并记录已接收的请求
        self.send_response(status_code)
        self.send_header("Content-type", "text/html")
        # 编写一个指定的HTTP头到输出流
        self.send_header("test", "This is test!")
        self.end_headers()
        # print("response is：", response)
        # 将响应内容的数据结构转化为json格式
        content = json.dumps(response,  ensure_ascii=False)
        # 包含写到客户端响应的输出流
        self.wfile.write(bytes(content, 'UTF-8'))

    # BaseHpptServer没有实现do_GET方法，需要自己重写
    def do_GET(self):
        # begin = datetime.datetime.now()

        # 将url分为6个部分，返回一个包含6个字符串项目的元组：协议、位置、路径、参数、查询、片段
        url_path = parse.urlparse(self.path)
        # print(url_path)
        req_path = url_path.path
        # 获取参数，返回一个字典s
        param_dict = parse.parse_qs(url_path.query)
        response = {}
        if req_path == '/shopee/test':
            if len(param_dict) != 2 or 'a' not in param_dict or 'b' not in param_dict:
                response['error_code'] = 21
                response['error_message'] = 'empty or wrong params'
                response['reference'] = 'Please ensure  params are only the int a and string b'
                self.send_res(response, 404)
                # return
            else:
                re_a = param_dict.get('a')
                re_b = param_dict.get('b')
                # a=eval(re_a[0])
                a = re_a[0]
                b = re_b[0]
                # 判断a是否由数字组成
                a_type_num = a.isdigit()
                # 判断b是否由字母组成
                b_type_str = b.isalpha()

                # # 只含有汉字、数字、字母、下划线，下划线位置不限
                # # b_object=re.search('^[a-zA-Z0-9_\u4e00-\u9fa5]+$', b)
                # # 只能输入由26个英文字母组成的字符串,包括大写和小写
                # b_object = re.search('^[A-Za-z]+$', b)
                # b_type=(None != b_object)

                if a_type_num is True and b_type_str is True:
                    response['error_code'] = 0
                    response['error_message'] = 'success'
                    response['reference'] = 'No.' + a + " is " + b
                    self.send_res(response, 200)
                else:
                    if a_type_num is not True:
                        response['error_code'] = 21
                        response['error_message'] = 'Please ensure that the type of a is int!'
                        self.send_res(response, 200)
                    elif b_type_str is not True:
                        response['error_code'] = 21
                        response['error_message'] = 'Please ensure that the type of b is string!'
                        self.send_res(response, 200)

        else:
            response['error_code'] = 11
            response['error_message'] = 'system error'
            self.send_res(response, 404)
        # end = datetime.datetime.now()
        # print("time is :", (end-begin).microseconds)


if __name__ == "__main__":
    http_server = HTTPServer(('', int(8080)), ServerHTTP)
    # 设置一直监听并接收请求，其中，IP为给localhost设定的访问地址
    http_server.serve_forever()


