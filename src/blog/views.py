from django.contrib.auth import logout, login
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import BlogPost, Task, CustomUser, Document, Comment
from .forms import TaskForm, TaskForm_, FormulaireInscription, FormComment


def index(request):
    return render(request, 'blog/index.html')

class BlogHome(ListView):
    queryset = BlogPost.objects.all().filter(published=True, our_intervention=False)
    context_object_name = "blogs"

def contact(request):
    return render(request, "blog/contact.html")

class BlogDetail(DetailView):
    model = BlogPost
    context_object_name = "blog"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()
        context['commentaires'] = blog.commentaires.all().order_by('-pk')
        context['comments_quantity'] = blog.commentaires.all().count()
        context['form'] = FormComment()
        return context

    def post(self, request, *args, **kwargs):
        blog = self.get_object()
        form = FormComment(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            if request.user.is_authenticated:
                comment.user = request.user
            else:
                comment.anonymous = "Inconnu"
            comment.save()
            return redirect('blog:blog_detail', pk=blog.pk)


class TaskCreate(CreateView):
    model = Task
    form_class = TaskForm

    def form_valid(self, form):
        form.instance.responsable = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("blog:login")
        if not request.user.is_agent:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class TaskView(ListView):
    model = Task
    context_object_name = "taches"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("blog:login")
        if not request.user.is_agent:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class TaskDetail(DetailView):
    model = Task
    context_object_name = "task"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("blog:login")
        if not request.user.is_agent:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class TaskUpdate(UpdateView):
    model = Task
    context_object_name = "update_task"
    form_class = TaskForm_

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("blog:login")
        if not request.user.is_agent:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class DocumentView(ListView):
    model = Document
    context_object_name = "documents"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("blog:login")
        if not request.user.is_student:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self): return Document.objects.filter(domain=self.request.user.domain)


def done(request):
    events = BlogPost.objects.all().filter(published=True, our_intervention=True).order_by('-pk')
    comments = Comment.objects.all()
    blogs_data = [ {'event': event, 'comments_count': comments.filter(blog=event).count()} for event in events ]
    return render(request, 'blog/events_template.html', context={"events": blogs_data})


def account_created(request):
    if not request.user.is_authenticated:
        return redirect("blog:login")
    return render(request, template_name="blog/account_created.html")


class InscriptionView(View):

    def get(self, request):
        form = FormulaireInscription()
        return render(request, 'blog/signup.html', {'form': form})

    def post(self,request):
        form = FormulaireInscription(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['Mot_de_passe'])
            user.save()
            login(request,user)
            return redirect('blog:account_created')
        return render(request, 'blog/signup.html', {'form': form})


def user_to_logout(request):
    if not request.user.is_authenticated:
        return redirect("blog:login")
    return render(request, "blog/user-to-logout.html", context={"username": request.user.username})


def logout_view(request):
    logout(request)
    return redirect("blog:home")


# Views for administration =======================================================================


def administrators(request):
    if not request.user.is_authenticated:
        return redirect("blog:login")
    if request.user.is_admin:
        return render(request, 'blog/admin/admin_site.html')


class BlogCreate(CreateView):
    model = BlogPost
    fields = [
        "title", "thumbnail", "content", "our_intervention", "published",
    ]
    template_name = "blog/admin/blogpost_form.html"

    success_url = reverse_lazy("blog:list_blog_admin")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("blog:login")
        if not request.user.is_admin:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class BlogUpdate(UpdateView):
    model = BlogPost
    template_name = "blog/admin/update_blog.html"
    context_object_name = "blog"
    fields = [
        "title", "thumbnail", "content", "our_intervention","published",
    ]

    success_url = reverse_lazy("blog:list_blog_admin")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("blog:login")
        if not request.user.is_admin:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class BlogAdminView(ListView):
    model = BlogPost
    context_object_name = "blogs"
    template_name = "blog/admin/bloglistadmin.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("blog:login")
        if not request.user.is_admin:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)



class BlogAdminDelete(DeleteView):
    model = BlogPost
    context_object_name = "blog"
    template_name = "blog/admin/deleteblogadmin.html"
    success_url = reverse_lazy("blog:list_blog_admin")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("blog:login")
        if not request.user.is_admin:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class DocumentsAdminView(ListView):
    model = Document
    context_object_name = "documents"
    template_name = "blog/admin/list-document-admin.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("blog:login")
        if not request.user.is_admin:
            raise Http404()
        return super().dispatch(request,*args,**kwargs)


class DocumentAdminCreate(CreateView):
    model = Document
    template_name = "blog/admin/create-document-admin.html"
    fields = [
        "title", "book_file", "domain", "level", "description"
    ]
    success_url = reverse_lazy("blog:list_admin_docs")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("blog:login")
        if not request.user.is_admin:
            raise Http404()
        return super().dispatch(request,*args,**kwargs)


class DocumentAdminUpdate(UpdateView):
    model = Document
    context_object_name = "document"
    template_name = "blog/admin/update-document-admin.html"
    fields = [
        "title", "book_file", "domain", "level", "description"
    ]
    success_url = reverse_lazy("blog:list_admin_docs")


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("blog:login")
        if not request.user.is_admin:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class DocumentAdminDelelte(DeleteView):
    model = Document
    context_object_name = "doc"
    template_name = "blog/admin/delete-document.html"
    success_url = reverse_lazy("blog:list_admin_docs")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("blog:login")
        if not request.user.is_admin:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class TaskAdminView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "blog/admin/tasklistadmin.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("blog:login")
        if not request.user.is_admin:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class TaskAdminUpdate(UpdateView):
    model = Task
    content_object_name = "task"
    template_name = "blog/admin/taskadminupdate.html"
    fields = ["title", "priorite", "responsable", "description", "commentaires", "date_de_debut", "date_de_fin",]

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("blog:login")
        if not request.user.is_admin:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class TaskAdminDelete(DeleteView):
    model = Task
    context_object_name = "Task"
    template_name = "blog/admin/taskdeleteadmin.html"
    success_url = reverse_lazy("blog:list_tasks_admin")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("blog:login")
        if not request.user.is_admin:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class UsersAdminView(ListView):
    model = CustomUser
    context_object_name = "users"
    template_name = "blog/admin/userslistadmin.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("blog:login")
        if not request.user.is_admin:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class UsersAdminUpdate(UpdateView):
    model = CustomUser
    context_object_name = "user"
    template_name = "blog/admin/updateuseradmin.html"
    fields = [
        "is_admin", "is_agent", "is_student", "is_allowed", "level", "domain"
    ]

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("blog:login")
        if not request.user.is_admin:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class UserAdminDelete(DeleteView):
    model = CustomUser
    context_object_name = "user"
    template_name = "blog/admin/deleteuseradmin.html"

    success_url = reverse_lazy("blog:list_users_admin")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("blog:login")
        if not request.user.is_admin:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)



