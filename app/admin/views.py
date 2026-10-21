from sqladmin import ModelView
from wtforms import PasswordField, SelectField

from app.core.database.models import Usuario
from app.schemas.usuarios import UserRole
from app.core.security.password import hash_senha


class UsuarioAdmin(ModelView, model=Usuario):
    name = "Usuário"
    name_plural = "Usuários"
    icon = "fa-solid fa-user"

    column_list = [Usuario.id, Usuario.nome, Usuario.usuario, Usuario.role]
    column_searchable_list = [Usuario.nome, Usuario.usuario]

    form_columns = [Usuario.nome, Usuario.usuario, Usuario.role]
    form_overrides = {"role": SelectField}
    form_args = {
        "role": {
            "choices": [(role.value, role.value) for role in UserRole],
        }
    }
    column_details_exclude_list = [Usuario.senha]

    async def scaffold_form(self, *args, **kwargs):
        form_class = await super().scaffold_form(*args, **kwargs)
        form_class.nova_senha = PasswordField("Senha")
        return form_class

    async def on_model_change(self, data, model, is_created, request):
        nova_senha = data.get("nova_senha")
        if is_created and not nova_senha:
            raise ValueError("A senha é obrigatória ao criar um usuário.")
        if nova_senha:  # na edição, vazio = mantém a senha atual
            model.senha = hash_senha(nova_senha)