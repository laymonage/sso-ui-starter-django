# sso-ui-starter-django

## SSO UI Starter Pack for Django

*Starter pack* berupa proyek Django yang sudah dilengkapi
dengan [`django_cas_ng`][django-cas-ng] dan siap untuk dipakai
dengan [SSO UI (DEV-CAS2)][sso-ui-cas2].

Demonstrasi dapat dilihat [di sini][sso-ui-heroku].

## Cara pakai

- *Clone* repositori ini, dan masuk ke direktori hasil *clone* tersebut.
- Disarankan untuk menggunakan [`pipenv`][pipenv].

```shell
$ pip install pipenv
$ pipenv install
```

  Jika tidak ingin menggunakan `pipenv`, `pip` juga bisa digunakan.

```shell
$ pip install -r requirements.txt
```

- Jalankan `python manage.py migrate` untuk migrasi basis data.
- Jalankan `python manage.py collectstatic` untuk mengumpulkan berkas statis.
- Jalankan `python manage.py runserver` untuk menjalankan *server*.
- ???
- Profit!

Untuk lebih detail, silakan lihat dokumentasi [django-cas-ng][django-cas-ng].


[django-cas-ng]: https://github.com/mingchen/django-cas-ng
[sso-ui-cas2]: https://sso.ui.ac.id/cas2
[sso-ui-heroku]: https://sso-ui.herokuapp.com
[pipenv]: https://pypi.org/project/pipenv
