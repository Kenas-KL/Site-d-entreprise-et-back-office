
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import CharField, BooleanField, DateTimeField
from django.urls import reverse
from ckeditor.fields import RichTextField


# Create your models here.

class MyUserManager(BaseUserManager):

    def create_user(self, username , password=None):
        if not username:
            raise ValueError("Vous devez entrer le nom utilisateur.")
        username = self.model.normalize_username(username)

        user = self.model(
            username = username
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username=username, password=password)
        user.is_staff = True
        user.is_admin = True
        user.is_allowed = True
        user.save()
        return user




class CustomUser(AbstractBaseUser):
    username = CharField(max_length=255, unique=True, blank=False, verbose_name="Nom utilisateur")
    is_staff = BooleanField(default=False, verbose_name="Statut d'équipe(Super Utilisateur)")
    is_admin = BooleanField(default=False, verbose_name="Administrateur")
    is_agent = BooleanField(default=False, verbose_name="Agent")
    is_student = BooleanField(default=False, verbose_name="Etudiant")
    is_allowed = BooleanField(default=False, verbose_name="Autorisé")
    level = models.IntegerField(default=0, verbose_name="Niveau")
    domain = models.CharField(max_length=30, choices=[
        ("informatique", "Informatique (Basic)"),
        ("telecommunication", "Télécommunication"),
        ("reseau_informatique", "Réseau informatique"),
        ("administration_reseau", "Administration réseau"),
        ("technologie_vsat", "Technologie VSAT"),
        ("programmation_informatique", "Programmation informatique"),
    ], verbose_name="Orientation")

    USERNAME_FIELD = "username"
    objects = MyUserManager()


    def has_perm(self,perm, obj=None): return True

    def has_module_perms(self,app_label): return True

    def get_absolute_url(self): return reverse("blog:list_users_admin")

    class Meta:
        verbose_name = "Utilisateur"

        
class Document(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name="Titre")
    book_file = models.FileField(upload_to="file_pdf/", null=True, verbose_name="Fichier PDF")
    domain = models.CharField( max_length=30, choices=[
        ("informatique","Informatique (Basic)"),
        ("telecommunication","Télécommunication"),
        ("reseau_informatique","Réseau informatique"),
        ("administration_reseau","Administration réseau"),
        ("technologie_vsat","Technologie VSAT"),
        ("programmation_informatique","Programmation informatique"),
    ])
    level = models.IntegerField(verbose_name="Niveau")
    description = models.TextField(unique=True, blank=True, verbose_name="Déscription")

    def __str__(self): return self.title


class BlogPost(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name="Title")
    content = RichTextField()
    our_intervention = BooleanField(default=False, verbose_name="Categorie intervention de l'entreprise")
    published = models.BooleanField(default=False, verbose_name="Publié")
    thumbnail = models.ImageField(blank=True, upload_to='blog_imgs/', null=True, verbose_name="Image")

    class Meta:
        verbose_name="Article_blog"

    def __str__(self): return self.title

    def get_absolute_url(self): return reverse("blog:home")


class Comment(models.Model):
    blog = models.ForeignKey(BlogPost, on_delete= models.SET_NULL, null=True, related_name='commentaires')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    anonymous = models.CharField(max_length=15, null=True, blank=True)
    content = models.TextField(verbose_name="Commentaire")
    created_at = DateTimeField(auto_now=True)

    def __str__(self): return f"Commentaire de {self.user} sur l'Article(BlogPost) {self.blog}."

    class Meta:
        verbose_name = "Commentaire"

class Task(models.Model):
    title = models.CharField(max_length=150, verbose_name="Projet(Tache)")
    responsable = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    date_de_debut = models.DateField()
    date_de_fin = models.DateField(blank=True, null=True)
    priorite = models.CharField(max_length=20, choices=[
        ('absolue', 'Absolue'),
        ('haute', 'Haute'),
        ('Moyenne', 'Moyenne'),
        ('basse', 'Basse'),
    ])
    statut = models.CharField(max_length=20, choices=[
        ('non debute', 'Non debuté'),
        ('en cours', 'En cours'),
        ('termine', 'Terminé')
    ])
    avancement = models.IntegerField(default=0)
    commentaires = models.TextField()

    class Meta:
        ordering = ['-date_de_debut']
        verbose_name = "Tache"


    def __str__(self): return self.title

    def get_absolute_url(self): return reverse("blog:task_view")
