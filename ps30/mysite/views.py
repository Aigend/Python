from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.core.signals import request_started, request_finished
from .forms import TaskForm
from .models import Task


# Create a task
def task_create(request):
    # 如果用户通过POST提交，通过request.POST获取提交数据
    if request.method == "POST":
        # 将用户提交数据与TaskForm表单绑定
        form = TaskForm(request.POST)
        # 表单验证，如果表单有效，将数据存入数据库
        if form.is_valid():
            form.save()
            # 跳转到任务清单
            return redirect(reverse("tasks:task_list"))
    else:
        # 否则空表单
        form = TaskForm()
    return render(request, "tasks/task_form.html", {"form": form, })


# Retrieve task list
def task_list(request):
    # from django.template import RequestContext
    # high_priority_context = RequestContext(request)
    # high_priority_context.push({"site_name": "Adrian"})
    # 从数据库获取任务清单
    tasks = Task.objects.all()
    # 指定渲染模板并传递数据
    return render(request, "tasks/task_list.html", {"tasks": tasks})


# Retrieve a single task
def task_detail(request, pk):
    # 从url里获取单个任务的pk值，然后查询数据库获得单个对象
    task = get_object_or_404(Task, pk=pk)
    return render(request, "tasks/task_detail.html", {"task": task})


# Update a single task
def task_update(request, pk):
    # 从url里获取单个任务的pk值，然后查询数据库获得单个对象实例
    task_obj = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(instance=task_obj, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("tasks:task_detail", args=[pk, ]))
    else:
        form = TaskForm(instance=task_obj)
    return render(request, "tasks/task_form.html", {"form": form, "object": task_obj})


# Delete a single task
def task_delete(request, pk):
    # 从url里获取单个任务的pk值，然后查询数据库获得单个对象
    task_obj = get_object_or_404(Task, pk=pk)
    task_obj.delete()  # 删除然后跳转
    return redirect(reverse("tasks:task_list"))


def request_started_callback(sender, **kwargs):
    pass
    # print("请求开始：%s" % kwargs['environ'])


def request_finished_callback(sender, **kwargs):
    pass
    # print("请求完成")


request_started.connect(request_started_callback)
request_finished.connect(request_finished_callback)

from mysite.signal import register_signal


def hello_my_signal(request):
    # 注意要和回调函数中的**kwargs的参数保持一致
    # 参数 sender（信号发送者指函数） **named（**kwargs参数相同）
    register_signal.send(hello_my_signal, request=request, user="admin")
    print("注册成功已经发送邮件")
    return JsonResponse({"msg": 'Hello signal'})
