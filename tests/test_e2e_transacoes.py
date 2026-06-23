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