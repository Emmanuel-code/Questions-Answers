from django import template
from ..models import Question,Answer


register = template.Library()
@register.simple_tag
def total_questions_answered():
    return Answer.objects.all()


@register.inclusion_tag('qanda/latest_posts.html')
def show_latest_questions(count=5):
    latest_questions=Question.objects.order_by('-created')[:count]
    return {'latest_questions':latest_questions}
