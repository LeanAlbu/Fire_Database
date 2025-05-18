--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8 (Ubuntu 16.8-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.8 (Ubuntu 16.8-0ubuntu0.24.04.1)

-- Started on 2025-05-18 18:50:17 -03

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
-- TOC entry 5 (class 2615 OID 24655)
-- Name: bd_queimadas; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA bd_queimadas;


ALTER SCHEMA bd_queimadas OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 216 (class 1259 OID 16414)
-- Name: focos_de_queimada; Type: TABLE; Schema: bd_queimadas; Owner: postgres
--

CREATE TABLE bd_queimadas.focos_de_queimada (
    id_queimada integer NOT NULL,
    data_hora timestamp(0) without time zone NOT NULL,
    latitude numeric(9,3) NOT NULL,
    longitude numeric(9,3) NOT NULL,
    potencia_rad real NOT NULL,
    id_municipio integer,
    CONSTRAINT id_municipio_positivo CHECK ((id_municipio > 0))
);


ALTER TABLE bd_queimadas.focos_de_queimada OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16413)
-- Name: focos_de_queimada_id_queimada_seq; Type: SEQUENCE; Schema: bd_queimadas; Owner: postgres
--

CREATE SEQUENCE bd_queimadas.focos_de_queimada_id_queimada_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE bd_queimadas.focos_de_queimada_id_queimada_seq OWNER TO postgres;

--
-- TOC entry 3489 (class 0 OID 0)
-- Dependencies: 215
-- Name: focos_de_queimada_id_queimada_seq; Type: SEQUENCE OWNED BY; Schema: bd_queimadas; Owner: postgres
--

ALTER SEQUENCE bd_queimadas.focos_de_queimada_id_queimada_seq OWNED BY bd_queimadas.focos_de_queimada.id_queimada;


--
-- TOC entry 218 (class 1259 OID 16436)
-- Name: municipios; Type: TABLE; Schema: bd_queimadas; Owner: postgres
--

CREATE TABLE bd_queimadas.municipios (
    nome_municipio character varying(50) NOT NULL,
    area_km2 numeric(6,2) NOT NULL,
    populacao integer NOT NULL,
    id_regiao integer NOT NULL,
    id_municipio integer NOT NULL,
    CONSTRAINT ck_area_positiva CHECK ((area_km2 > (0)::numeric))
);


ALTER TABLE bd_queimadas.municipios OWNER TO postgres;

--
-- TOC entry 3490 (class 0 OID 0)
-- Dependencies: 218
-- Name: CONSTRAINT ck_area_positiva ON municipios; Type: COMMENT; Schema: bd_queimadas; Owner: postgres
--

COMMENT ON CONSTRAINT ck_area_positiva ON bd_queimadas.municipios IS 'Verifica se a área fornecidade é positiva';


--
-- TOC entry 223 (class 1259 OID 24669)
-- Name: municipios_id_municipio_seq; Type: SEQUENCE; Schema: bd_queimadas; Owner: postgres
--

CREATE SEQUENCE bd_queimadas.municipios_id_municipio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE bd_queimadas.municipios_id_municipio_seq OWNER TO postgres;

--
-- TOC entry 3491 (class 0 OID 0)
-- Dependencies: 223
-- Name: municipios_id_municipio_seq; Type: SEQUENCE OWNED BY; Schema: bd_queimadas; Owner: postgres
--

ALTER SEQUENCE bd_queimadas.municipios_id_municipio_seq OWNED BY bd_queimadas.municipios.id_municipio;


--
-- TOC entry 217 (class 1259 OID 16422)
-- Name: regioes_imediatas; Type: TABLE; Schema: bd_queimadas; Owner: postgres
--

CREATE TABLE bd_queimadas.regioes_imediatas (
    bioma character varying(30) NOT NULL,
    nome_regiao character varying(50) NOT NULL,
    clima_regiao character varying(50) NOT NULL,
    id_regiao integer NOT NULL
);


ALTER TABLE bd_queimadas.regioes_imediatas OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 24656)
-- Name: regioes_imediatas_id_regiao_seq; Type: SEQUENCE; Schema: bd_queimadas; Owner: postgres
--

