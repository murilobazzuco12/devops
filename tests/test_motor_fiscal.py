import motor_fiscal

# CRITÉRIO DE ACEITE: O sistema deve identificar corretamente FIIs e Ações.

def test_deve_classificar_ativo_como_fii_quando_termina_em_11():
    """Testa se um ticker terminado em 11 é classificado como Fundo Imobiliário."""
    # 1. Arrange (Preparar)
    ticker = "MXRF11"
    
    # 2. Act (Agir)
    resultado = motor_fiscal.classificar_ativo(ticker)
    
    # 3. Assert (Verificar)
    assert resultado == "FII"

def test_deve_classificar_ativo_como_acao_quando_for_unit_excecao():
    """Testa se as Units (que terminam em 11, mas são ações) são tratadas corretamente."""
    # 1. Arrange
    ticker = "TAEE11"
    
    # 2. Act
    resultado = motor_fiscal.classificar_ativo(ticker)
    
    # 3. Assert
    assert resultado == "ACAO"