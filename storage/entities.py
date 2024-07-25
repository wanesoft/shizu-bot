from pydantic import BaseModel
from dataclasses import dataclass


@dataclass
class RefInfo(BaseModel):
    user_id: int
    users_from_link: list[str]
    balance_from_link: int = 0

    @classmethod
    def create(cls, user_id):
        return cls.model_construct(
            user_id = user_id,
            users_from_link = [],
            balance_from_link = 0
        )


@dataclass
class User(BaseModel):
    id: int
    nick: str
    fullname: str
    ref_id: str
    balance: int

    @classmethod
    def from_message(cls, message, ref_id, balance=5):
        return cls.model_construct(
            id = message.chat.id,
            nick = message.chat.username,
            fullname = message.chat.full_name,
            ref_id = ref_id,
            balance = balance,
        )