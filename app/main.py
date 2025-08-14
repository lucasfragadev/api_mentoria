import logging 
from fastapi import FastAPI, status, HTTPException, Depends
from typing import List # Vamos precisar de um Lista

from app.schemas import Mentor, MentorCreate # Importação a partir do schemas.py
from app.database import engine, SessionLocal
import app.models as models
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = FastAPI() ## Criou uma instância do FastAPI / Criou um objeto

def get_db():
   db = SessionLocal() # Abrir sessão
   try: 
      yield db # Entregar para a rota usar
   finally: 
      db.close() # Garante o fechamento
    
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
@app.post("/mentors", response_model=schemas.Mentor, status_code=status.HTTP_201_CREATED)
def create_mentor(mentor: schemas.MentorCreate, db: Session = Depends(get_db)):
   
   skills_str = ",".join(mentor.skills)
   db_mentor = models.Mentor(**mentor.model_dump(exclude={'skills'}), skills=skills_str)
   db.add(db_mentor)
   db.commit()
   db.refresh(db_mentor)
   return db_mentor

@app.post("/mentors-manual", response_model=schemas.Mentor, status_code=status.HTTP_201_CREATED)
def create_mentor(mentor: schemas.MentorCreate):
      
   db = SessionLocal()
   try:
      skills_str = ",".join(mentor.skills)
      db_mentor = models.Mentor(**mentor.model_dump(exclude={'skills'}), skills=skills_str)
      db.add(db_mentor)
      db.commit()
      db.refresh(db_mentor)
      return db_mentor
   except Exception as e:
      db.rollback()
      raise HTTPException(status_code=500, detail='erro ao criar mentor / interno')
   finally:
     db.close()
   
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