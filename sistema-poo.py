from abc import ABC, abstractmethod

class Cliente(ABC):
    def __init__(self, endereco):
        self.contas = []
        self.endereco = endereco

    @abstractmethod
    def criar_conta(self, numero, agencia, saldo):
        pass

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def __str__(self):
        return f"tipo: {self.__class__.__name__.capitalize()} | {', '.join([f'{chave}: {valor}' for chave, valor in self.__dict__.items()])}"

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

    def criar_conta(self, numero, agencia, saldo):
        nova_conta = Conta(numero=numero, agencia=agencia, saldo=saldo, cliente=self)
        self.adicionar_conta(nova_conta)

class ContaJuridica(Cliente):
    def __init__(self, cnpj, nome_fantasia, endereco):
        super().__init__(endereco)
        self.cnpj = cnpj
        self.nome_fantasia = nome_fantasia

    def criar_conta(self, numero, agencia, saldo):
        nova_conta = Conta(numero=numero, agencia=agencia, saldo=saldo, cliente=self)
        self.adicionar_conta(nova_conta)

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Conta:
    def __init__(self, numero, agencia, saldo, cliente):
        self._numero = numero
        self._agencia = agencia
        self._saldo = saldo
        self._cliente = cliente
        self._historico = Historico()
        self._limiteDeSaque = 1000
        self._saqueAcumulado = 0

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    def sacar(self, valor):
        if valor > 0 and self._saldo >= valor:
            if self._saqueAcumulado > self._limiteDeSaque:
                print("Limite excedido.")
                return False
            else:
                self._saqueAcumulado = valor + self._saqueAcumulado
                self._saldo -= valor
                self._historico.adicionar_transacao(f"Saque de {valor} realizado.")
                return True
        else:
            print("Saldo insuficiente para saque.")
            return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            self._historico.adicionar_transacao(f"Depósito de {valor} realizado.")
            return True
        else:
            print("Valor de depósito inválido.")
            return False

    def consultar_saldo(self):
        return self._saldo

    def __str__(self):
        return f"{self.__class__.__name__.capitalize()} | {', '.join([f'{chave}: {valor}' for chave, valor in self.__dict__.items()])}"