CREATE SEQUENCE bd_queimadas.regioes_imediatas_id_regiao_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE bd_queimadas.regioes_imediatas_id_regiao_seq OWNER TO postgres;

--
-- TOC entry 3492 (class 0 OID 0)
-- Dependencies: 222
-- Name: regioes_imediatas_id_regiao_seq; Type: SEQUENCE OWNED BY; Schema: bd_queimadas; Owner: postgres
--

ALTER SEQUENCE bd_queimadas.regioes_imediatas_id_regiao_seq OWNED BY bd_queimadas.regioes_imediatas.id_regiao;


--
-- TOC entry 221 (class 1259 OID 24638)
-- Name: satelite_queimada; Type: TABLE; Schema: bd_queimadas; Owner: postgres
--

CREATE TABLE bd_queimadas.satelite_queimada (
    id_queimada integer NOT NULL,
    id_satelite integer NOT NULL
);


ALTER TABLE bd_queimadas.satelite_queimada OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 24597)
-- Name: satelites; Type: TABLE; Schema: bd_queimadas; Owner: postgres
--

CREATE TABLE bd_queimadas.satelites (
    id_satelite integer NOT NULL,
    nome_satelite character varying(30) NOT NULL
);


ALTER TABLE bd_queimadas.satelites OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 24596)
-- Name: satelites_id_satelite_seq; Type: SEQUENCE; Schema: bd_queimadas; Owner: postgres
--

CREATE SEQUENCE bd_queimadas.satelites_id_satelite_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE bd_queimadas.satelites_id_satelite_seq OWNER TO postgres;

--
-- TOC entry 3493 (class 0 OID 0)
-- Dependencies: 219
-- Name: satelites_id_satelite_seq; Type: SEQUENCE OWNED BY; Schema: bd_queimadas; Owner: postgres
--

ALTER SEQUENCE bd_queimadas.satelites_id_satelite_seq OWNED BY bd_queimadas.satelites.id_satelite;


--
-- TOC entry 3304 (class 2604 OID 16417)
-- Name: focos_de_queimada id_queimada; Type: DEFAULT; Schema: bd_queimadas; Owner: postgres
--

ALTER TABLE ONLY bd_queimadas.focos_de_queimada ALTER COLUMN id_queimada SET DEFAULT nextval('bd_queimadas.focos_de_queimada_id_queimada_seq'::regclass);


--
-- TOC entry 3306 (class 2604 OID 24670)
-- Name: municipios id_municipio; Type: DEFAULT; Schema: bd_queimadas; Owner: postgres
--

ALTER TABLE ONLY bd_queimadas.municipios ALTER COLUMN id_municipio SET DEFAULT nextval('bd_queimadas.municipios_id_municipio_seq'::regclass);


--
-- TOC entry 3305 (class 2604 OID 24657)
-- Name: regioes_imediatas id_regiao; Type: DEFAULT; Schema: bd_queimadas; Owner: postgres
--

ALTER TABLE ONLY bd_queimadas.regioes_imediatas ALTER COLUMN id_regiao SET DEFAULT nextval('bd_queimadas.regioes_imediatas_id_regiao_seq'::regclass);


--
-- TOC entry 3307 (class 2604 OID 24600)
-- Name: satelites id_satelite; Type: DEFAULT; Schema: bd_queimadas; Owner: postgres
--

ALTER TABLE ONLY bd_queimadas.satelites ALTER COLUMN id_satelite SET DEFAULT nextval('bd_queimadas.satelites_id_satelite_seq'::regclass);


--
-- TOC entry 3476 (class 0 OID 16414)
-- Dependencies: 216
-- Data for Name: focos_de_queimada; Type: TABLE DATA; Schema: bd_queimadas; Owner: postgres
--

COPY bd_queimadas.focos_de_queimada (id_queimada, data_hora, latitude, longitude, potencia_rad, id_municipio) FROM stdin;
1	2025-05-18 14:30:00	-3524.440	4355.000	4.3	1
\.


--
-- TOC entry 3478 (class 0 OID 16436)
-- Dependencies: 218
-- Data for Name: municipios; Type: TABLE DATA; Schema: bd_queimadas; Owner: postgres
--

COPY bd_queimadas.municipios (nome_municipio, area_km2, populacao, id_regiao, id_municipio) FROM stdin;
Palmas	2000.00	300000	1	1
\.


