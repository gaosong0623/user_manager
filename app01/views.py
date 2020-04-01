
from app01 import models
from django.shortcuts import render, redirect, HttpResponse
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "user_manager.settings")
django.setup()

def login(request):
    message = ""
    v = request.session
    # requests库的session会话对象可以跨请求保持某些参数，
    # 说白了，就是比如你使用session成功的登录了某个网站，
    # 则在再次使用该session对象求求该网站的其他网页都会默认使用该session之前使用的cookie等参数
    from django.contrib.sessions.backends.db import SessionStore
    #判断你请求的方法如果是POST:
    if request.method == "POST":
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        identity =request.POST.get('identity')
        #Administrator是一张表（存用户名密码的），.objects.filter()方法是用来查询表格里面的内容的，
        #.count()方法是用来获取查询到的结果有多大，命名为C
        c = models.administrator.objects.filter(username=user, password=pwd,identity=identity).count()
        if c:
            #如果C存在的话，就把登录状态改成正确，登录名改成用户名
            #request.session[]方法就相当于一个名片，能储存你想要储存的信息，然后跳转到登录界面！
            request.session['is_login'] = True
            request.session['username'] = user
            request.session['identity'] = identity
            #把用户的唯一ID通过一系列复杂的查询转化取出来然后存到cookie
            request.session['User_unique_ID'] = list(models.administrator.objects.filter(username=user,password=pwd,identity=identity).values('unique_id'))[0].get('unique_id')
            rep = redirect('/index.html')
            return rep
        else:
            message = "用户名或密码错误"
    obj = render(request,'login.html', {'msg': message})
    #render()方法是一个渲染函数，你可以放进去你要渲染的页面，和你的错误信息~一起返回回去
    return obj

def logout(request):
    request.session.clear()
    return redirect('/login.html')



def auth(func):
    def inner(request, *args, **kwargs):
        is_login = request.session.get('is_login')
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return redirect('/login.html')
    return inner

@auth
def index(request):
    current_user = request.session.get('username')
    return render(request, 'index.html',{'username': current_user})






#学生管理
@auth
def handle_student(request):
    #先拿到当前登录人的名字
    current_user = request.session.get('username')
    #拿到当前登录人的身份
    identity = request.session.get('identity')
    #根据不同身份返回不同界面：

    if identity =="root":
        #管理员返回全部学生列表
        if request.method == "GET":
            # 获取当前页，如果没传默认是1
            current_page = request.GET.get('p', 1)
            current_page = int(current_page)

            # 所有数据的个数
            total_count = models.classes.objects.all().count()
            print("数据个数=" + str(total_count))

            from utils.page import PagerHelper
            # 创建中间人obj，中间人调用pager_str()方法，经过一系列处理后把页码标签返回给你，赋值给变量pager
            obj = PagerHelper(total_count, current_page, '/student.html', 10)
            pager = obj.pager_str()
            student_list = models.student.objects.all()[obj.db_start:obj.db_end]
            current_user = request.session.get('username')

            return render(request,
                          'student.html',
                          {'student_list': student_list,
                           'username': current_user,
                           'str_pager': pager}, )


    if identity =="teacher":
        #老师返回自己管理班级的信息
        pass

    if identity =="student":
        #学生返回自己的信息

        User_unique_ID = request.session.get('User_unique_ID')
        #拿到学生的用户唯一ID，如果在学生表里能找到这个ID，就说明已经完善过学生信息了，直接显示就OK，
        #如果找不到，就显示现有信息，然后完善，补充到学生表去。
        c = models.student.objects.filter(student_id=User_unique_ID).count()
        if c:
            if request.method == "GET":
                #显示自己的学生信息
                # 获取当前页，如果没传默认是1
                current_page = request.GET.get('p', 1)
                current_page = int(current_page)

                # 数据的个数
                total_count =c
                from utils.page import PagerHelper
                # 创建中间人obj，中间人调用pager_str()方法，经过一系列处理后把页码标签返回给你，赋值给变量pager
                obj = PagerHelper(total_count, current_page, '/classes.html', 10)
                pager = obj.pager_str()
                student_list = models.student.objects.filter(student_id=User_unique_ID)
                current_user = request.session.get('username')

                return render(request,
                              'student.html',
                              {'student_list': student_list,
                               'username': current_user,
                               'str_pager': pager}, )

        else:
            message = "没有找到您的信息，请点此完善"

            return render(request,
                          'Error_pages.html',
                          {'User_unique_ID': User_unique_ID,
                           'msg': message
                           })






    else:
        return redirect('/index.html')

