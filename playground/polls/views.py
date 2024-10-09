# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from .models import Todo

def add_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        # Create a new Todo instance and save it to the database
        todo = Todo(title=title, description=description)
        todo.save()
        
        return redirect('list_todos')
    
    return render(request, 'polls/add_todo.html')  # Render a form template for adding todos

def list_todos(request):
    # Retrieve all todos from the database
    todos = Todo.objects.all()
    
    return render(request, 'polls/list_todos.html', {'todos': todos})  # Render a template with the list of todos

def delete_todo(request, todo_id):
    # Try to get the Todo object, raise a 404 error if not found
    try:
        todo = Todo.objects.get(id=todo_id)
    except Todo.DoesNotExist:
        raise Http404("Todo not found")

    if request.method == 'POST':
        # If the request is POST, delete the todo
        todo.delete()
        return redirect('list_todos')
      
    # If GET request, render the confirmation page
    return render(request, 'polls/delete_todo.html', {'todo': todo})