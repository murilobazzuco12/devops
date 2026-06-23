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

def test_jornada_cadastro_e_login(page: Page):
    # Cria dados 100% únicos para esta execução do teste
    cpf_teste = gerar_cpf_valido()
    email_teste = f"investidor_{int(time.time())}@teste.com"
    telefone_teste = f"119{random.randint(10000000, 99999999)}"

    # ==========================================
    # ETAPA 1: O CADASTRO DO NOVO USUÁRIO
    # ==========================================
    page.goto("https://fincalcdevops.local/cadastro")

    page.locator("#nome").fill("Investidor QA")
    page.locator("#cpf").fill(cpf_teste)
    page.locator("#telefone").fill(telefone_teste)
    page.locator("#email").fill(email_teste)
    
    page.locator("#senha").fill("SenhaForte@2026")
    page.locator("#confirmarSenha").fill("SenhaForte@2026")

    page.locator("text=Finalizar Cadastro").click()

    # Aguarda o redirecionamento
    expect(page).to_have_url("https://fincalcdevops.local/login")

    # ==========================================
    # ETAPA 2: O LOGIN 
    # ==========================================
    page.locator("#email").fill(email_teste)
    page.locator("#senha").fill("SenhaForte@2026")

    page.locator("text=Entrar").click()

    # Validação final
    expect(page).to_have_url("https://fincalcdevops.local/home")