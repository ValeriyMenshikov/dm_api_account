from pydantic import BaseModel, Field, StrictStr, ConstrainedDate
from typing import List, Optional
from enum import Enum


class Roles(Enum):
    GUEST = 'Guest'
    PLAYER = 'Player'
    ADMINISTRATOR = 'Administrator'
    NANNY_MODERATOR = 'NannyModerator'
    REGULAR_MODERATOR = 'RegularModerator'
    SENIOR_MODERATOR = 'SeniorModerator'


class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int


class User(BaseModel):
    login: StrictStr
    roles: List[Roles]
    medium_picture_url: Optional[StrictStr] = Field(alias='mediumPictureUrl')
    small_picture_url: Optional[StrictStr] = Field(alias='smallPictureUrl')
    status: Optional[StrictStr]
    rating: Rating
    online: Optional[ConstrainedDate]
    name: StrictStr = Field(default='TestUser')
    location: Optional[StrictStr]
    registration: Optional[ConstrainedDate]


class UserEnvelopeModel(BaseModel):
    resource: User
    metadata: Optional[StrictStr]