table_cliente = """(CREATE TABLE IF NOT EXISTS "cliente" (
	"id_cliente"	INTEGER,
	"nome_cliente"	VARCHAR(50) NOT NULL,
	"cpf"	VARCHAR(50) NOT NULL UNIQUE,
	"endereco"	VARCHAR(50) NOT NULL,
	"telefone"	VARCHAR(50) NOT NULL,
	PRIMARY KEY("id_cliente" AUTOINCREMENT)
) )"""