--
-- TOC entry 3477 (class 0 OID 16422)
-- Dependencies: 217
-- Data for Name: regioes_imediatas; Type: TABLE DATA; Schema: bd_queimadas; Owner: postgres
--

COPY bd_queimadas.regioes_imediatas (bioma, nome_regiao, clima_regiao, id_regiao) FROM stdin;
Caatinga	Palmas	Inferno	1
\.


--
-- TOC entry 3481 (class 0 OID 24638)
-- Dependencies: 221
-- Data for Name: satelite_queimada; Type: TABLE DATA; Schema: bd_queimadas; Owner: postgres
--

COPY bd_queimadas.satelite_queimada (id_queimada, id_satelite) FROM stdin;
\.


--
-- TOC entry 3480 (class 0 OID 24597)
-- Dependencies: 220
-- Data for Name: satelites; Type: TABLE DATA; Schema: bd_queimadas; Owner: postgres
--

COPY bd_queimadas.satelites (id_satelite, nome_satelite) FROM stdin;
\.


--
-- TOC entry 3494 (class 0 OID 0)
-- Dependencies: 215
-- Name: focos_de_queimada_id_queimada_seq; Type: SEQUENCE SET; Schema: bd_queimadas; Owner: postgres
--

SELECT pg_catalog.setval('bd_queimadas.focos_de_queimada_id_queimada_seq', 1, true);


--
-- TOC entry 3495 (class 0 OID 0)
-- Dependencies: 223
-- Name: municipios_id_municipio_seq; Type: SEQUENCE SET; Schema: bd_queimadas; Owner: postgres
--

SELECT pg_catalog.setval('bd_queimadas.municipios_id_municipio_seq', 1, true);


--
-- TOC entry 3496 (class 0 OID 0)
-- Dependencies: 222
-- Name: regioes_imediatas_id_regiao_seq; Type: SEQUENCE SET; Schema: bd_queimadas; Owner: postgres
--

SELECT pg_catalog.setval('bd_queimadas.regioes_imediatas_id_regiao_seq', 1, true);


--
-- TOC entry 3497 (class 0 OID 0)
-- Dependencies: 219
-- Name: satelites_id_satelite_seq; Type: SEQUENCE SET; Schema: bd_queimadas; Owner: postgres
--

SELECT pg_catalog.setval('bd_queimadas.satelites_id_satelite_seq', 1, false);


--
-- TOC entry 3311 (class 2606 OID 16419)
-- Name: focos_de_queimada focos_de_queimada_pkey; Type: CONSTRAINT; Schema: bd_queimadas; Owner: postgres
--

ALTER TABLE ONLY bd_queimadas.focos_de_queimada
    ADD CONSTRAINT focos_de_queimada_pkey PRIMARY KEY (id_queimada);


--
-- TOC entry 3327 (class 2606 OID 24642)
-- Name: satelite_queimada pk_ligacao_queimada_satelite; Type: CONSTRAINT; Schema: bd_queimadas; Owner: postgres
--

ALTER TABLE ONLY bd_queimadas.satelite_queimada
    ADD CONSTRAINT pk_ligacao_queimada_satelite PRIMARY KEY (id_queimada, id_satelite);


--
-- TOC entry 3319 (class 2606 OID 24676)
-- Name: municipios pk_municipio; Type: CONSTRAINT; Schema: bd_queimadas; Owner: postgres
--

ALTER TABLE ONLY bd_queimadas.municipios
    ADD CONSTRAINT pk_municipio PRIMARY KEY (id_municipio);


--
-- TOC entry 3315 (class 2606 OID 24663)
-- Name: regioes_imediatas pk_regiao; Type: CONSTRAINT; Schema: bd_queimadas; Owner: postgres
--

ALTER TABLE ONLY bd_queimadas.regioes_imediatas
    ADD CONSTRAINT pk_regiao PRIMARY KEY (id_regiao);


--
-- TOC entry 3323 (class 2606 OID 24602)
-- Name: satelites pk_satelite; Type: CONSTRAINT; Schema: bd_queimadas; Owner: postgres
--

