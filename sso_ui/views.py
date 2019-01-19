"""SSO UI views module."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    """Render home page."""
    return render(request, "sso_ui/home.html")


@login_required(login_url='sso_ui:login')
def profile(request):
    """Render profile page."""
    context = {
        "profile": {
            "Nama lengkap": request.user.get_full_name(),
            "Nama pengguna": request.user.username,
            "Alamat surel": request.user.email,
            "Kode organisasi": request.user.profile.org_code,
            "Peran pengguna": request.user.profile.role,
            "Nomor Pokok Mahasiswa": request.user.profile.npm,
            "Fakultas": request.user.profile.faculty,
            "Jurusan": request.user.profile.study_program,
            "Program pendidikan": request.user.profile.educational_program
        }
    }
    return render(request, "sso_ui/profile.html", context)
