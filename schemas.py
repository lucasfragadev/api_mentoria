from pydantic import BaseModel, EmailStr 
from typing import List 

# Informações padrões para CRIAR e OBTER Mentores.
class MentorBase(BaseModel):
    name: str
    email: EmailStr ## Esse "EmailStr" contém as validações que poderiam ser feitas com um Regex // TODO: Crie um Regex, pode usar IA, mas pesquise.
    skills: List[str]
    active: bool = True

# Schema utilizado para CRIAR um novo mentor (não teremos id).
# As informações virão da classe MentorBase.
class MentorCreate(MentorBase):
    pass

# Schema utilizado para OBTER/LER as informações de um mentor (tem 'id')
# As informações virão da classe MentorBase
class Mentor(MentorBase):
    id: int