from pydantic import BaseModel, EmailStr


class Email(BaseModel):
    to: EmailStr
    subject: str
    message: str

