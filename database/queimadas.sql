PGDMP  $                    }         	   queimadas #   16.9 (Ubuntu 16.9-0ubuntu0.24.04.1) #   16.9 (Ubuntu 16.9-0ubuntu0.24.04.1) 0    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16403 	   queimadas    DATABASE     u   CREATE DATABASE queimadas WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';
    DROP DATABASE queimadas;
                postgres    false                        2615    24655    bd_queimadas    SCHEMA        CREATE SCHEMA bd_queimadas;
    DROP SCHEMA bd_queimadas;
                postgres    false            �            1259    16414    focos_de_queimada    TABLE     M  CREATE TABLE bd_queimadas.focos_de_queimada (
    id_queimada integer NOT NULL,
    data_hora timestamp(0) without time zone NOT NULL,
    latitude numeric(9,3) NOT NULL,
    longitude numeric(9,3) NOT NULL,
    potencia_rad real NOT NULL,
    id_municipio integer,
    CONSTRAINT id_municipio_positivo CHECK ((id_municipio > 0))
);
 +   DROP TABLE bd_queimadas.focos_de_queimada;
       bd_queimadas         heap    postgres    false    5            �            1259    16413 !   focos_de_queimada_id_queimada_seq    SEQUENCE     �   CREATE SEQUENCE bd_queimadas.focos_de_queimada_id_queimada_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 >   DROP SEQUENCE bd_queimadas.focos_de_queimada_id_queimada_seq;
       bd_queimadas          postgres    false    5    216            �           0    0 !   focos_de_queimada_id_queimada_seq    SEQUENCE OWNED BY     s   ALTER SEQUENCE bd_queimadas.focos_de_queimada_id_queimada_seq OWNED BY bd_queimadas.focos_de_queimada.id_queimada;
          bd_queimadas          postgres    false    215            �            1259    16436 
   municipios    TABLE       CREATE TABLE bd_queimadas.municipios (
    nome_municipio character varying(50) NOT NULL,
    area_km2 numeric(6,2) NOT NULL,
    populacao integer NOT NULL,
    id_regiao integer,
    id_municipio integer NOT NULL,
    CONSTRAINT ck_area_positiva CHECK ((area_km2 > (0)::numeric))
);
 $   DROP TABLE bd_queimadas.municipios;
       bd_queimadas         heap    postgres    false    5            �           0    0 )   CONSTRAINT ck_area_positiva ON municipios    COMMENT     t   COMMENT ON CONSTRAINT ck_area_positiva ON bd_queimadas.municipios IS 'Verifica se a área fornecidade é positiva';
          bd_queimadas          postgres    false    218            �            1259    24669    municipios_id_municipio_seq    SEQUENCE     �   CREATE SEQUENCE bd_queimadas.municipios_id_municipio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 8   DROP SEQUENCE bd_queimadas.municipios_id_municipio_seq;
       bd_queimadas          postgres    false    5    218            �           0    0    municipios_id_municipio_seq    SEQUENCE OWNED BY     g   ALTER SEQUENCE bd_queimadas.municipios_id_municipio_seq OWNED BY bd_queimadas.municipios.id_municipio;
          bd_queimadas          postgres    false    223            �            1259    16422    regioes_imediatas    TABLE     �   CREATE TABLE bd_queimadas.regioes_imediatas (
    bioma character varying(30) NOT NULL,
    nome_regiao character varying(50) NOT NULL,
    clima_regiao character varying(50) NOT NULL,
    id_regiao integer NOT NULL
);
 +   DROP TABLE bd_queimadas.regioes_imediatas;
       bd_queimadas         heap    postgres    false    5            �            1259    24656    regioes_imediatas_id_regiao_seq    SEQUENCE     �   CREATE SEQUENCE bd_queimadas.regioes_imediatas_id_regiao_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 <   DROP SEQUENCE bd_queimadas.regioes_imediatas_id_regiao_seq;
       bd_queimadas          postgres    false    217    5            �           0    0    regioes_imediatas_id_regiao_seq    SEQUENCE OWNED BY     o   ALTER SEQUENCE bd_queimadas.regioes_imediatas_id_regiao_seq OWNED BY bd_queimadas.regioes_imediatas.id_regiao;
          bd_queimadas          postgres    false    222            �            1259    24638    satelite_queimada    TABLE     t   CREATE TABLE bd_queimadas.satelite_queimada (
    id_queimada integer NOT NULL,
    id_satelite integer NOT NULL
);
 +   DROP TABLE bd_queimadas.satelite_queimada;
       bd_queimadas         heap    postgres    false    5            �            1259    24597 	   satelites    TABLE     |   CREATE TABLE bd_queimadas.satelites (
    id_satelite integer NOT NULL,
    nome_satelite character varying(30) NOT NULL
);
 #   DROP TABLE bd_queimadas.satelites;
       bd_queimadas         heap    postgres    false    5            �            1259    24596    satelites_id_satelite_seq    SEQUENCE     �   CREATE SEQUENCE bd_queimadas.satelites_id_satelite_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 6   DROP SEQUENCE bd_queimadas.satelites_id_satelite_seq;
       bd_queimadas          postgres    false    5    220            �           0    0    satelites_id_satelite_seq    SEQUENCE OWNED BY     c   ALTER SEQUENCE bd_queimadas.satelites_id_satelite_seq OWNED BY bd_queimadas.satelites.id_satelite;
          bd_queimadas          postgres    false    219            �           2604    16417    focos_de_queimada id_queimada    DEFAULT     �   ALTER TABLE ONLY bd_queimadas.focos_de_queimada ALTER COLUMN id_queimada SET DEFAULT nextval('bd_queimadas.focos_de_queimada_id_queimada_seq'::regclass);
 R   ALTER TABLE bd_queimadas.focos_de_queimada ALTER COLUMN id_queimada DROP DEFAULT;
       bd_queimadas          postgres    false    215    216    216            �           2604    24670    municipios id_municipio    DEFAULT     �   ALTER TABLE ONLY bd_queimadas.municipios ALTER COLUMN id_municipio SET DEFAULT nextval('bd_queimadas.municipios_id_municipio_seq'::regclass);
 L   ALTER TABLE bd_queimadas.municipios ALTER COLUMN id_municipio DROP DEFAULT;
       bd_queimadas          postgres    false    223    218            �           2604    24657    regioes_imediatas id_regiao    DEFAULT     �   ALTER TABLE ONLY bd_queimadas.regioes_imediatas ALTER COLUMN id_regiao SET DEFAULT nextval('bd_queimadas.regioes_imediatas_id_regiao_seq'::regclass);
 P   ALTER TABLE bd_queimadas.regioes_imediatas ALTER COLUMN id_regiao DROP DEFAULT;
       bd_queimadas          postgres    false    222    217            �           2604    24600    satelites id_satelite    DEFAULT     �   ALTER TABLE ONLY bd_queimadas.satelites ALTER COLUMN id_satelite SET DEFAULT nextval('bd_queimadas.satelites_id_satelite_seq'::regclass);
 J   ALTER TABLE bd_queimadas.satelites ALTER COLUMN id_satelite DROP DEFAULT;
       bd_queimadas          postgres    false    219    220    220            �          0    16414    focos_de_queimada 
   TABLE DATA           z   COPY bd_queimadas.focos_de_queimada (id_queimada, data_hora, latitude, longitude, potencia_rad, id_municipio) FROM stdin;
    bd_queimadas          postgres    false    216   �=       �          0    16436 
   municipios 
   TABLE DATA           h   COPY bd_queimadas.municipios (nome_municipio, area_km2, populacao, id_regiao, id_municipio) FROM stdin;
    bd_queimadas          postgres    false    218   �=       �          0    16422    regioes_imediatas 
   TABLE DATA           ^   COPY bd_queimadas.regioes_imediatas (bioma, nome_regiao, clima_regiao, id_regiao) FROM stdin;
    bd_queimadas          postgres    false    217   �=       �          0    24638    satelite_queimada 
   TABLE DATA           K   COPY bd_queimadas.satelite_queimada (id_queimada, id_satelite) FROM stdin;
    bd_queimadas          postgres    false    221   �=       �          0    24597 	   satelites 
   TABLE DATA           E   COPY bd_queimadas.satelites (id_satelite, nome_satelite) FROM stdin;
    bd_queimadas          postgres    false    220    >       �           0    0 !   focos_de_queimada_id_queimada_seq    SEQUENCE SET     U   SELECT pg_catalog.setval('bd_queimadas.focos_de_queimada_id_queimada_seq', 1, true);
          bd_queimadas          postgres    false    215            �           0    0    municipios_id_municipio_seq    SEQUENCE SET     P   SELECT pg_catalog.setval('bd_queimadas.municipios_id_municipio_seq', 1, false);
          bd_queimadas          postgres    false    223            �           0    0    regioes_imediatas_id_regiao_seq    SEQUENCE SET     T   SELECT pg_catalog.setval('bd_queimadas.regioes_imediatas_id_regiao_seq', 1, false);
          bd_queimadas          postgres    false    222            �           0    0    satelites_id_satelite_seq    SEQUENCE SET     N   SELECT pg_catalog.setval('bd_queimadas.satelites_id_satelite_seq', 1, false);
          bd_queimadas          postgres    false    219            �           2606    16419 (   focos_de_queimada focos_de_queimada_pkey 
   CONSTRAINT     u   ALTER TABLE ONLY bd_queimadas.focos_de_queimada
    ADD CONSTRAINT focos_de_queimada_pkey PRIMARY KEY (id_queimada);
 X   ALTER TABLE ONLY bd_queimadas.focos_de_queimada DROP CONSTRAINT focos_de_queimada_pkey;
       bd_queimadas            postgres    false    216            �           2606    24642 .   satelite_queimada pk_ligacao_queimada_satelite 
   CONSTRAINT     �   ALTER TABLE ONLY bd_queimadas.satelite_queimada
    ADD CONSTRAINT pk_ligacao_queimada_satelite PRIMARY KEY (id_queimada, id_satelite);
 ^   ALTER TABLE ONLY bd_queimadas.satelite_queimada DROP CONSTRAINT pk_ligacao_queimada_satelite;
       bd_queimadas            postgres    false    221    221            �           2606    24676    municipios pk_municipio 
   CONSTRAINT     e   ALTER TABLE ONLY bd_queimadas.municipios
    ADD CONSTRAINT pk_municipio PRIMARY KEY (id_municipio);
 G   ALTER TABLE ONLY bd_queimadas.municipios DROP CONSTRAINT pk_municipio;
       bd_queimadas            postgres    false    218            �           2606    24663    regioes_imediatas pk_regiao 
   CONSTRAINT     f   ALTER TABLE ONLY bd_queimadas.regioes_imediatas
    ADD CONSTRAINT pk_regiao PRIMARY KEY (id_regiao);
 K   ALTER TABLE ONLY bd_queimadas.regioes_imediatas DROP CONSTRAINT pk_regiao;
       bd_queimadas            postgres    false    217            �           2606    24602    satelites pk_satelite 
   CONSTRAINT     b   ALTER TABLE ONLY bd_queimadas.satelites
    ADD CONSTRAINT pk_satelite PRIMARY KEY (id_satelite);
 E   ALTER TABLE ONLY bd_queimadas.satelites DROP CONSTRAINT pk_satelite;
       bd_queimadas            postgres    false    220            �           2606    16421 #   focos_de_queimada unq_foco_queimada 
   CONSTRAINT     ~   ALTER TABLE ONLY bd_queimadas.focos_de_queimada
    ADD CONSTRAINT unq_foco_queimada UNIQUE (data_hora, latitude, longitude);
 S   ALTER TABLE ONLY bd_queimadas.focos_de_queimada DROP CONSTRAINT unq_foco_queimada;
       bd_queimadas            postgres    false    216    216    216            �           2606    24632    municipios unq_nome_municipio 
   CONSTRAINT     h   ALTER TABLE ONLY bd_queimadas.municipios
    ADD CONSTRAINT unq_nome_municipio UNIQUE (nome_municipio);
 M   ALTER TABLE ONLY bd_queimadas.municipios DROP CONSTRAINT unq_nome_municipio;
       bd_queimadas            postgres    false    218            �           2606    24604    satelites unq_nome_satelite 
   CONSTRAINT     e   ALTER TABLE ONLY bd_queimadas.satelites
    ADD CONSTRAINT unq_nome_satelite UNIQUE (nome_satelite);
 K   ALTER TABLE ONLY bd_queimadas.satelites DROP CONSTRAINT unq_nome_satelite;
       bd_queimadas            postgres    false    220            �           2606    24613    regioes_imediatas unq_regiao 
   CONSTRAINT     d   ALTER TABLE ONLY bd_queimadas.regioes_imediatas
    ADD CONSTRAINT unq_regiao UNIQUE (nome_regiao);
 L   ALTER TABLE ONLY bd_queimadas.regioes_imediatas DROP CONSTRAINT unq_regiao;
       bd_queimadas            postgres    false    217                        2606    24687    focos_de_queimada fk_municipio    FK CONSTRAINT     �   ALTER TABLE ONLY bd_queimadas.focos_de_queimada
    ADD CONSTRAINT fk_municipio FOREIGN KEY (id_municipio) REFERENCES bd_queimadas.municipios(id_municipio) ON DELETE SET NULL NOT VALID;
 N   ALTER TABLE ONLY bd_queimadas.focos_de_queimada DROP CONSTRAINT fk_municipio;
       bd_queimadas          postgres    false    218    3319    216            �           0    0 ,   CONSTRAINT fk_municipio ON focos_de_queimada    COMMENT     l   COMMENT ON CONSTRAINT fk_municipio ON bd_queimadas.focos_de_queimada IS 'Chave estrangeira para municipio';
          bd_queimadas          postgres    false    3328                       2606    24692    satelite_queimada fk_queimada    FK CONSTRAINT     �   ALTER TABLE ONLY bd_queimadas.satelite_queimada
    ADD CONSTRAINT fk_queimada FOREIGN KEY (id_queimada) REFERENCES bd_queimadas.focos_de_queimada(id_queimada) ON DELETE CASCADE NOT VALID;
 M   ALTER TABLE ONLY bd_queimadas.satelite_queimada DROP CONSTRAINT fk_queimada;
       bd_queimadas          postgres    false    221    3311    216            �           0    0 +   CONSTRAINT fk_queimada ON satelite_queimada    COMMENT     s   COMMENT ON CONSTRAINT fk_queimada ON bd_queimadas.satelite_queimada IS 'Armazena a chave estrangeira de queimada';
          bd_queimadas          postgres    false    3330                       2606    24682    municipios fk_regiao    FK CONSTRAINT     �   ALTER TABLE ONLY bd_queimadas.municipios
    ADD CONSTRAINT fk_regiao FOREIGN KEY (id_regiao) REFERENCES bd_queimadas.regioes_imediatas(id_regiao) ON DELETE SET NULL;
 D   ALTER TABLE ONLY bd_queimadas.municipios DROP CONSTRAINT fk_regiao;
       bd_queimadas          postgres    false    218    3315    217                       2606    24697    satelite_queimada fk_satelite    FK CONSTRAINT     �   ALTER TABLE ONLY bd_queimadas.satelite_queimada
    ADD CONSTRAINT fk_satelite FOREIGN KEY (id_satelite) REFERENCES bd_queimadas.satelites(id_satelite) ON DELETE CASCADE NOT VALID;
 M   ALTER TABLE ONLY bd_queimadas.satelite_queimada DROP CONSTRAINT fk_satelite;
       bd_queimadas          postgres    false    221    220    3323            �           0    0 +   CONSTRAINT fk_satelite ON satelite_queimada    COMMENT     q   COMMENT ON CONSTRAINT fk_satelite ON bd_queimadas.satelite_queimada IS 'Armazena a chave primária de satelite';
          bd_queimadas          postgres    false    3331            �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �     