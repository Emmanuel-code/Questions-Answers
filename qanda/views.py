from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect, HttpResponseBadRequest
from django.urls.base import reverse
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DayArchiveView,
    DetailView,
    RedirectView,
    UpdateView,
    ListView
)
from django.shortcuts import render
from .forms import QuestionForm, AnswerForm, AnswerAcceptanceForm,CommentForm
from .models import Question, Answer,Comment
from django.db.models import Q
# import request
# from bs4 import BeautifulSoup




def search_questions(request):
    query=request.GET.get('q')

    questions=Question.objects.filter(Q(title__icontains=query) |
                                              Q(question__icontains=query)
                                                ).distinct()

    return render(request,'qanda/search.html',{'questions':questions})


class AskQuestionView(LoginRequiredMixin, CreateView):
    form_class = QuestionForm
    template_name = 'qanda/ask.html'

    def get_initial(self):
        return {
            'user': self.request.user.id
        }

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            # save and redirect as usual.
            return super().form_valid(form)
        elif action == 'PREVIEW':
            preview = Question(
                question=form.cleaned_data['question'],
                title=form.cleaned_data['title'])
            ctx = self.get_context_data(preview=preview)
            return self.render_to_response(context=ctx)
        return HttpResponseBadRequest()


class CreateAnswerView(LoginRequiredMixin, CreateView):
    form_class = AnswerForm
    template_name = 'qanda/create_answer.html'

    def get_initial(self):
        return {
            'question': self.get_question().id,
            'user': self.request.user.id,
        }

    def get_context_data(self, **kwargs):
        return super().get_context_data(question=self.get_question(),
                                        **kwargs)

    def get_success_url(self):
        return self.object.question.get_absolute_url()

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            # save and redirect as usual.
            return super().form_valid(form)
        elif action == 'PREVIEW':
            ctx = self.get_context_data(preview=form.cleaned_data['answer'])
            return self.render_to_response(context=ctx)
        return HttpResponseBadRequest()

    def get_question(self):
        return Question.objects.get(pk=self.kwargs['pk'])


class DailyQuestionList(DayArchiveView):
    queryset = Question.objects.all()
    date_field = 'created'
    month_format = '%m'
    allow_empty = True


class QuestionDetailView(DetailView):
    model = Question

    ACCEPT_FORM = AnswerAcceptanceForm(initial={'accepted': True})
    REJECT_FORM = AnswerAcceptanceForm(initial={'accepted': False})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'answer_form': AnswerForm(initial={
                'user': self.request.user.id,
                'question': self.object.id,
            })
        })
        if self.object.can_accept_answers(self.request.user):
            ctx.update({
                'accept_form': self.ACCEPT_FORM,
                'reject_form': self.REJECT_FORM,
            })
        return ctx


class TodaysQuestionList(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        today = timezone.now()
        return reverse(
            'questions:daily_questions',
            kwargs={
                'day': today.day,
                'month': today.month,
                'year': today.year,
            }
        )


class UpdateAnswerAcceptanceView(LoginRequiredMixin, UpdateView):
    form_class = AnswerAcceptanceForm
    queryset = Answer.objects.all()

    def get_success_url(self):
        return self.object.question.get_absolute_url()

    def form_invalid(self, form):
        return HttpResponseRedirect(
            redirect_to=self.object.question.get_absolute_url())

#
# def comment_view(request):
#
#     new_comment = None
#     if request.method == 'POST':
#         # A comment was posted
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             # Create Comment object but don't save to database yet
#             new_comment = comment_form.save(commit=False)
#             # Assign the current post to the comment
#             new_comment.post = post
#             # Save the comment to the database
#             new_comment.save()
#     else:
#         comment_form = CommentForm()
#     return render(request,'qanda/comment.html',{ 'new_comment': new_comment,'comment_form': comment_form})
#
#
class CreateComment(CreateView):
    form_class = CommentForm
    template_name = 'qanda/comment.html'

    def get_initial(self):
        return {
            'answer': self.get_answer().id,
            'user': self.request.user.id,
        }

    def get_context_data(self, **kwargs):
        return super().get_context_data(answer=self.get_answer(),
                                        **kwargs)

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            # save and redirect as usual.
            return super().form_valid(form)
        elif action == 'PREVIEW':
            ctx = self.get_context_data(preview=form.cleaned_data['answer'])
            return self.render_to_response(context=ctx)
        return HttpResponseBadRequest()

    def get_answer(self):
        return Answer(self.kwargs['pk'])


class QuestionListView(ListView):
    model = Question
    context_object_name = 'questions'
    template_name = 'qanda/all.html'
    paginate_by = 3

