from pydantic import BaseModel, Field, StrictStr


class ChangePasswordModel(BaseModel):
    login: StrictStr
    token: StrictStr
    old_password: StrictStr = Field(title='oldPassword', alias='oldPassword')
    new_password: StrictStr = Field(title='newPassword', alias='newPassword')
