from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserBioForm, UploadFileForm

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
    context = {
        "form": UserBioForm(),
    }
    return render(request, "requestdataapp/user-bio-form.html", context=context)


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    MAX_UPLOAD_SIZE = 1 * 1024 * 1024

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
    else:
        form = UploadFileForm()

    if request.method == "POST" and form.is_valid():
        uploaded_file = form.cleaned_data["file"]

        if uploaded_file.size > MAX_UPLOAD_SIZE:
            size_mb = uploaded_file.size / (1024 * 1024)
            limit_mb = MAX_UPLOAD_SIZE / (1024 * 1024)
            messages.error(
                request,
                f"Размер файла ({size_mb:.2f} МБ) превышает допустимый лимит {limit_mb:.0f} МБ."
            )
        else:
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            messages.success(request, f"Файл '{filename}' успешно загружен.")
            request.session["last_uploaded_url"] = fs.url(filename)

        return redirect(request.path)

    context = {"form": form}
    return render(request, "requestdataapp/file-upload.html", context=context)

