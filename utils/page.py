#__author:  Administrator
#date:  2016/12/7

class PagerHelper:
    def __init__(self,total_count,current_page,base_url,per_page=10):
        # 先接收变量，total_count所有数据个数，
        # current_page当前页，base_url现在URL，per_page每页10条数据？。
        self.total_count = total_count
        self.current_page = current_page
        self.base_url = base_url
        self.per_page = per_page

    @property
    def db_start(self):
        #当前页-1*每页显示多少数据=开始的页码
        return (self.current_page -1) * self.per_page

    @property
    def db_end(self):
        #当前页码*每页显示多少数据=结束的页码
        return self.current_page * self.per_page

    def total_page(self):

        v, a = divmod(self.total_count, self.per_page)
        #total_count=所有数据个数，per_page=每页显示多少数据

        #divmod函数把除数和余数运算结果结合起来，返回一个包含商和余数的元组(v=v // a, a=v % a)。
        #v整除a=数据一共能显示多少页，v除余a=显示那么多页之后还剩多少数据，
        #如果整除之后有余就说明要多显示一页，这就是最终的总页码。

        if a != 0:
            v += 1
        return v

    def pager_str(self):
        #寻呼机字符串？
        v = self.total_page()
        #v=最终页码
        pager_list = []
        #寻呼机列表？

        #当前页等于1的时候，上一页点了没效果。
        if self.current_page == 1:
            pager_list.append('<a href="javascript:void(0);">上一页</a>')
        else:
        #否则上一页能正常跳转
            pager_list.append('<a href="%s?p=%s">上一页</a>' % (self.base_url, self.current_page - 1,))
            #把上一页A标签的连接替换到前一页的页码

        # 6，1:12
        # 7，2:13
        if v <= 11:
            #如果最终总页码小于或等于11页，当前开始页=1，当前结束页=总页码
            pager_range_start = 1
            pager_range_end = v+1
        else:
            #总页码>11的情况下：如果当前页<6，当前开始页=1，当前结束页=12
            if self.current_page < 6:
                pager_range_start = 1
                pager_range_end = 11 + 1
            #总页码>11且当前页>6,
            else:
                #当前开始页=当前页-5，当前结束页=当前页+6
                pager_range_start = self.current_page - 5
                pager_range_end = self.current_page + 5 + 1

                #如果当前结束页>总页数，当前开始页就等于总页数-10，当前结束页就等于当前页+1
                if pager_range_end > v:
                    pager_range_start = v - 10
                    pager_range_end = v + 1

        #循环显示页码：
        for i in range(pager_range_start, pager_range_end):
            if i == self.current_page:#当前页页码=i
                #寻呼机列表里面加上URL+页码=当前页
                #类：变动的
                pager_list.append('<a class="active" href="%s?p=%s">%s</a>' % (self.base_url, i, i,))
            else:
                #列表里加上当前URL+当前页码
                pager_list.append('<a href="%s?p=%s">%s</a>' % (self.base_url, i, i,))

        #如果当前页码等于总页码，下一页没反应。
        if self.current_page == v:
            pager_list.append('<a href="javascript:void(0);">下一页</a>')
        else:
        #如果当前页码不是总页码，下一页有反应。
            pager_list.append('<a href="%s?p=%s">下一页</a>' % (self.base_url, self.current_page + 1,))

        #页码之间用空格分开，存入变量pager
        pager = "".join(pager_list)
        return pager