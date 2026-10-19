-- Inserção de dados iniciais (DML)

-- Inserir Fabricantes únicos
INSERT INTO Fabricantes (CodigoFabricante, Fabricante) VALUES 
(1, 'Sony'),
(2, 'Creative Labs'),
(3, 'Hewlett-Packard'),
(6, 'Winchester');

-- Inserir Produtos únicos
INSERT INTO Produtos (CodigoProduto, Produto, Preco, CodigoFabricante) VALUES 
(5, 'Monitor', 240.0, 1),
(7, 'CD drive', 90.0, 2),
(2, 'Memory', 120.0, 6),
(8, 'Printer', 270.0, 3),
(9, 'Toner cartridge', 66.0, 3);

-- Inserir Pedidos únicos
INSERT INTO Pedidos (NumeroPedido, DataVenda, Estado) VALUES 
(1001, '2025-01-10', 'SP'),
(1002, '2025-01-15', 'RJ'),
(1003, '2025-01-20', 'MG');

-- Inserir Itens dos Pedidos
INSERT INTO ItensPedido (NumeroPedido, CodigoProduto, QuantidadeVendida, ValorVenda) VALUES 
(1001, 5, 2, 480.0),
(1001, 7, 1, 90.0),
(1002, 2, 3, 360.0),
(1003, 8, 1, 270.0),
(1003, 9, 2, 132.0);
