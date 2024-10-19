# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from .models import Todo
from event.models import UserTodo
from django.contrib.auth.decorators import login_required

@login_required
def add_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        # Create a new Todo instance and save it to the database
        todo = Todo(title=title, description=description)
        todo.save()
        userTodo = UserTodo(
            userID = request.user, #foreign key
            todoID = str(todo.pk)
        )
        userTodo.save()
        return redirect('list_todos')
    
    return render(request, 'todos/add_todo.html')  # Render a form template for adding todos

@login_required
def list_todos(request):
    # Retrieve all todos from the database
    userTodos = UserTodo.objects.filter(userID = request.user.id)
    todo_ids = [user_todo.todoID for user_todo in userTodos]
    todos = Todo.objects.filter(id__in=todo_ids)
    
    return render(request, 'todos/list_todos.html', {'todos': todos})  # Render a template with the list of todos

@login_required
def delete_todo(request, todo_id):
    # Try to get the Todo object, raise a 404 error if not found
    try:
        todo = Todo.objects.get(id=todo_id)
        userTodo = UserTodo.objects.get(todoID=todo_id, userID=request.user.id)  # Check for user ownership
    except Todo.DoesNotExist:
        raise Http404("Todo not found")

    if request.method == 'POST':
        # If the request is POST, delete the todo
        todo.delete()
        userTodo.delete()
        return redirect('list_todos')
      
    # If GET request, render the confirmation page
    return render(request, 'todos/delete_todo.html', {'todo': todo})