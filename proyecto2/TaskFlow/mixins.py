# TaskFlow/mixins.py

from django.contrib.auth.mixins import UserPassesTestMixin

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.rol == 'admin'  # Usa el campo rol de tu modelo