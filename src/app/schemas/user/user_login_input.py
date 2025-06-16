from pydantic import BaseModel, EmailStr


class UserLoginInput(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
