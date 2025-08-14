import logging 
from fastapi import FastAPI, status, HTTPException, Depends
from typing import List # Vamos precisar de um Lista

from app.schemas import Mentor, MentorCreate # Importação a partir do schemas.py
from app.database import engine, SessionLocal
import app.models as models
from sqlalchemy.orm import Session
from app import schemas

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

# Endpoint: rota para LISTAR todos os mentores
@app.get("/mentors", response_model=List[schemas.Mentor])
def get_mentors(db: Session = Depends(get_db)):
   """
   Retorna uma lista com todos os mentores cadastrados.
   """
   mentors = db.query(models.Mentor).all()
   return mentors

# Endpoint: rota para BUSCAR um mentor especifico pelo ID
@app.get("/mentors/{mentor_id}", response_model=schemas.Mentor)
def get_mentor(mentor_id: int, db: Session = Depends(get_db)):
   """
   Busca e retorna um único mentor cadastrado no banco de dados pelo ID.
   """
   # Fazemos uma consulta, filtramos o ID e pegamoms o primeiro resultado.
   mentor = db.query(models.Mentor).filter(models.Mentor.id == mentor_id).first()
   
   # A lógica para o erro 404 continua a mesma aqui
   if mentor is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mentor Not Found")
   
   return mentor

# Endpoint: rota para CRIAR os mentores
@app.post("/mentors", response_model=schemas.Mentor, status_code=status.HTTP_201_CREATED)
def create_mentor(mentor: schemas.MentorCreate, db: Session = Depends(get_db)):
   
   skills_str = ",".join(mentor.skills)
   db_mentor = models.Mentor(**mentor.model_dump(exclude={'skills'}), skills=skills_str)
   db.add(db_mentor)
   db.commit()
   db.refresh(db_mentor)
   return db_mentor

# Enpoint: rota para ATUALIZAR os dados de um mentor no banco de dados   
@app.put("/mentors/{mentor_id}", response_model=schemas.Mentor, status_code=status.HTTP_200_OK)
def update_mentor(mentor_id: int, mentor_data: schemas.MentorCreate, db: Session = Depends(get_db)):
   """
   Atualiza as informações de um mentor existente no banco de dados.
   """
   # Vamos buscar o m entor no banco de dados
   mentor_to_update = db.query(models.Mentor).filter(models.Mentor.id == mentor_id).first()
   
   # Caso o mentor não exista, vamos retornar 404
   if not mentor_to_update:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mentor Not Found")
   
   # Pronto, agora podemos atualizar os campos do objeto encontrado com os dados que quisermos
   mentor_to_update.name = mentor_data.name
   mentor_to_update.email = mentor_data.email
   mentor_to_update.skills = ",".join(mentor_data.skills) # Aqui é necessário fazer a conversão
   mentor_to_update.active = mentor_data.active
   
   db.commit()
   db.refresh(mentor_to_update)
   
   return mentor_to_update

# Enpoint: rota para EXCLUIR um mentor (Exclusão física)
@app.delete("/mentors/{mentor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mentor(mentor_id: int, db: Session = Depends(get_db)):
   """
   Deleta um mentor do sistema pelo ID.
   """  
   logging.info(f"Recebida a requisicao para deletar o mentor com ID {mentor_id}")
   
   mentor_to_delete = db.query(models.Mentor).filter(models.Mentor.id == mentor_id).first()

   if not mentor_to_delete:
      logging.warning(f"Tentativa de deletar mentor com ID {mentor_id}, mas ele não foi encontrado")
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mentor Not Found")
   
   db.delete(mentor_to_delete)   
   db.commit()
   logging.info(f"Mentor com ID {mentor_id} ({mentor_to_delete.name}) foi deletado com sucesso.")
   
   return None