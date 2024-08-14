CREATE TABLE tb_rezago_social (
                clave_entidad INT, 
                entidad_federativa VARCHAR, 
                clave_municipio INT, 
                municipio VARCHAR,
                poblacion_total INT, 
                poblacion_de_15_anos_o_mas_analfabeta REAL,
                poblacion_de_6_a_14_anos_que_no_asiste_a_la_escuela REAL, 
                poblacion_de_15_anos_y_mas_con_educacion_basica_incompleta REAL,
                poblacion_sin_derechohabiencia_a_servicios_de_salud REAL,
                viviendas_con_piso_de_tierra REAL,
                viviendas_que_no_disponen_de_excusado_o_sanitario REAL,
                viviendas_que_no_disponen_de_agua_entubada_de_la_red_publica REAL,
                viviendas_que_no_disponen_de_drenaje REAL,
                viviendas_que_no_disponen_de_energia_electrica REAL,
                viviendas_que_no_disponen_de_lavadora REAL,
                viviendas_que_no_disponen_de_refrigerador REAL, 
                indice_de_rezago_social REAL,
                grado_de_rezago_social VARCHAR
);

\copy tb_rezago_social(clave_entidad,entidad_federativa,clave_municipio,municipio,poblacion_total,poblacion_de_15_anos_o_mas_analfabeta,poblacion_de_6_a_14_anos_que_no_asiste_a_la_escuela,poblacion_de_15_anos_y_mas_con_educacion_basica_incompleta,poblacion_sin_derechohabiencia_a_servicios_de_salud,viviendas_con_piso_de_tierra,viviendas_que_no_disponen_de_excusado_o_sanitario,viviendas_que_no_disponen_de_agua_entubada_de_la_red_publica,viviendas_que_no_disponen_de_drenaje,viviendas_que_no_disponen_de_energia_electrica,viviendas_que_no_disponen_de_lavadora,viviendas_que_no_disponen_de_refrigerador,indice_de_rezago_social,grado_de_rezago_social) FROM '/content/rezago_coneval_2020.csv' DELIMITERS ',' CSV HEADER;
