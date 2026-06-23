import integracao_b3
import time

# CRITÉRIO DE ACEITE: O sistema deve consultar a B3 e utilizar Cache para otimizar performance.

def test_deve_retornar_dados_validos_ao_consultar_ticker_real():
    """Verifica se a integração com o Yahoo Finance devolve um preço numérico."""
    # 1. Arrange
    ticker = "WEGE3"
    
    # 2. Act
    resultado = integracao_b3.buscar_cotacao_b3(ticker)
    
    # 3. Assert
    assert resultado is not None
    assert resultado["ticker"] == "WEGE3"
    assert isinstance(resultado["preco_atual"], float)
    assert resultado["preco_atual"] > 0

def test_deve_retornar_none_ao_consultar_ticker_falso():
    """Verifica se a API lida graciosamente com ativos que não existem."""
    # 1. Arrange
    ticker = "TESTE99"
    
    # 2. Act
    resultado = integracao_b3.buscar_cotacao_b3(ticker)
    
    # 3. Assert
    assert resultado is None