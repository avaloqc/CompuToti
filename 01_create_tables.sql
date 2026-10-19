--  Criação das tabelas (DDL)  
-- Habilitar suporte a chaves estrangeiras no SQLite
PRAGMA foreign_keys = ON;

-- 1. Tabela de Fabricantes
CREATE TABLE Fabricantes (
    CodigoFabricante INTEGER PRIMARY KEY,
    Fabricante TEXT NOT NULL
);

-- 2. Tabela de Produtos
CREATE TABLE Produtos (
    CodigoProduto INTEGER PRIMARY KEY,
    Produto TEXT NOT NULL,
    Preco REAL NOT NULL,
    CodigoFabricante INTEGER NOT NULL,
    FOREIGN KEY (CodigoFabricante) REFERENCES Fabricantes (CodigoFabricante)
);

-- 3. Tabela de Pedidos
CREATE TABLE Pedidos (
    NumeroPedido INTEGER PRIMARY KEY,
    DataVenda TEXT NOT NULL, -- Formato ISO8601 recomendado: 'YYYY-MM-DD'
    Estado TEXT NOT NULL
);

-- 4. Tabela de Itens do Pedido (Vendas detalhadas)
CREATE TABLE ItensPedido (
    IdVenda INTEGER PRIMARY KEY AUTOINCREMENT,
    NumeroPedido INTEGER NOT NULL,
    CodigoProduto INTEGER NOT NULL,
    QuantidadeVendida INTEGER NOT NULL,
    ValorVenda REAL NOT NULL,
    FOREIGN KEY (NumeroPedido) REFERENCES Pedidos (NumeroPedido),
    FOREIGN KEY (CodigoProduto) REFERENCES Produtos (CodigoProduto)
);
