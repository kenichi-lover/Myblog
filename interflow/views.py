from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Board
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import InterflowInfoForm
from django.core.paginator import Paginator,EmptyPage
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.
def home_view(request):

    page_number_str = request.GET.get('page')
    interflow = Board.objects.all().order_by('-created')
    paginator = Paginator(interflow, 2)
    try:
        page_number = int(page_number_str) if page_number_str else 1
        page_obj = paginator.get_page(page_number)
    except (ValueError, TypeError):
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'interflow/interflow_detail.html', context)

class IndexView(LoginRequiredMixin,View):
    def get(self, request,id=None):
        if id is not None:
            inter_flows = Board.objects.all()
        else:
            inter_flows = Board.objects.filter(user_id=id)
        interflow_list = Board.objects.all().order_by('-created')
        form = InterflowInfoForm()
        context = {'inter_flows':inter_flows, 'interflow_list':interflow_list, 'form':form}
        return render(request,'interflow/index.html',context)
    def post(self, request,id=None):
        form = InterflowInfoForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.user = request.user
            board.save()
            return redirect('interflow:home')
        inter_flows = Board.objects.all()
        interflow_list = Board.objects.all().order_by('-created')
        context = {
            'inter_flows':inter_flows,
            'interflow_list':interflow_list,
            'form':form,
        }
        return render(request, 'interflow/index.html', context)

def page_list(request,id=None):
    if id :
        return redirect(f'{reverse("page_list")}?page={id}',
                        permanent=True)

    page_number_str = request.GET.get('page')
    pages = Board.objects.all().order_by('-created')
    paginator = Paginator(pages, 3)
    try:
        page_number = int(page_number_str) if page_number_str else 1
        page_obj = paginator.get_page(page_number)
    except (ValueError, TypeError):
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    return render(request, 'interflow/interflow_detail.html', {'page_obj': page_obj})

@login_required()
def publish_interflow(request):
    if request.method == "POST":
        form = InterflowInfoForm(request.POST,request.FILES)
        if form.is_valid():
            interflow = form.save(commit=False)

            interflow.user_id = request.user.id
            interflow.save()
            form.save_m2m()
            return redirect('interflow:home')
    else:
        form = InterflowInfoForm()
    return render(request,'interflow/index.html', {'form': form})

def test_view(request):
    inter_flows = Board.objects.all().order_by('-created')
    interflow = inter_flows[1]
    interflow.delete()
    return HttpResponse('成功')


