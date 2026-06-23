import pytest
import time
import random
from playwright.sync_api import Page, expect

def gerar_cpf_valido():
    cpf = [random.randint(0, 9) for _ in range(9)]
    for _ in range(2):
        val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11
        cpf.append(11 - val if val > 1 else 0)
    return ''.join(map(str, cpf))

def test_fluxo_transacao_completo(page: Page):
    # ==========================================
    # PREPARAÇÃO: Login rápido no sistema
    # ==========================================
    cpf_teste = gerar_cpf_valido()
    email_teste = f"investidor_{int(time.time())}@teste.com"
    telefone_teste = f"119{random.randint(10000000, 99999999)}"

    page.goto("https://fincalcdevops.local/cadastro")
    page.locator("#nome").fill("Investidor QA")
    page.locator("#cpf").fill(cpf_teste)
    page.locator("#telefone").fill(telefone_teste)
    page.locator("#email").fill(email_teste)
    page.locator("#senha").fill("SenhaForte@2026")
    page.locator("#confirmarSenha").fill("SenhaForte@2026")
    page.locator("text=Finalizar Cadastro").click()
    
    expect(page).to_have_url("https://fincalcdevops.local/login")
    
    page.locator("#email").fill(email_teste)
    page.locator("#senha").fill("SenhaForte@2026")
    page.locator("text=Entrar").click()
    
    expect(page).to_have_url("https://fincalcdevops.local/home")

    # ==========================================
    # ETAPA 3: O CORE DO SISTEMA (Transações)
    # ==========================================
    
    # O robô clica no menu de transações
    page.goto("https://fincalcdevops.local/transacoes")

    # Digita o ativo
    page.locator("#ticker").fill("PRIO3")
    
    # Clica no campo de quantidade. Isso tira o foco do Ticker 
    # e aciona o seu evento 'blur' para validar na B3!
    page.locator("#quantidade").click()
    
    # O robô aguarda o botão ser habilitado novamente após o aval da B3
    expect(page.locator("#btn-salvar")).to_be_enabled()

    # Preenche o restante do boletim de negociação
    page.locator("#tipo_operacao").select_option("COMPRA")
    page.locator("#quantidade").fill("100")
    page.locator("#preco_unitario").fill("85.50")
    page.locator("#taxas").fill("2.50")

    # Confirma a transação
    page.locator("text=Salvar Transação").click()

    # PROVA REAL 1: O backend retornou sucesso?
    expect(page.locator("#alerta")).to_contain_text("Transação registrada com sucesso.")

    # PROVA REAL 2: O sistema listou o ativo corretamente na tabela de baixo?
    expect(page.locator("#tabelaTransacoes")).to_contain_text("PRIO3")

def test_falha_exclusao_gera_saldo_negativo(page: Page):
    # ==========================================
    # PREPARAÇÃO RÁPIDA: Usuário e Login
    # ==========================================
    cpf_teste = gerar_cpf_valido()
    email_teste = f"investidor_{int(time.time())}@teste.com"
    telefone_teste = f"119{random.randint(10000000, 99999999)}"

    page.goto("https://fincalcdevops.local/cadastro")
    page.locator("#nome").fill("Investidor Validador")
    page.locator("#cpf").fill(cpf_teste)
    page.locator("#telefone").fill(telefone_teste)
    page.locator("#email").fill(email_teste)
    page.locator("#senha").fill("SenhaForte@2026")
    page.locator("#confirmarSenha").fill("SenhaForte@2026")
    page.locator("text=Finalizar Cadastro").click()
    
    expect(page).to_have_url("https://fincalcdevops.local/login")
    
    page.locator("#email").fill(email_teste)
    page.locator("#senha").fill("SenhaForte@2026")
    page.locator("text=Entrar").click()
    expect(page).to_have_url("https://fincalcdevops.local/home")

    # ==========================================
    # CRIANDO A ARMADILHA (Compra 100 e Vende 50)
    # ==========================================
    page.goto("https://fincalcdevops.local/transacoes")

    # 1. Registra a Compra (100 VALE3)
    page.locator("#ticker").fill("VALE3")
    page.locator("#quantidade").click()
    expect(page.locator("#btn-salvar")).to_be_enabled()
    page.locator("#tipo_operacao").select_option("COMPRA")
    page.locator("#quantidade").fill("100")
    page.locator("#preco_unitario").fill("60.00")
    page.locator("#taxas").fill("1.00")
    page.locator("text=Salvar Transação").click()
    expect(page.locator("#alerta")).to_contain_text("Transação registrada com sucesso.")

    # 2. Registra a Venda (50 VALE3)
    page.locator("#ticker").fill("VALE3")
    page.locator("#quantidade").click()
    expect(page.locator("#btn-salvar")).to_be_enabled()
    page.locator("#tipo_operacao").select_option("VENDA")
    page.locator("#quantidade").fill("50")
    page.locator("#preco_unitario").fill("65.00")
    page.locator("#taxas").fill("1.00")
    page.locator("text=Salvar Transação").click()
    expect(page.locator("#alerta")).to_contain_text("Transação registrada com sucesso.")

    # ==========================================
    # O ATAQUE: Tentar apagar a Compra Base
    # ==========================================
    
    # Criamos uma "escuta" no robô para capturar todos os alertas do navegador
    mensagens_alerta = []
    
    def escutar_dialogos(dialog):
        mensagens_alerta.append(dialog.message)
        dialog.accept() # O robô clica em "OK" na caixinha

    page.on("dialog", escutar_dialogos)

    # O robô procura a linha da tabela que tem a palavra "COMPRA" e clica na lixeira dela
    linha_compra = page.locator("tr").filter(has_text="COMPRA").first
    linha_compra.locator("button", has_text="🗑️").click()

    # Dá um tempinho para o backend pensar e devolver a mensagem
    page.wait_for_timeout(1000)

    # ==========================================
    # A PROVA REAL: O Backend segurou a bomba?
    # ==========================================
    # Vamos verificar se o sistema disparou algum alerta de "Atenção:" (que você programou no seu JS)
    backend_bloqueou = any("Atenção" in msg for msg in mensagens_alerta)
    
    # Se backend_bloqueou for Falso, o assert vai falhar e explodir a mensagem customizada abaixo
    assert backend_bloqueou, f"O Motor Fiscal FALHOU e deixou excluir a transação! Alertas capturados: {mensagens_alerta}"