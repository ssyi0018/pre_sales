from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


# 中间件类修改,设置页面权限访问
class AuthMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        # 排除不需要验证的页面
        if request.path_info in ['/login/', '/image/code/', '/user/add/',]:
            return
        # 如果方法没有返回值，None，继续往后走，有返回值则不继续执行可以重定向等
        # return HttpResponse('无权访问')
        info_dict = request.session.get('info')
        if info_dict:
            return
        else:
            return redirect('/login/')
    # def process_response(self, request, response):
    #     print('m1 out')
    #     return response
