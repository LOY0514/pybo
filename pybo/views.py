from django.shortcuts import render ,get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required


from .forms import QuestionForm, AnswerForm


from .models import Question, Answer

from .SwingData1 import MainSwingCheck, SwingData1
# Create your views here.

def index(request):
    
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    
    question = Question.objects.get(id=question_id)
    context = {'question': question}
    
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url = 'common:login')
def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
# ---------------------------------- [edit] ---------------------------------- #

    if request.method == "POST":
        form = AnswerForm(request.POST)
        
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
        
    else:
        form = AnswerForm()
        
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url = 'common:login')
def question_create(request):
    """
    pybo 질문등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        
        if form.is_valid():
            
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            """
            
            loc_url = "http://192.168.43.106/"
            loc_pathBase = "pybo/SwingData"
            question_name = question.subject
            result = MainSwingCheck(loc_url, loc_pathBase, question_name)
            
            checklist = result[0]
            mainData = result[1]
            
            question.elbowCheck = checklist['check1']
            question.dampCheck = checklist['check2']
            question.vibCheck = checklist['check3']
            question.backAngCheck = checklist['check4']
            question.rlTimeCheck = checklist['check5']
            question.rlAngCheck = checklist['check6']
            
            """
            data = [[1 for i in range(500)] for i in range(17)]
            data[0] = list(range(500))
            data[10] = list(range(500))
            
            filename = question.subject
            SwingData = SwingData1(filename, data)
            SwingData.save()
            SwingData.plot_save()
            
            question.elbowCheck = 0
            question.dampCheck = 0
            question.vibCheck = 0
            question.backAngCheck = 0
            question.rlTimeCheck = 0
            question.rlAngCheck = 0
            
            
            return redirect('pybo:index')
        
    else:
        form = QuestionForm()
        
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


def mypage(request):
    
    User = request.user
    user_question = Question.objects.filter(author=User)
    
    context = {'question_list': user_question}
    
    return render(request, 'pybo/question_list.html', context)