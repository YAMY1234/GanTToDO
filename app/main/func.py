# 功能函数
import datetime


# #####################################
# 实现to_json功能
# 为了方便对含有许多task的list的转换
# 不在task类内定义to_json，而是外部定义
# #####################################
class JSONHelper():
    @staticmethod
    def jsonBQlist(bqlist):
        result = []
        for item in bqlist:
            jsondata = {}
            # 想办法获取类的所有成员的值
            for name, value in vars(item).items():
                if(name[0] != '_' and name != 'user_id'):  # 过滤掉
                    # 可以用修饰器完成
                    if isinstance(value, datetime.date):
                        d = (str(value.day).zfill(2) + '-'
                             + str(value.month).zfill(2) + '-'
                             + str(value.year).zfill(4))
                        tdic = {name: d}
                    else:
                        tdic = {name: value}

                    jsondata.update(tdic)
            result.append(jsondata)
        return result
