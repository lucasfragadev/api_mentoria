from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Endereco do nosso Banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./mentoria.db"

# Motor da  conexao com o banco de dados 
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
) 

# Fabrica de sessoes para conversar com Banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cimento para criar os modelos de tabela 
Base = declarative_base() 