#报错界面，补充学生信息界面
@auth
def Error_pages(request):
    # 先拿到当前登录人的名字
    current_user = request.session.get('username')
    # 拿到当前登录人的身份
    identity = request.session.get('identity')
    # 拿到登录人的ID
    User_unique_ID = request.session.get('User_unique_ID')
    if request.method == "GET":
        return render(request, 'Error_pages.html', )

    if request.method == "POST":
        import json
        # status，状态。 error，错误信息。data，数据。demand,需求。
        response_dict = {'status': True, 'error': None, 'data': None, 'demand': None}
        demand = request.POST.get('demand', None)

        gender = request.POST.get('gender', None)
        name = request.POST.get('name', None)
        cls = request.POST.get('cls', None)
        phone = request.POST.get('phone', None)
        emile = request.POST.get('emile', None)
        student_id = request.session.get('User_unique_ID')
        print(gender,name,cls,phone,emile,student_id)
        print("需求" + demand)
        # 先判断需求是啥子：
        if demand == "add":
            if gender:
                obj = models.student.objects.create(gender=gender,name=name,cls=cls,phone=phone,emile=emile,student_id=student_id)


            else:
                response_dict['status'] = False
                response_dict['error'] = "标题不能为空"
            return HttpResponse(json.dumps(response_dict))



#老师管理
@auth
def handle_teacher(request):
    # 先拿到当前登录人的名字
    current_user = request.session.get('username')
    # 拿到当前登录人的身份
    identity = request.session.get('identity')
    # 拿到登录人的ID
    User_unique_ID = request.session.get('User_unique_ID')


    if request.method == "GET":
        #显示老师和他教的所有的班级。
        # 获取当前页，如果没传默认是1
        current_page = request.GET.get('p', 1)
        current_page = int(current_page)

        # 所有数据的个数
        total_count = models.teacher.objects.all().count()
        print("数据个数=" + str(total_count))

        from utils.page import PagerHelper
        # 创建中间人obj，中间人调用pager_str()方法，经过一系列处理后把页码标签返回给你，赋值给变量pager
        obj = PagerHelper(total_count, current_page, '/teacher.html', 10)
        pager = obj.pager_str()

        #一次性把老师列表全部都拿到
        teacher_list = models.teacher.objects.filter(id__in=models.teacher.objects.all()).values('id', 'name', 'cls__id', 'cls__caption')
        result = {}
        for t in teacher_list:

            if t['id'] in result:
                if t['cls__id']:
                    result[t['id']]['cls_list'].append({'id': t['cls__id'], 'caption': t['cls__caption']})
            else:
                if t['cls__id']:
                    temp = [{'id': t['cls__id'], 'caption': t['cls__caption']}, ]
                else:
                    temp = []
                result[t['id']] = {
                    'nid': t['id'],
                    'name': t['name'],
                    'cls_list': temp
                }

        return render(request, 'teacher.html', {'username': current_user,'pager':pager,'teacher_list':result})
    else:
        return render(request, 'teacher.html', {'username': current_user})

#添加老师
def add_teacher(request):
    if request.method == 'GET':
        cls_list = models.classes.objects.all()
        return render(request, 'add_teacher.html', {'cls_list': cls_list})
    elif request.method == "POST":
        name = request.POST.get('name')
        cls = request.POST.getlist('cls')
        #创建老师
        obj = models.teacher.objects.create(name=name)
        # 创建老师和班级的对应关系
        obj.cls.add(*cls)


        return redirect('/teacher.html')

def edit_teacher(request,nid):
    # 获取当前老师信息
    # 获取当前老师对应的所有班级
    # - 获取所有的班级
    # - 获取当前老师未对应的所有班级
    if request.method == "GET":
        # 当前老师的信息
        obj = models.teacher.objects.get(id=nid)

        # 获取当前老师已经管理的所有班级
        # [ (1,"root1"),(2,"root2"),(3,"root3"),]
        obj_cls_list = obj.cls.all().values_list('id', 'caption')

        # 已经管理的班级的ID列表
        id_list = list(zip(*obj_cls_list))[0] if obj_cls_list else []
        # # [1,2,3]


        # 获取不包括已经管理的班级，
        cls_list = models.classes.objects.exclude(id__in=id_list)
        # # 1
        return render(request, 'edit_teacher.html', {'obj': obj,
                                                     'obj_cls_list': obj_cls_list,
                                                     "cls_list": cls_list,
                                                     "id_list": id_list
                                                     })
    elif request.method == "POST":
        # nid = request.POST.get('nid')
        name = request.POST.get('name')
        cls_li = request.POST.getlist('cls')
        obj = models.teacher.objects.get(id=nid)
        obj.name = name
        obj.save()

        obj.cls.set(cls_li)

        return redirect('/teacher.html')




def mother_set(request):
    return render(request, "mother_set.html")

def registered(request):
    if request.method == "POST":

        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        name = request.POST.get("name", None)
        emile = request.POST.get("emile", None)
        phone = request.POST.get("phone", None)
        gender = request.POST.get("gender", None)
        identity = request.POST.get("identity", None)
        print(username,password,name,emile,phone,gender,identity)

        # Administrator是一张表（存用户信息的），.objects.create()方法是用来增加内容的

        import uuid
        unique_id=uuid.uuid1()
        print(unique_id)

        d = models.administrator.objects.create(
            username=username,
            password=password,
            name=name,
            emile=emile,
            phone=phone,
            unique_id=unique_id,
            gender=gender,
            identity=identity,
        )

        if d:
            # 如果d存在的话，说明数据存入成功了，告知用户并且，跳转到登录界面！
            message = "注册成功！请点击登录跳转登录界面……"
            obj = render(request, 'registered.html', {'msg': message})
            # render()方法是一个渲染函数，你可以放进去你要渲染的页面，和你的错误信息~一起返回回去
            return obj

        else:
            message = "注册失败……"
            obj = render(request, 'login.html', {'msg': message})
            return obj

    return render(request, "registered.html")




