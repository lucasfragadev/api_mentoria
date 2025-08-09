from fastapi import FastAPI, status
from typing import List # Vamos precisar de um Lista

from schemas import Mentor, MentorCreate # Importação a partir do schemas.py

app = FastAPI() ## Criou uma instância do FastAPI / Criou um objeto

## Um Mock (mock é uma forma de testar a aplicação com exemplos práticos // Tema: testes)
db_mentors = [
   Mentor(id=1, name='João Velloso', email='joaovelosso.dev@gmail.com', skills=['Python', 'Algorithm', 'Rust'], active=True), 
   Mentor(id=2, name='Rafaela Mattos', email='rafaprogramador@gmail.com', skills=['Java', 'SpringBoot', 'SQL'], active=True),
   Mentor(id=3, name='Pedro', email='pedrinvelosso.dev@gmail.com', skills=['Java', 'COBOL', 'Compilers'], active=False)
]

# Rota de Status
@app.get("/health") # O @app.get e o decorator // O que ta entre parenteses e o path // path = url = "/"
def health():
   return {"status": "OK"}

# Endpoint: rota para LISTAR os mentores
@app.get("/mentors", response_model=List[Mentor])
def get_mentors():
   """
   Retorna uma lista com todos os mentores cadastrados.
   """
   return db_mentors

# Endpoint: rota para CRIAR os mentores
@app.post("/mentors", response_model=Mentor, status_code=status.HTTP_201_CREATED)
def create_mentor(mentor: MentorCreate):
   new_id = len(db_mentors) + 1
   new_mentor = Mentor(id=new_id, **mentor.model_dump())
   db_mentors.append(new_mentor)
   return new_mentor
