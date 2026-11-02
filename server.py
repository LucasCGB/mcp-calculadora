from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Calculadora")

@mcp.tool()
def somar(a: float, b: float) -> float:
    """Soma dois números e retorna o resultado."""
    return a + b

@mcp.tool()
def subtrair(a: float, b: float) -> float:
    """Subtrai o segundo número do primeiro (a - b)."""
    return a - b

@mcp.tool()
def multiplicar(a: float, b: float) -> float:
    """Multiplica dois números."""
    return a * b

@mcp.tool()
def dividir(a: float, b: float) -> float:
    """Divide o primeiro número pelo segundo (a / b)."""
    if b == 0:
        raise ValueError("Não é possível dividir por zero.")
    return a / b

if __name__ == "__main__":
    mcp.run()