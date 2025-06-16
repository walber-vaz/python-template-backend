from app.exception import Conflict, NotAuthenticated


class UserEmailAlreadyExists(Conflict):
    DETAIL = 'E-mail já cadastrado.'


class UserPhoneAlreadyExists(Conflict):
    DETAIL = 'Telefone já cadastrado.'


class UserNotAuthenticated(NotAuthenticated):
    DETAIL = 'Senha ou e-mail incorretos.'
