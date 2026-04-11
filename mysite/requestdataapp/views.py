from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages


def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    result = a + b
    context = {
        "a": a,
        "b": b,
        "result": result,
    }
    return render(request, "requestdataapp/request_query_params.html", context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    return render(request, "requestdataapp/user-bio-form.html")


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    MAX_UPLOAD_SIZE = 1 * 1024 * 1024

    if request.method == "POST":
        uploaded_file = request.FILES.get("myfile")

        if not uploaded_file:
            messages.error(request, "Файл не выбран.")
        elif uploaded_file.size > MAX_UPLOAD_SIZE:
            size_mb = uploaded_file.size / (1024 * 1024)
            messages.error(
                request,
                f"Размер файла ({size_mb:.2f} МБ) превышает допустимый лимит "
                f"{MAX_UPLOAD_SIZE / (1024 * 1024):.0f} МБ."
            )
        else:
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            messages.success(request, f"Файл '{filename}' успешно загружен.")
            request.session['last_uploaded_url'] = fs.url(filename)

        return redirect(request.path)

    context = {}
    return render(request, "requestdataapp/file-upload.html", context)

