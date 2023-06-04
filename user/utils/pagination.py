# 自定义分页组件
from django.utils.safestring import mark_safe
import copy


class Pagination(object):

    def __init__(self, request, queryset, page_size=10, page_param='page', plus=5):
        """
        :param request:请求对象
        :param queryset:查询符合条件数据，根据这个数据分页处理
        :param page_size:每页显示多少条数据
        :param page_param:在URL中传递的分页参数，例如：/user/list/?page=11
        :param plus:显示当前页的，前或后的几页页码
        """

        # 获取get请求中的参数
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True  # 设置setlist可以修改
        self.query_dict = query_dict

        self.page_param = page_param
        page = request.GET.get(page_param, '1')  # 分页
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page  # 获取到当前页
        self.page_size = page_size  # 每页显示条数

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        # 数据总条数
        total_num = queryset.count()

        # 计算出总页码 divmod函数计算商和余数
        total_page, div = divmod(total_num, page_size)
        if div:
            total_page += 1
        self.total_page = total_page
        self.plus = plus

    def html(self):
        # 根据当前页计算出前后5页

        if self.total_page <= 2 * self.plus + 1:
            # 当数据库数据少的时候，没有达到11页
            start_page = 1
            end_page = self.total_page
        else:
            # 数据库数据比较多，判断当前页,<5
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus
            else:
                # 当前页大于5
                if (self.page + self.plus) > self.total_page:
                    start_page = self.total_page - 2 * self.plus
                    end_page = self.total_page
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码
        page_list = []

        # 参数进行组装增加新的搜索内容，先setlist再urlencode转换格式
        self.query_dict.setlist(self.page_param, [1])
        page_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))
        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_list.append(prev)

        # 分页页面
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_list.append(ele)

        # 下一页
        if self.page < self.total_page:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_list.append(prev)

        self.query_dict.setlist(self.page_param, [self.total_page])
        page_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        search_tz = '''
                        <li>
                           <form style="float: left;margin-left: -1px" method="get">
                               <input name="page"
                                      style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0;"
                                      type="text" class="form-control" placeholder="页码">
                               <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
                               </span>
                           </form>
                       </li>
           '''
        page_list.append(search_tz)

        # 导入mark_safe，把数据包裹成安全的传递给html
        page_string = mark_safe(''.join(page_list))
        return page_string
