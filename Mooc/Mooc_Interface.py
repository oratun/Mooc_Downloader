"""
    Mooc 人机交互的接口函数
"""

import os
import re

if __package__ is None:
    import sys

    sys.path.append('.\\')
    sys.path.append("..\\")
from Mooc.Mooc_Config import *
from Mooc.Mooc_Request import *
from Mooc.Mooc_Download import *
from Mooc.Icourse163.Icourse163_Mooc import *
from Mooc.Icourses.Icourse_Cuoc import *
from Mooc.Icourses.Icourse_Mooc import *

__all__ = [
    "mooc_interface"
]

# 课程名对应的Mooc类
courses_mooc = {
    "icourse163_mooc": Icourse163_Mooc,
    "icourse_cuoc": Icourse_Cuoc,
    "icourse_mooc": Icourse_Mooc
}


def mooc_interface():
    try:
        while True:
            os.system("cls")
            print("\t{:^90}".format("下载路径: " + PATH))
            urlstr = 'https://www.icourse163.org/learn/ZJU-93001?tid=1207006212#/learn/content'
            while not urlstr:
                try:
                    urlstr = input('\n输入一个视频课程网址(q退出): ')
                except KeyboardInterrupt:
                    print()
            if urlstr == 'q':
                break
            mooc = match_mooc(urlstr)
            if not mooc:
                input("视频课程链接不合法，请回车继续...")
                continue
            if not mooc.set_mode():
                continue
            print("正在连接资源......")
            try:
                mooc.prepare(urlstr)
            except RequestFailed:
                print("网路请求异常！")
                input("请按回车键返回主界面...")
                continue
            while True:
                try:
                    isdownload = mooc.download()
                    if isdownload:
                        print('"{}" 下载完毕!'.format(mooc.title))
                        print("下载路径: {}".format(mooc.rootDir))
                        os.startfile(mooc.rootDir)
                    else:
                        print('"{}" 还未开课！'.format(mooc.title))
                    input("请按回车键返回主界面...")
                    break
                except (RequestFailed, DownloadFailed) as err:
                    # raise
                    if isinstance(err, RequestFailed):
                        print("网路请求异常！")
                    else:
                        print("文件下载异常！")
                    if inquire():
                        continue
                    else:
                        break
                except KeyboardInterrupt:
                    print()
                    if inquire():
                        continue
                    else:
                        break
                except:
                    print("程序异常退出，希望反馈作者！")
                    return
    except KeyboardInterrupt:
        input("程序退出...")
    finally:
        os.system("pause")
        # pass


def inquire():
    redown = None
    while redown not in ('y', 'n'):
        try:
            redown = input("是否继续[y/n]: ")
        except (KeyboardInterrupt, EOFError):
            print()
    return redown == 'y'


def match_mooc(url):
    mooc = None
    for mooc_name in courses_mooc:
        if courses_re.get(mooc_name).match(url):
            mooc = courses_mooc.get(mooc_name)()
            break
    return mooc


def main():
    mooc_interface()


if __name__ == '__main__':
    main()
