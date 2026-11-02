# MCP Calculadora

Estudo prático de criação de um servidor **MCP (Model Context Protocol)** em Python, com quatro operações matemáticas expostas como ferramentas para aplicações de IA. O projeto utiliza o `FastMCP` do SDK oficial de Python e tem como cenário de integração o Claude Desktop no Windows.

## Objetivo do estudo

Entender como uma aplicação de IA descobre e utiliza funções implementadas fora do modelo, passando por configuração do ambiente, definição das ferramentas, execução local e integração com um cliente MCP.

O exemplo permite estudar:

- A comunicação entre uma aplicação hospedeira, seu cliente MCP e um servidor local.
- O registro de funções com o decorador `@mcp.tool()`.
- O uso de anotações de tipos e docstrings na descrição das ferramentas.
- O tratamento de erros, como divisão por zero.
- A validação das chamadas pelo MCP Inspector.

## Como o MCP aparece neste projeto

MCP é um protocolo para conectar aplicações de IA a ferramentas e fontes de contexto. Neste exemplo, o Claude Desktop é a aplicação hospedeira, seu cliente MCP se conecta ao servidor `Calculadora`, e o servidor executa as funções de Python solicitadas.

```text
Usuário solicita um cálculo
          |
Aplicação de IA / cliente MCP
          |  descobre ferramentas e envia uma chamada
Servidor Calculadora (server.py)
          |  executa a função Python
Resultado retorna ao cliente e à aplicação
```

O servidor usa o transporte local **stdio**: recebe mensagens pela entrada padrão e responde pela saída padrão. Ele não inicia uma página web ou uma API HTTP. A implementação fornece ferramentas; não define recursos ou modelos de prompts MCP.

## Ferramentas disponíveis

Todas recebem os parâmetros `a` e `b`, anotados como `float`, e retornam um resultado numérico.

| Ferramenta | Operação | Exemplo | Resultado esperado |
| --- | --- | --- | --- |
| `somar` | `a + b` | `a=15, b=27` | `42.0` |
| `subtrair` | `a - b` | `a=10, b=4` | `6.0` |
| `multiplicar` | `a * b` | `a=6, b=7` | `42.0` |
| `dividir` | `a / b` | `a=20, b=5` | `4.0` |

Quando `b` é zero em `dividir`, a função lança `ValueError` com a mensagem `Não é possível dividir por zero.` O SDK comunica a falha ao cliente como erro da ferramenta.

## Tecnologias e requisitos

- **Python 3.14 ou superior**, conforme o `pyproject.toml`; `.python-version` seleciona a versão 3.14.
- **uv**, para gerenciar o ambiente e as dependências.
- **MCP Python SDK**, declarado como `mcp[cli]>=1.28.1`; o `uv.lock` incluído registra a versão 1.28.1.
- **Claude Desktop**, para reproduzir a integração descrita no estudo.
- **Node.js com npm/npx**, para executar o MCP Inspector.

A documentação original descreve o uso no Windows 11. Embora o SDK suporte outras versões de Python, este repositório exige Python 3.14 ou superior.

## Estrutura do projeto

```text
mcp-calculadora/
├── .gitignore
├── .python-version
├── README.md
├── documentação_mcp_server_calculadora_Lucas_Godoy.docx
├── main.py
├── pyproject.toml
├── server.py
└── uv.lock
```

- `server.py`: servidor MCP e as quatro ferramentas.
- `main.py`: arquivo inicial gerado na criação do projeto; apenas imprime uma mensagem. Para iniciar o servidor, utilize `server.py`.
- `pyproject.toml`: metadados, requisito de Python e dependências.
- `uv.lock`: versões resolvidas das dependências.
- Documento Word: registro original do passo a passo do estudo.
- `.venv/` e `__pycache__/`: gerados localmente e ignorados pelo Git.

## Instalação e execução

