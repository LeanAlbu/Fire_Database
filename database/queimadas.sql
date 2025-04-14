--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8 (Ubuntu 16.8-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.8 (Ubuntu 16.8-0ubuntu0.24.04.1)

-- Started on 2025-04-14 10:42:17 -03

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- TOC entry 3460 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 216 (class 1259 OID 16414)
-- Name: focos_de_queimada; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.focos_de_queimada (
    id_queimada integer NOT NULL,
    data_hora timestamp(0) without time zone NOT NULL,
    latitude numeric(9,3) NOT NULL,
    longitude numeric(9,3) NOT NULL,
    potencia_rad real NOT NULL,
    id_municipio integer
);


ALTER TABLE public.focos_de_queimada OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16413)
-- Name: focos_de_queimada_id_queimada_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.focos_de_queimada_id_queimada_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.focos_de_queimada_id_queimada_seq OWNER TO postgres;

--
-- TOC entry 3461 (class 0 OID 0)
-- Dependencies: 215
-- Name: focos_de_queimada_id_queimada_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.focos_de_queimada_id_queimada_seq OWNED BY public.focos_de_queimada.id_queimada;


--
-- TOC entry 218 (class 1259 OID 16436)
-- Name: municipios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.municipios (
    id_municipio integer NOT NULL,
    nome_municipio text NOT NULL,
    area_km2 numeric(6,2) NOT NULL,
    populacao integer NOT NULL,
    codigo_regiao integer NOT NULL
);


ALTER TABLE public.municipios OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16422)
-- Name: regioes_imediatas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.regioes_imediatas (
    codigo_regiao integer NOT NULL,
    bioma text NOT NULL,
    area_km2 numeric(10,2) NOT NULL,
    nome_regiao text NOT NULL,
    clima_regiao text NOT NULL
);


ALTER TABLE public.regioes_imediatas OWNER TO postgres;

--
-- TOC entry 3293 (class 2604 OID 16417)
-- Name: focos_de_queimada id_queimada; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.focos_de_queimada ALTER COLUMN id_queimada SET DEFAULT nextval('public.focos_de_queimada_id_queimada_seq'::regclass);


--
-- TOC entry 3452 (class 0 OID 16414)
-- Dependencies: 216
-- Data for Name: focos_de_queimada; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.focos_de_queimada (id_queimada, data_hora, latitude, longitude, potencia_rad, id_municipio) FROM stdin;
\.


--
-- TOC entry 3454 (class 0 OID 16436)
-- Dependencies: 218
-- Data for Name: municipios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.municipios (id_municipio, nome_municipio, area_km2, populacao, codigo_regiao) FROM stdin;
1	Palmas	2000.00	100000	170001
\.


--
-- TOC entry 3453 (class 0 OID 16422)
-- Dependencies: 217
-- Data for Name: regioes_imediatas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.regioes_imediatas (codigo_regiao, bioma, area_km2, nome_regiao, clima_regiao) FROM stdin;
170001	Cerrado	40000.00	Palmas	Tropical de Savana
\.


--
-- TOC entry 3462 (class 0 OID 0)
-- Dependencies: 215
-- Name: focos_de_queimada_id_queimada_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.focos_de_queimada_id_queimada_seq', 5, true);


--
-- TOC entry 3295 (class 2606 OID 16419)
-- Name: focos_de_queimada focos_de_queimada_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.focos_de_queimada
    ADD CONSTRAINT focos_de_queimada_pkey PRIMARY KEY (id_queimada);


--
-- TOC entry 3303 (class 2606 OID 16442)
-- Name: municipios pk_municipio; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.municipios
    ADD CONSTRAINT pk_municipio PRIMARY KEY (id_municipio);


--
-- TOC entry 3299 (class 2606 OID 16428)
-- Name: regioes_imediatas pk_regiao; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.regioes_imediatas
    ADD CONSTRAINT pk_regiao PRIMARY KEY (codigo_regiao);


--
-- TOC entry 3297 (class 2606 OID 16421)
-- Name: focos_de_queimada unq_foco_queimada; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.focos_de_queimada
    ADD CONSTRAINT unq_foco_queimada UNIQUE (data_hora, latitude, longitude);


--
-- TOC entry 3305 (class 2606 OID 16454)
-- Name: municipios unq_nome_municipio; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.municipios
    ADD CONSTRAINT unq_nome_municipio UNIQUE (nome_municipio);


--
-- TOC entry 3301 (class 2606 OID 16430)
-- Name: regioes_imediatas unq_regiao; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.regioes_imediatas
    ADD CONSTRAINT unq_regiao UNIQUE (nome_regiao);


--
-- TOC entry 3307 (class 2606 OID 16443)
-- Name: municipios fk_municipios; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.municipios
    ADD CONSTRAINT fk_municipios FOREIGN KEY (codigo_regiao) REFERENCES public.regioes_imediatas(codigo_regiao) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 3306 (class 2606 OID 16448)
-- Name: focos_de_queimada fk_queimada; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.focos_de_queimada
    ADD CONSTRAINT fk_queimada FOREIGN KEY (id_municipio) REFERENCES public.municipios(id_municipio);


-- Completed on 2025-04-14 10:42:18 -03

--
-- PostgreSQL database dump complete
--

