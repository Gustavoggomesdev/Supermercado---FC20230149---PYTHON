class Product:
    def __init__(self, codigo, produto, valor, unidades, tipo, validade=None, garantia=None):
        self.codigo = codigo
        self.produto = produto
        self.valor = valor
        self.unidades = unidades
        self.tipo = tipo
        self.validade = validade
        self.garantia = garantia

    def __str__(self):
        return f"Código: {self.codigo}, Nome: {self.produto}, Preço: {self.valor}, Unidades: {self.unidades}"


class Market:
    def __init__(self):
        self.produtos = {}
        self.caixa_aberto = False
        self.valor_inicial = 0.0
        self.valor_final = 0.0
        self.vendas = []

    def open_cash_register(self):
        if not self.caixa_aberto:
            self.valor_inicial = float(input("Digite o valor inicial do caixa: "))
            self.valor_final = self.valor_inicial
            self.caixa_aberto = True
            print(f"Caixa aberto com valor inicial de R$ {self.valor_inicial}")
        else:
            print("O caixa já está aberto.")

    def close_cash_register(self):
        if self.caixa_aberto:
            print(f"Caixa fechado com valor final de R$ {self.valor_final}")
            self.caixa_aberto = False
        else:
            print("O caixa já está fechado.")

    def register_product(self):
        codigo = int(input("Digite o código do produto: "))
        if codigo in self.produtos:
            print("Produto já cadastrado!")
            return
        
        nome = input("Digite o nome do produto: ")
        valor = float(input("Digite o valor do produto: "))
        unidades = int(input("Digite a quantidade de unidades em estoque: "))
        tipo = input("Digite o tipo do produto (alimento, utensilio, eletroeletronico): ")
        validade = input("Digite a validade do produto (ou deixe em branco se não tiver): ")
        garantia = input("Digite a garantia do produto (ou deixe em branco se não tiver): ")

        produto = Product(codigo, nome, valor, unidades, tipo, validade or None, garantia or None)
        self.produtos[codigo] = produto
        print("Produto cadastrado com sucesso.")

    def search_product(self):
        codigo = int(input("Digite o código do produto para pesquisa: "))
        produto = self.produtos.get(codigo)
        if produto:
            print(produto)
        else:
            print("Produto não encontrado.")

    def delete_product(self):
        codigo = int(input("Digite o código do produto a ser excluído: "))
        if codigo in self.produtos:
            del self.produtos[codigo]
            print("Produto excluído com sucesso.")
        else:
            print("Produto não encontrado.")

    def make_sale(self):
        if not self.caixa_aberto:
            print("O caixa não está aberto!")
            return

        total_compra = 0.0
        itens_compra = {}

        while True:
            codigo = int(input("Digite o código do produto para a venda (ou 0 para finalizar): "))
            if codigo == 0:
                break

            produto = self.produtos.get(codigo)
            if produto:
                quantidade = int(input("Digite a quantidade a ser vendida: "))
                if produto.unidades >= quantidade:
                    valor_venda = produto.valor * quantidade
                    produto.unidades -= quantidade
                    total_compra += valor_venda
                    self.valor_final += valor_venda

                    if produto.produto in itens_compra:
                        itens_compra[produto.produto]['quantidade'] += quantidade
                        itens_compra[produto.produto]['valor'] += valor_venda
                    else:
                        itens_compra[produto.produto] = {'quantidade': quantidade, 'valor': valor_venda}
                    self.vendas.append((produto.produto, quantidade, valor_venda))

                    print("\nItens da compra até o momento:")
                    for item_nome, info in itens_compra.items():
                        print(f"{info['quantidade']} x {item_nome}: R$ {info['valor']:.2f}")
                    print(f"Total da compra atual: R$ {total_compra:.2f}\n")
                else:
                    print("Quantidade insuficiente em estoque.")
            else:
                print("Produto não encontrado.")

        print(f"Total da compra: R$ {total_compra:.2f}")

    def show_nearly_out_of_stock(self):
        print("Produtos com baixa quantidade em estoque:")
        for produto in self.produtos.values():
            if produto.unidades < 5:
                print(produto)

    def show_nearly_expiring(self):
        print("Produtos próximos do vencimento:")
        for produto in self.produtos.values():
            if produto.validade:
                print(produto)


market = Market()

while True:
    print("Opções:")
    print("1 - Abrir Caixa")
    print("2 - Menu Principal")
    print("3 - Fechar Caixa")
    escolha = int(input("Digite a opção desejada: "))

    if escolha == 1:
        market.open_cash_register()
    elif escolha == 2:
        print("Menu Principal:")
        print("1 - Cadastrar Produto")
        print("2 - Pesquisar Produto")
        print("3 - Excluir Produto")
        print("4 - Realizar Venda")
        print("5 - Mostrar Produtos Próximos ao Vencimento")
        print("6 - Mostrar Produtos Próximos a Esgotar")
        print("7 - Voltar")

        escolha2 = int(input("Digite a opção desejada: "))

        if escolha2 == 1:
            market.register_product()
        elif escolha2 == 2:
            market.search_product()
        elif escolha2 == 3:
            market.delete_product()
        elif escolha2 == 4:
            market.make_sale()
        elif escolha2 == 5:
            market.show_nearly_expiring()
        elif escolha2 == 6:
            market.show_nearly_out_of_stock()
        elif escolha2 == 7:
            continue
    elif escolha == 3:
        market.close_cash_register()
        break
