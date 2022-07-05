-- MySQL Script generated by MySQL Workbench
-- ter 05 jul 2022 07:57:48
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering


-- -----------------------------------------------------
-- DROP TABLES
-- -----------------------------------------------------
DROP TABLE IF EXISTS public.ESTADO;
DROP TABLE IF EXISTS public.MUNICIPIO;
DROP TABLE IF EXISTS public.RESPONSAVEL;
DROP TABLE IF EXISTS public.CIDADAO;
DROP TABLE IF EXISTS public.BENEFICIO;

-- -----------------------------------------------------
-- Table public.ESTADO
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS public.ESTADO (
  ID_ESTADO SERIAL PRIMARY KEY,
  UF CHAR(2) NOT NULL UNIQUE,
  ESTADO_NOME VARCHAR(100) NOT NULL UNIQUE
);

-- -----------------------------------------------------
-- Table public.MUNICIPIO
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS public.MUNICIPIO (
  ID_MUNICIPIO SERIAL PRIMARY KEY,
  CODIGO_IBGE VARCHAR(15) NOT NULL UNIQUE,
  MUNICIPIO_NOME VARCHAR(245) NOT NULL,
  ESTADO_ID_ESTADO INT NOT NULL,
  CONSTRAINT FK_MUNICIPIO_ESTADO
    FOREIGN KEY (ESTADO_ID_ESTADO)
    REFERENCES public.ESTADO (ID_ESTADO)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);
CREATE INDEX CODIGO_IBGE_INDEX ON public.MUNICIPIO (CODIGO_IBGE);

-- -----------------------------------------------------
-- Table public.RESPONSAVEL
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS public.RESPONSAVEL (
  ID_RESPONSAVEL SERIAL PRIMARY KEY,
  RESPONSAVEL_NOME VARCHAR(300) NULL,
  RESPONSAVEL_NIS VARCHAR(45) NULL,
);

-- -----------------------------------------------------
-- Table public.CIDADAO
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS public.CIDADAO (
  ID_CIDADAO SERIAL PRIMARY KEY,
  CIDADAO_NOME VARCHAR(300) NULL,
  NIS VARCHAR(45) NULL,
  RESPONSAVEL_ID_RESPONSAVEL INT NOT NULL,
  CONSTRAINT FK_CIDADAO_RESPONSAVEL
    FOREIGN KEY (RESPONSAVEL_ID_RESPONSAVEL)
    REFERENCES public.RESPONSAVEL (ID_RESPONSAVEL)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- -----------------------------------------------------
-- Table public.BENEFICIO
-- -----------------------------------------------------
CREATE TYPE enquadramento AS ENUM ('EXTRACAD', 'BOLSA_FAMILIA', 'CADUNICO');
CREATE TABLE IF NOT EXISTS public.BENEFICIO (
  ID_BENEFICIO SERIAL PRIMARY KEY,
  CIDADAO_ID_CIDADAO INT NOT NULL,
  MUNICIPIO_ID_MUNICIPIO INT NOT NULL,
  MES_DISPONIBILIZACAO VARCHAR(15) NOT NULL,
  ENQUADRAMENTO enquadramento NOT NULL,
  PARCELA SMALLINT(1) NOT NULL,
  OBSERVACAO VARCHAR(245) NULL,
  VALOR_BENEFICIO INT(5) NOT NULL,
  CONSTRAINT FK_LOCALIZACAO_CIDADAO
    FOREIGN KEY (CIDADAO_ID_CIDADAO)
    REFERENCES public.CIDADAO (ID_CIDADAO)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT FK_BENEFICIO_MUNICIPIO
    FOREIGN KEY (MUNICIPIO_ID_MUNICIPIO)
    REFERENCES public.MUNICIPIO (ID_MUNICIPIO)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);
