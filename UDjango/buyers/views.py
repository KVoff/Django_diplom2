from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse


from .models import Buyer
from .forms import BuyerForm, BuyerLoginForm



def buyer_list(request):
    buyers = Buyer.objects.all()
    return render(request, 'buyers/buyer_list.html', {'buyers': buyers})



def buyer_detail(request, pk):
    buyer = get_object_or_404(Buyer, pk=pk)
    return render(request, 'buyers/buyer_detail.html', {'buyer': buyer})



def buyer_create(request):
    if request.method == "POST":
        form = BuyerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('buyers:buyer_list')
    else:
        form = BuyerForm()
    return render(request, 'buyers/buyer_form.html', {'form': form})



def buyer_update(request, pk):
    buyer = get_object_or_404(Buyer, pk=pk)
    if request.method == "POST":
        form = BuyerForm(request.POST, instance=buyer)
        if form.is_valid():
            form.save()
            return redirect('buyers:buyer_detail', pk=buyer.pk)
        else:
            print("Ошибки валидации:",
                  form.errors)  # Добавляем отладочный вывод
    else:
        form = BuyerForm(instance=buyer)
    return render(request, 'buyers/buyer_form.html',
                  {'form': form, 'buyer': buyer})



def buyer_delete(request, pk):
    buyer = get_object_or_404(Buyer, pk=pk)
    if request.method == "POST":
        buyer.delete()
        return redirect('buyers:buyer_list')
    return render(request, 'buyers/buyer_confirm_delete.html',
                  {'buyer': buyer})


# представление для логина
def buyer_login_view(request):
    if request.method == "POST":
        form = BuyerLoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            user = authenticate(phone_number=phone_number, password=password)
            if user:
                login(request, user)

                # 'profile' — путь по умолчанию, если next нет
                next_url = request.GET.get('next', 'profile')
                return redirect(next_url)
                # return redirect(reverse('profile'))
            else:
                form.add_error(None, "Неправильный номер телефона или пароль.")
    else:
        form = BuyerLoginForm()

    return render(request, "registration/buyers_login.html", {"form": form})
