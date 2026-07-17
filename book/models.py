from django.db import models

class Login(models.Model):
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=7)

    def __str__(self):
        return self.username
    

class Student(models.Model):
    name = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    department = models.CharField(max_length=50)
    year = models.IntegerField()
    age = models.IntegerField()
    grade = models.CharField(max_length=10, default="A")
    status = models.CharField(max_length=20, default="Active")
    
    def __str__(self):
        return self.name
    
class Book(models.Model):


    book_id = models.CharField(max_length=10)
    book_name = models.CharField(max_length=20)
    author = models.CharField(max_length=10)
    category = models.CharField(max_length=15)
    quantity = models.IntegerField(default=2)
    available = models.IntegerField(default=0)
    status = models.CharField(max_length=8, default="Available")
    


    def __str__(self):
        return self.book_name
    
class IssueBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=15)
    status = models.CharField(max_length= 10,default="Issued")
    issue_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    

    def __str__(self):
        return self.book.book_name
    

    

    