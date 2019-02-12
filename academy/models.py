from django.db import models


class Planet(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        verbose_name = 'Планета'
        verbose_name_plural = 'Планеты'

    def __str__(self):
        return self.name


class Jedi(models.Model):
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Джедай'
        verbose_name_plural = 'Джедаи'

    def __str__(self):
        return self.name


class Candidate(models.Model):
    jedi = models.ForeignKey(Jedi, blank=True, null=True, on_delete=models.SET_NULL)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    age = models.IntegerField()

    class Meta:
        verbose_name = 'Кандидат'
        verbose_name_plural = 'Кандидаты'

        def __str__(self):
            return self.name


class TestQuestion(models.Model):
    text = models.TextField()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.text[:50]


class TestAnswer(models.Model):
    question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct_answer = models.BooleanField()

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопросы'

        def __str__(self):
            return self.text


class CandidateAnswers(models.Model):
    test_question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE)
    test_answer = models.ForeignKey(TestAnswer, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