Instale o [Python](https://www.python.org/downloads/) e o [uv](https://docs.astral.sh/uv/getting-started/installation/). Em seguida, no PowerShell:

```powershell
git clone https://github.com/LucasCGB/mcp-calculadora.git
cd mcp-calculadora
uv sync --locked
uv run python server.py
```

Ao executar o último comando, o processo aguarda mensagens de um cliente MCP. Não há um menu interativo para digitar operações. Use `Ctrl+C` para encerrar.

Para reproduzir as dependências registradas, mantenha o `uv.lock` e utilize `uv sync --locked`. Não é necessário executar `uv init` ou `uv add` depois de clonar este projeto.

## Testando com o MCP Inspector

Com Node.js e npm/npx disponíveis, execute na pasta do projeto:

```powershell
uv run mcp dev server.py
```

Abra o endereço informado no terminal e conecte o Inspector ao servidor. Na área de ferramentas, liste as funções e execute chamadas com os parâmetros `a` e `b`.

Casos sugeridos para validação manual:

| Caso | Ferramenta e entrada | Resultado esperado |
| --- | --- | --- |
| Soma | `somar(a=15, b=27)` | `42.0` |
| Resultado negativo | `subtrair(a=4, b=10)` | `-6.0` |
| Casas decimais | `multiplicar(a=2.5, b=4)` | `10.0` |
| Divisão | `dividir(a=9, b=2)` | `4.5` |
| Divisão por zero | `dividir(a=10, b=0)` | Erro da ferramenta |

Esses casos são um roteiro de teste; o repositório ainda não contém uma suíte de testes automatizados.

## Integração com o Claude Desktop

Localize a configuração dos servidores MCP locais nas configurações de desenvolvedor do Claude Desktop. No fluxo descrito no estudo, o acesso é por **Settings → Developer → Edit Config**; os nomes podem variar conforme a versão do aplicativo.

Adicione a entrada `calculadora` ao objeto `mcpServers` do arquivo `claude_desktop_config.json`, preservando outras configurações existentes:

```json
{
  "mcpServers": {
    "calculadora": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\SeuUsuario\\mcp-calculadora",
        "run",
        "python",
        "server.py"
      ]
    }
  }
}
```

Substitua o caminho pelo diretório real do projeto. No JSON, as barras invertidas precisam ser duplicadas. Se `uv` não for encontrado pelo aplicativo, utilize seu caminho absoluto no campo `command`; no PowerShell, `(Get-Command uv).Source` mostra esse caminho.

Salve o arquivo e encerre completamente o Claude Desktop, inclusive pela bandeja do sistema, antes de reabri-lo. Verifique se o servidor e suas ferramentas estão disponíveis e habilitados.

Exemplos de solicitações:

- “Some 15 e 27 usando a ferramenta da calculadora.”
- “Use a calculadora para dividir 20 por 5.”
- “Tente dividir 10 por zero usando a calculadora e explique o erro.”

Além de conferir a resposta numérica, verifique na interface se houve uma chamada à ferramenta. O modelo pode responder a contas simples sem usar o servidor.

## Entendendo a implementação

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Calculadora")

@mcp.tool()
def somar(a: float, b: float) -> float:
    """Soma dois números e retorna o resultado."""
    return a + b

if __name__ == "__main__":
    mcp.run()
```

`FastMCP("Calculadora")` cria o servidor. O decorador registra a função como ferramenta, enquanto a assinatura e a docstring ajudam o SDK a expor seus parâmetros e sua finalidade ao cliente. O bloco final inicia a comunicação por stdio quando o arquivo é executado diretamente.

As demais operações seguem o mesmo padrão em `server.py`. A divisão inclui uma verificação explícita do denominador antes de realizar a operação.

## Solução de problemas

| Sintoma | Verificação ou solução |
| --- | --- |
| `uv` não encontrado | Confirme a instalação e reabra o terminal. No cliente MCP, configure o caminho absoluto do executável. |
| Python incompatível | Execute `uv python install 3.14` e depois `uv sync --locked`. |
| `No pyproject.toml found` | Entre na pasta clonada ou corrija o caminho passado a `--directory`. |
| Pacote `mcp` ou comando `mcp` não encontrado | Execute `uv sync --locked` na raiz do projeto e use os comandos com `uv run`. |
| Inspector não inicia | Confira `node --version` e `npx --version`; acompanhe o diagnóstico no terminal. |
| Servidor não aparece no Claude Desktop | Valide o JSON, os caminhos e o executável `uv`, e reinicie completamente o aplicativo. |
| Terminal parece parado ao executar `server.py` | O servidor está aguardando mensagens MCP por stdio; conecte um cliente ou use o Inspector. |

Evite adicionar `print()` à saída padrão do servidor: ela é usada pelas mensagens do protocolo. Para diagnóstico, use logging direcionado à saída de erro.

## Aprendizados e limites

O estudo demonstra o ciclo de definição, descoberta e chamada de ferramentas locais. As operações são executadas por funções Python e o resultado retorna à aplicação de IA pelo protocolo.

A implementação usa números de ponto flutuante, sujeitos a aproximações em cálculos decimais. Não inclui interface gráfica, persistência, autenticação, transporte HTTP ou interpretação de expressões matemáticas completas. Cada chamada realiza uma das quatro operações com dois argumentos.

Possíveis próximos passos incluem testes automatizados, novas operações e comparação entre clientes MCP.

## Referências

- [Documentação do Model Context Protocol](https://modelcontextprotocol.io/)
- [SDK oficial de Python — versão 1.28.1](https://github.com/modelcontextprotocol/python-sdk/tree/v1.28.1)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
- [Documentação do uv](https://docs.astral.sh/uv/)
- [Documentação original do estudo](documentação_mcp_server_calculadora_Lucas_Godoy.docx)

Estudo desenvolvido por Lucas Godoy.
