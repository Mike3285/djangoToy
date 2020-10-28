from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.conf import settings
from django.db import models
from django.contrib import admin


class CustomModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = self.model.all_objects
        # The below is copied from the base implementation in BaseModelAdmin to prevent other changes in behavior
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def delete_model(self, request, obj):
        obj.hard_delete()


class SoftDeletionQuerySet(models.QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class CustomModelManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(CustomModelManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class MyCustomModel(models.Model):
    last_updated = models.DateTimeField(auto_now=True, editable=False,null=True, verbose_name=_('Ultima modifica'), help_text=_('Data e ora dell\'ultima modifica'))
    created = models.DateTimeField(auto_now_add=True, editable=False,null=True, verbose_name=_('Creato'), help_text=_('Data e ora di creazione'))
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_%(class)ss', on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('proprietario'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_%(class)ss', on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('autore'))
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='lastedited_%(class)ss', on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('ultima modifica di'))
    deleter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='has_deleted_%(class)ss', on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('eliminato da'))
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = CustomModelManager()
    all_objects = CustomModelManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(MyCustomModel, self).delete()


class MyCreateView(CreateView):
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.editor = self.request.user
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_message(self):
        success_message = _(f"Oggetto <strong>{self.object}</strong> creato con successo!")
        return success_message


class MyUpdateView(UpdateView):
    def form_valid(self, form):
        form.instance.editor = self.request.user
        return super().form_valid(form)

    def get_success_message(self):
        success_message = _(f"Oggetto <strong>{self.object}</strong> aggiornato con successo!")
        return success_message


class MyDeleteView(DeleteView):
    def get_object(self, *args, **kwargs):
        obj = super(MyDeleteView, self).get_object(*args, **kwargs)
        if self.request.user == obj.owner or self.request.user.is_superuser == obj.owner:
            return obj
        else:
            raise PermissionDenied()

    def delete(self, request, *args, **kwargs):
        obj = super(MyDeleteView, self).get_object()
        obj.deleter = self.request.user
        obj.save()
        return super(MyDeleteView, self).delete(request, *args, **kwargs)


class MyListView(ListView):
    def get_queryset(self):
        if not self.request.user.is_superuser:
            return self.model.objects.filter(owner=self.request.user).select_related('owner')
        else:
            return self.model.objects.all().select_related('owner')


class MyDetailView(LoginRequiredMixin, DetailView):
    def get_object(self, *args, **kwargs):
        obj = super(MyDetailView, self).get_object(*args, **kwargs)
        if self.request.user == obj.owner or self.request.user.is_superuser:
            return obj
        else:
            raise PermissionDenied()