#班级管理
@auth
def handle_class(request):
    # 如果是GET请求访问说明是访问页面，正常渲染数据库里面的内容。
    if request.method == "GET":
        # 获取当前页，如果没传默认是1
        current_page = request.GET.get('p', 1)
        current_page = int(current_page)

        # 所有数据的个数
        total_count = models.classes.objects.all().count()
        print("数据个数="+str(total_count))

        from utils.page import PagerHelper
        #创建中间人obj，中间人调用pager_str()方法，经过一系列处理后把页码标签返回给你，赋值给变量pager
        obj = PagerHelper(total_count, current_page, '/classes.html', 10)
        pager = obj.pager_str()
        clss_list = models.classes.objects.all()[obj.db_start:obj.db_end]
        current_user = request.session.get('username')

        return render(request,
                      'classes.html',
                     {'clsss_list': clss_list,
                      'username': current_user,
                      'str_pager': pager},)
    #如果是POST请求说明是提交数据，获取到前端提取的caption值，
    #如果不为空的话添加到数据库里，把数据更新到响应列表，再把这个响应列表返回给前端，
    # 再追加在表单末端，个人觉得这种方式很鸡肋，不喜欢。
    elif request.method == "POST":
        # Ajax
        import json
        #status，状态。 error，错误。data，数据。demand,需求。
        response_dict = {'status': True, 'error': None, 'data': None, 'demand': None}
        caption = request.POST.get('caption', None)
        demand=request.POST.get('demand', None)
        print("需求"+demand)
        # 先判断需求是啥子：
        if demand == "add":
            if caption:
                obj = models.classes.objects.create(caption=caption)
                response_dict['data'] = {'id': obj.id, 'caption': obj.caption}
            else:
                response_dict['status'] = False
                response_dict['error'] = "标题不能为空"
            return HttpResponse(json.dumps(response_dict))

        if demand == "edit":
            nid = request.POST.get('id')
            caption = request.POST.get('caption')
            print(nid,caption)
            if caption:
                models.classes.objects.filter(id=nid).update(caption=caption)
                response_dict['error'] =True
            else:
                response_dict['status'] = False
                response_dict['error'] = "标题不能为空"
            return HttpResponse(json.dumps(response_dict))

        if demand == "Delete":
            nid = request.POST.get('id')
            print(nid,demand)
            if nid:
                models.classes.objects.filter(id=nid).delete()
                response_dict['error'] = True
            else:
                response_dict['status'] = False
                response_dict['error'] = "删除失败，请重新操作。"
            return HttpResponse(json.dumps(response_dict))

        else:
            return redirect('/classes.html')



@auth
def handle_add_classes(request):
    message = ""
    if request.method == "GET":
        return render(request, 'add_classes.html', {'msg': message})
    elif request.method == "POST":
        caption = request.POST.get('caption',None)
        if caption:
            models.classes.objects.create(caption=caption)
        else:
            message = "班级名称不能为空"
            return render(request, 'add_classes.html', {'msg': message})
        return redirect('/classes.html')
    else:
        return redirect('/index.html')

@auth
def handle_edit_classes(request):
    if request.method == "GET":
        nid = request.GET.get('nid')
        obj = models.classes.objects.filter(id=nid).first()
        return render(request, 'edit_classes.html', {'obj': obj})
    elif request.method == "POST":
        nid = request.POST.get('nid')
        caption = request.POST.get('caption')
        print(nid,caption)
        models.classes.objects.filter(id=nid).update(caption=caption)
        return redirect('/classes.html')
    else:
        return redirect('/index.html')






def test(request):
    di = {'k1': 'v1','name': 'shahu'}
    import json
    return HttpResponse(json.dumps(di))
    # return render(request,'test.html',{'k1': 'v1'})
def page(request):
    return render(request, 'page.html')
@auth
def add_student(request):
    if request.method == "GET":
        cls_list = models.classes.objects.all()[0: 20]
        return render(request, 'add_student.html', {'cls_list': cls_list})
    elif request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        cls_id = request.POST.get('cls_id')
        models.student.objects.create(name=name,email=email,cls_id=cls_id)
        return redirect('/student.html')
@auth
def edit_student(request):
    if request.method == "GET":
        cls_list = models.classes.objects.all()[0: 20]
        nid = request.GET.get('nid')
        obj = models.student.objects.get(id=nid)
        return render(request, 'edit_student.html', {'cls_list': cls_list, "obj": obj})
    elif request.method == "POST":
        nid = request.POST.get('id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        cls_id = request.POST.get('cls_id')
        models.student.objects.filter(id=nid).update(name=name,email=email,cls_id=cls_id)
        return redirect('/student.html')





