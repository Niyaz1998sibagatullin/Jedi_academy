from django.db.models import Count
from django.shortcuts import render
from .models import *
from django.conf import settings
from django.core.mail import send_mail


def index(request):
    return render(request, "home.html")


# Создание нового кандидата
def new_candidate(request):
    if request.method == "POST":
        candidate = Candidate.objects.create(
            planet_id=request.POST.get("planet"),
            email=request.POST.get("email"),
            name=request.POST.get("name"),
            age=request.POST.get("age"),
        )
        test_question = TestQuestion.objects.all()
        test_answer = TestAnswer.objects.all()
        return render(request, "test.html",
                      {"candidate_id": candidate.id, "Questions": test_question,
                       "Answers": test_answer})
    planet = Planet.objects.all()
    return render(request, "candidate.html", {"planet": planet})


# Выводит для Джедая список возможных ему учеников
def jedi_list_candidate(request):
    jedi = request.POST.get('selected_jedi')
    context = ({'selected_jedi': jedi,
                'master_jedi': jedi,
                'list_candidate': Candidate.objects.all().filter(
                    name__icontains=request.POST.get('name_filter', ''),
                    age__gte=request.POST.get('age_filter', 0),
                    planet=Jedi.objects.get(id=jedi).planet, jedi__isnull=True)})
    return render(request, "jedi_list_candidate.html", context)


# Выводит список джедаев
def jedi_list(request):
    all_jedi = Jedi.objects.all()
    return render(request, 'jedi_list.html', {'all_jedi': all_jedi})


def jedi_candidates(request, jedi_id, candidate_id):
    candidate = Candidate.objects.get(id=candidate_id)
    jedi = Jedi.objects.get(id=jedi_id)
    number_of_candidate = Jedi.objects.filter(id=jedi_id).aggregate(Count('candidate'))

    if number_of_candidate['candidate__count'] < 3:
        test_list = CandidateAnswers.objects.all()
        number_of_questions = test_list.filter(candidate_id=candidate_id).count()
        number_of_answers = test_list.filter(test_answer__is_correct_answer=
                                             True, candidate__id=candidate_id
                                             ).count()
        candidate.jedi = jedi
        candidate.save()
        letter = (
            'Мастер Джедай {0} взял к себе в ученики. Количество правильных '
            'ответов за тест {1} из {2} вопросов. Вы вступили  в орден'
        ).format(jedi.name, number_of_answers, number_of_questions)
        send_mail('Вы приняты в орден', letter, settings.EMAIL_HOST_USER,
                  [candidate.email])
        return render(request, "info.html", {
            "text": "{0}, взял в падаваны: {1}".format(jedi.name,
                                                       candidate.name)})
    else:
        return render(request, "info.html", {
            "text": "У Вас и так уже 3 падавана. Пока Вы не можете взять себе новых падаванов."})


# Выводит ответы за тест выбранного кандидата
def answer_test(request, candidate_id):
    test_list = CandidateAnswers.objects.all().filter(candidate=candidate_id)
    context = ({"test_list": test_list, "candidate_name": Candidate.objects.get(id__exact=candidate_id).name})
    return render(request, "answer_test.html", context)


# Выводит список вопроов
def entry_test(request):
    id_candidate = request.POST.get("candidate_id")
    for test_question in TestQuestion.objects.all():
        selected_option = request.POST.get(str(test_question.id))
        test_answer = TestAnswer.objects.get(id=int(selected_option))
        CandidateAnswers.objects.create(test_question=test_question, test_answer=test_answer, candidate_id=id_candidate)
    return render(request, "home.html")


# Выводит полный список джедаев с кол-вом падаванов
def show_jedi_count(request):
    jedi = Jedi.objects.all().annotate(Count('candidate'))
    context = {'jedi': jedi}
    return render(request, "show_jedi_count.html", context)


# Выводит всех джедаев у которых более 1-го падавана
def jedi_candidate_one(request):
    jedi = Jedi.objects.annotate(num=Count('candidate')).filter(num__gt=1)
    context = {'jedi': jedi}
    return render(request, "jedi_candidate_one.html", context)

