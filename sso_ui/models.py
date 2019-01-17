from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_cas_ng.signals import cas_user_authenticated

import json


LANG = settings.SSO_UI_ORG_DETAIL_LANG
ORG_CODE = {}
with open(settings.SSO_UI_ORG_DETAIL_FILE_PATH, 'r') as ORG_CODE_FILE:
    ORG_CODE.update(json.load(ORG_CODE_FILE))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    org_code = models.CharField('kode organisasi', max_length=11, blank=True)
    role = models.CharField('peran pengguna', max_length=128, blank=True)
    npm = models.CharField('Nomor Pokok Mahasiswa', max_length=10, blank=True)
    faculty = models.CharField('fakultas', max_length=128, blank=True)
    study_program = models.CharField('program studi', max_length=128, blank=True)
    educational_program = models.CharField('program pendidikan', max_length=128, blank=True)

    class Meta:
        verbose_name = 'profil'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(cas_user_authenticated)
def save_user_profile(sender, user, created, attributes, **kwargs):
    try:
        user.profile.save()
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)
    else:
        profile = user.profile
    profile.role = attributes['peran_user']
    profile.npm = attributes['npm']
    if profile.role == 'mahasiswa':
        user.email = f'{user.username}@ui.ac.id'

    full_name = attributes['nama']
    i = full_name.rfind(' ')
    user.first_name, user.last_name = full_name[:i], full_name[i + 1:]

    org_code = attributes['kd_org']
    record = ORG_CODE[LANG][org_code]
    profile.org_code = org_code
    profile.faculty = record['faculty']
    profile.study_program = record['study_program']
    profile.educational_program = record['educational_program']

    user.profile.save()
    user.save()