ALTER TABLE ONLY bd_queimadas.satelites
    ADD CONSTRAINT pk_satelite PRIMARY KEY (id_satelite);


--
-- TOC entry 3313 (class 2606 OID 16421)
-- Name: focos_de_queimada unq_foco_queimada; Type: CONSTRAINT; Schema: bd_queimadas; Owner: postgres
--

ALTER TABLE ONLY bd_queimadas.focos_de_queimada
    ADD CONSTRAINT unq_foco_queimada UNIQUE (data_hora, latitude, longitude);


--
-- TOC entry 3321 (class 2606 OID 24632)
-- Name: municipios unq_nome_municipio; Type: CONSTRAINT; Schema: bd_queimadas; Owner: postgres
--

ALTER TABLE ONLY bd_queimadas.municipios
    ADD CONSTRAINT unq_nome_municipio UNIQUE (nome_municipio);


--
-- TOC entry 3325 (class 2606 OID 24604)
-- Name: satelites unq_nome_satelite; Type: CONSTRAINT; Schema: bd_queimadas; Owner: postgres
--

ALTER TABLE ONLY bd_queimadas.satelites
    ADD CONSTRAINT unq_nome_satelite UNIQUE (nome_satelite);


--
-- TOC entry 3317 (class 2606 OID 24613)
-- Name: regioes_imediatas unq_regiao; Type: CONSTRAINT; Schema: bd_queimadas; Owner: postgres
--

ALTER TABLE ONLY bd_queimadas.regioes_imediatas
    ADD CONSTRAINT unq_regiao UNIQUE (nome_regiao);


--
-- TOC entry 3330 (class 2606 OID 24643)
-- Name: satelite_queimada fk_id_queimada; Type: FK CONSTRAINT; Schema: bd_queimadas; Owner: postgres
--

ALTER TABLE ONLY bd_queimadas.satelite_queimada
    ADD CONSTRAINT fk_id_queimada FOREIGN KEY (id_queimada) REFERENCES bd_queimadas.focos_de_queimada(id_queimada);


--
-- TOC entry 3331 (class 2606 OID 24648)
-- Name: satelite_queimada fk_id_satelite; Type: FK CONSTRAINT; Schema: bd_queimadas; Owner: postgres
--

ALTER TABLE ONLY bd_queimadas.satelite_queimada
    ADD CONSTRAINT fk_id_satelite FOREIGN KEY (id_satelite) REFERENCES bd_queimadas.satelites(id_satelite);


--
-- TOC entry 3328 (class 2606 OID 24677)
-- Name: focos_de_queimada fk_municipio; Type: FK CONSTRAINT; Schema: bd_queimadas; Owner: postgres
--

ALTER TABLE ONLY bd_queimadas.focos_de_queimada
    ADD CONSTRAINT fk_municipio FOREIGN KEY (id_municipio) REFERENCES bd_queimadas.municipios(id_municipio) NOT VALID;


--
-- TOC entry 3498 (class 0 OID 0)
-- Dependencies: 3328
-- Name: CONSTRAINT fk_municipio ON focos_de_queimada; Type: COMMENT; Schema: bd_queimadas; Owner: postgres
--

COMMENT ON CONSTRAINT fk_municipio ON bd_queimadas.focos_de_queimada IS 'Chave estrangeira que relaciona as tabelas focos_de_queimada e municipios';


--
-- TOC entry 3329 (class 2606 OID 24664)
-- Name: municipios fk_regiao; Type: FK CONSTRAINT; Schema: bd_queimadas; Owner: postgres
--

ALTER TABLE ONLY bd_queimadas.municipios
    ADD CONSTRAINT fk_regiao FOREIGN KEY (id_regiao) REFERENCES bd_queimadas.regioes_imediatas(id_regiao) NOT VALID;


--
-- TOC entry 3499 (class 0 OID 0)
-- Dependencies: 3329
-- Name: CONSTRAINT fk_regiao ON municipios; Type: COMMENT; Schema: bd_queimadas; Owner: postgres
--

COMMENT ON CONSTRAINT fk_regiao ON bd_queimadas.municipios IS 'Chave estrangeira que relaciona as tabelas municipio e regioes_imediatas';


-- Completed on 2025-05-18 18:50:18 -03

--
-- PostgreSQL database dump complete
--

