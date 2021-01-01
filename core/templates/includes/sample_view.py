def myView(request):
    form = myForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    return render(request, 'my_template.html', {'form': form})