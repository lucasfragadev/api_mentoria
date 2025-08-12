import logging 
from fastapi import FastAPI, status, HTTPException
from typing import List # Vamos precisar de um Lista

from schemas import Mentor, MentorCreate # Importação a partir do schemas.py

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = FastAPI() ## Criou uma instância do FastAPI / Criou um objeto

## Um Mock (mock é uma forma de testar a aplicação com exemplos práticos // Tema: testes)
db_mentors = [
   Mentor(id=1, name='João Velloso', email='joaovelosso.dev@gmail.com', skills=['Python', 'Algorithm', 'Rust'], active=True), 
   Mentor(id=2, name='Rafaela Mattos', email='rafaprogramador@gmail.com', skills=['Java', 'SpringBoot', 'SQL'], active=True),
   Mentor(id=3, name='Pedro', email='pedrinvelosso.dev@gmail.com', skills=['Java', 'COBOL', 'Compilers'], active=False)
]

# Rota de Status
@app.get("/health") # O @app.get e o decorator // O que ta entre parenteses e o path // path = url = "/health"
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

# Endpoint: rota para BUSCAR um mentor especifico pelo ID
@app.get("/mentors/{mentor_id}", response_model=Mentor)
def get_mentor(mentor_id: int):
   """
   Busca e retorna um único mentor cadastrado
   """
   for mentor in db_mentors:
      if mentor.id == mentor_id:
         return mentor

   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mentor Not Found")

# Enpoint: rota para ATUALIZAR os dados de um mentor no banco de dados   
@app.put("/mentors/{mentor_id}", response_model=Mentor, status_code=status.HTTP_200_OK)
def update_mentor(mentor_id: int, mentor_data: MentorCreate):
   
   for index, mentor in enumerate(db_mentors):
      if mentor.id == mentor_id:
         updated_mentor = Mentor(id=mentor_id, **mentor_data.model_dump())
         db_mentors[index] = updated_mentor
         return updated_mentor

   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mentor Not Found")

# Enpoint: rota para EXCLUIR um mentor (Exclusão física)
@app.delete("/mentors/{mentor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mentor(mentor_id: int):
   """
   Deleta um mentor do sistema pelo Id
   """  
   logging.info(f"Recebida a requisicao para deletar o mentor com ID {mentor_id}")
   
   mentor_to_delete = None
   for mentor in db_mentors:
      if mentor.id == mentor_id:
         mentor_to_delete = mentor
         break
   
   if not mentor_to_delete:
      logging.warning(f"Tentativa de deletar mentor com ID {mentor_id}, mas ele não foi encontrado")
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mentor Not Found")
   
   db_mentors.remove(mentor_to_delete)
   
   logging.info(f"Mentor com ID {mentor_id} ({mentor_to_delete.name}) foi deletado com sucesso.")
   
   return None