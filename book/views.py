from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Book, IssueBook
from django.db.models import Sum
from openpyxl import Workbook  #its use for excel download
from django.http import HttpResponse #its use for excel download
from django.core.paginator import Paginator  #its use for page shows
from .models import Login
from django.contrib.auth.hashers import check_password, make_password



def login(request):
    
    if request.method == "POST":

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            user = Login.objects.get(username=username)

            if password == user.password:
                request.session['user_id'] = user.id
                return redirect('home')

            else:
                return render(request, "login.html", {
                    "error": "Invalid password"
                })

        except Login.DoesNotExist:
            return render(request, "login.html", {
                "error": "User not found"
            })

    return render(request, "login.html")


def home(request):

    total_student = Student.objects.count()

    total_books = Book.objects.aggregate(
        total=Sum("quantity")
    )["total"] or 0

    issued_books = IssueBook.objects.filter(
        status="Issued"
    ).count()

    available_books = total_books - issued_books

    
    recent_issues = IssueBook.objects.filter(
        status="Issued"
    ).order_by("-id")[:5] #slicing

    context = {
        "total_student": total_student,
        "total_books": total_books,
        "issued_books": issued_books,
        "available_books": available_books,
        "recent_issues": recent_issues,
    }

    return render(request, "home.html", context)



def student_list(request):
    
    search = request.GET.get("search")

    if search:
        students = Student.objects.filter(name__icontains=search)
    else:
        students = Student.objects.all()

    paginator = Paginator(students, 5)   # small letter variable

    page_number = request.GET.get("page")
    students = paginator.get_page(page_number)

    return render(request, "student_list.html", {
        "students": students
    })



def add_student(request):

    if request.method == "POST":

        Student.objects.create(

            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            department=request.POST.get("department"),
            year=request.POST.get("year"),
            age=request.POST.get("age"),
            
            grade=request.POST.get("grade"),
            status=request.POST.get("status"),
        )

        return redirect('student_list')
        
    
    return render(request,'student_add.html')

def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('student_list')

def book(request):
    
    search = request.GET.get("search")

    if search:
        books = Book.objects.filter(book_name__icontains=search)
    else:
        books = Book.objects.all()

    paginator = Paginator(books, 5)

    page_number = request.GET.get("page")
    books = paginator.get_page(page_number)

    return render(request, "book.html", {
        "books": books
    })

def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect('book_list')


def add_book(request):


    if request.method == 'POST':

        Book.objects.create(


        book_name = request.POST.get('book_name'),
        author = request.POST.get('author'),
        category = request.POST.get('category'),
        quantity = request.POST.get('quantity'),
        status = request.POST.get('status'),
            

        )

        return redirect('book_list')
    

    return render(request,'add_book.html')



def issue_book(request):
    students = Student.objects.all()  #its use for dropdown
    
    books = Book.objects.all()  #its use for dropdown

    if request.method == "POST":

        student = Student.objects.get(id=request.POST.get("student"))
        book = Book.objects.get(id=request.POST.get("book"))

        
        already_issued = IssueBook.objects.filter(
            student=student,
            book=book,
            status="Issued"
        ).exists()  

        if already_issued:
            return render(request, "issue_book.html", {
                "students": students,
                "books": books,
                "error": "This book is already issued to this student."
            })

        IssueBook.objects.create(
            student=student,
            student_name=student.name,
            book=book,
            book_name=book.book_name,
            status="Issued",
            issue_date=request.POST.get("issue_date"),
        )

        return redirect("home")

    return render(request, "issue_book.html", {
        "students": students,
        "books": books,
    })


def return_book(request):
    
    students = Student.objects.all()
    books = Book.objects.all()

    if request.method == "POST":

        student = Student.objects.get(id=request.POST.get("student"))
        book = Book.objects.get(id=request.POST.get("book"))

        issue = get_object_or_404(
            IssueBook,
            student=student,
            book=book,
            status="Issued"
        )

        issue.return_date = request.POST.get("return_date")
        issue.status = "Returned"
        issue.save()

        return redirect("home")

    return render(request, "return_book.html", {
        "students": students,
        "books": books,
    })


def edit_student(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == "POST":

        student.name = request.POST.get("name")
        student.email = request.POST.get('email')
        student.phone = request.POST.get('phone')
        student.department = request.POST.get('department')
        student.year = request.POST.get('year')
        student.age = request.POST.get('age')
        student.grade = request.POST.get('grade')
        student.status = request.POST.get('status')

        student.save()

        return redirect("student_list")
    
    return render(request,'student_edit.html',{"student":student})

def edit_book(request, id):

    
    
    book = get_object_or_404(Book, id=id)

    if request.method == "POST":

        book.book_name = request.POST.get("book_name")
        book.author = request.POST.get("author")
        book.category = request.POST.get("category")
        book.quantity = request.POST.get("quantity")
        
        book.status = request.POST.get("status")

        book.save()

        return redirect("book_list")

    return render(request, "edit_book.html", {"book": book})



def export_student_excel(request):

    wb = Workbook()
    ws = wb.active
    ws.title = "Students"

    ws.append([
        "ID",
        "Student Name",
        "Email",
        "Phone",
        "Department",
        "Year",
        "Status"
    ])

    students = Student.objects.all()

    for stu in students:
        ws.append([
            stu.id,
            stu.name,
            stu.email,
            stu.phone,
            stu.department,
            stu.year,
            stu.status
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = 'attachment; filename="students.xlsx"'

    wb.save(response)

    return response



def export_book_excel(request):
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Books"

    ws.append([
        "Book ID",
        "Book Name",
        "Author",
        "Category",
        "Quantity",
        "Status"
    ])

    books = Book.objects.all()

    for bk in books:
        ws.append([
            bk.id,
            bk.book_name,
            bk.author,
            bk.category,
            bk.quantity,
            bk.status
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = 'attachment; filename="books.xlsx"'

    wb.save(response)

    return response




def setting(request):

    if request.method == "POST":

        username = request.POST.get("username")
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        dark_mode = request.POST.get("dark_mode")

        try:
            user = Login.objects.get(username=username)

    
            if user.password != current_password:
                return render(request, "setting.html", {
                    "error": "Current password wrong"
                })

            
            if new_password != confirm_password:
                return render(request, "setting.html", {
                    "error": "New password not matching"
                })

        
            user.password = new_password
            user.save()

            return render(request, "setting.html", {
                "success": "Password updated successfully"
            })

        except Login.DoesNotExist:
            return render(request, "setting.html", {
                "error": "User not found"
            })

    return render(request, "setting.html")