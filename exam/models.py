from django.db import models
from tinymce.models import HTMLField
from courses.models import Branch,Unit,Lesson
from edu.models import Year
from student.models import Student
# # Create your models here.

class Quiz(models.Model):
	title =models.CharField(max_length=200)
	description = models.CharField(max_length=500, blank=True, null=True)
	year = models.ForeignKey(Year, on_delete=models.CASCADE)
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE, blank=True, null=True)
	lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return str(self.title)
	
	@property
	def get_questions(self):
		return self.quiz_questions.all()
	
	@property
	def get_grade(self):
		grade = 0
		for i in self.get_questions:
			grade += i.grade
		return grade


	

class Question(models.Model):
	text =HTMLField()
	grade = models.PositiveIntegerField(default=1)
	quiz = models.ForeignKey(Quiz, related_name="quiz_questions",on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	

	def __str__(self):
		return str(self.id)

	@property
	def get_answers(self):
		return self.question_answer.all()

	@property
	def get_answers_true(self):
		return self.question_answer.get(correct=True)

	def get(self):
		pass

class Answer(models.Model):
	text = HTMLField()
	correct = models.BooleanField(default=False)
	question = models.ForeignKey(Question, related_name="question_answer", on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.text


class Result(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	degree = models.IntegerField(blank=True, null=True)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f'{self.student} | {self.quiz}'
