from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from apps.usuario.views import Register, ListGroupsAvailable, UpdateEstadoEmpleado, listUsuarios, update_colaboradores, change_password, obtener_firma_digital, controller_firma_digital

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path("registra_usuarios/", Register.as_view(), name="register_user"),
    path("list_groups_available/", ListGroupsAvailable.as_view(), name="list_groups"),
    path("update_estado_empleado/<int:pk>/", UpdateEstadoEmpleado.as_view(), name="update_estado_empleado"),
    path("list_usuarios/", listUsuarios.as_view(), name="list_usuarios"),
    path("update_empleado/<int:pk>/", update_colaboradores, name="update_empleado"),
    path("update_contrasenia/<int:pk>/", change_password, name="change_password"),
    path("obtener_firma_digital/", obtener_firma_digital, name="obtener_firma_digital"),
    path("controlador_firma_digital/", controller_firma_digital, name="controlador_firma_digital"),
]