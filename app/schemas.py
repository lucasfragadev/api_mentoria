from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Any

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
    
    @field_validator('skills', mode='before')
    @classmethod
    def split_skills_string(cls, valor: Any) -> List[str]:
        if isinstance(valor, str):
            return [skill.strip() for skill in valor.split(',')]
        return valor
    class Config:
        from_attributes = True