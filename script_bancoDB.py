<<<<<<< HEAD
table_cliente = """(CREATE TABLE IF NOT EXISTS "cliente" (
=======
table_cliente = """(CREATE TABLE IF NOT EXISTS"cliente" (
>>>>>>> 2ae28ffb88e3cd1da1e56acfb931ca84c6bb4212
	"id_cliente"	INTEGER,
	"nome_cliente"	VARCHAR(50) NOT NULL,
	"cpf"	VARCHAR(50) NOT NULL UNIQUE,
	"endereco"	VARCHAR(50) NOT NULL,
	"telefone"	VARCHAR(50) NOT NULL,
	PRIMARY KEY("id_cliente" AUTOINCREMENT)
) )"""