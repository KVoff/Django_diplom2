# employee/views.py

from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate

from .forms import EmployeeLoginForm


def employee_login_view(request):
    if request.method == "POST":
        form = EmployeeLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            if user:
                login(request, user)
                return redirect(reverse('product_list'))
    else:
        form = EmployeeLoginForm()
    return render(request, "registration/employee_login.html", {"form": form})
