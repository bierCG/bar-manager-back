-- ------------------------------------------------------------------------------------------
-- USUÁRIOS
-- ------------------------------------------------------------------------------------------

TRUNCATE usuarios, pedidos RESTART IDENTITY CASCADE;

INSERT INTO usuarios (nome, email, senha, role)
VALUES (
    'Usuario 1',
    'user@email.com',
    '$argon2id$v=19$m=65536,t=3,p=4$6utweNkxndKgLeSV67AYSA$I628BE7uflrXmF0PWsie6Xi7OlyScr9JeoiLTqjaIII',
    'barman'
);

INSERT INTO usuarios (nome, email, senha, role)
VALUES (
    'Usuario 2',
    'teste@email.com',
    '123456',
    'barman'
);

INSERT INTO usuarios (nome, email, senha, role)
VALUES (
    'Usuario 2',
    'fulano_duplicado@email.com',
    '123456',
    'barman'
);


-- ------------------------------------------------------------------------------------------
-- PEDIDOS
-- ------------------------------------------------------------------------------------------

INSERT INTO pedidos (cliente_nome, drink, status, vendedor_id)
VALUES (
    'Cliente Aberto',
    'Caipirinha',
    'ABERTO',
    1
);

INSERT INTO pedidos (cliente_nome, drink, status, vendedor_id)
VALUES (
    'Cliente Pronto',
    'Caipirinha',
    'PRONTO',
    2
);

INSERT INTO pedidos (cliente_nome, drink, status, vendedor_id)
VALUES (
    'Cliente Cancelado',
    'Caipirinha',
    'CANCELADO',
    1
);