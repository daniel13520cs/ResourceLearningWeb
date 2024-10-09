# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Todo

def add_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        # Create a new Todo instance and save it to the database
        todo = Todo(title=title, description=description)
        todo.save()
        
        return JsonResponse({'message': 'Todo added successfully'})
    
    return render(request, 'polls/add_todo.html')  # Render a form template for adding todos

def list_todos(request):
    # Retrieve all todos from the database
    todos = Todo.objects.all()
    
    return render(request, 'polls/list_todos.html', {'todos': todos})  # Render a template with the list of todos

def delete_todo(request, todo_id):
    # Retrieve the Todo object by id or return a 404 if not found
    todo = get_object_or_404(Todo, id=todo_id)

    if request.method == 'POST':
        # If the request is POST, delete the todo
        todo.delete()
        return JsonResponse({'message': 'Todo deleted successfully'})
    
    # If GET request, render the confirmation page
    return render(request, 'polls/delete_todo.html', {'todo': todo})