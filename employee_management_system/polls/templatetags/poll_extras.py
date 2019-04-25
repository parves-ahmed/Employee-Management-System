from django import template
from polls.models import Question

register = template.Library()


def upper(value):
    return value.upper()


register.filter('upper', upper)


@register.simple_tag
def recent_polls(n=5, **kwargs):
    """Return recent n polls"""
    name = kwargs.get("name", "Argument is not passed")
    print(name)
    questions = Question.objects.all().order_by('-created_at')
    return questions[0:n]