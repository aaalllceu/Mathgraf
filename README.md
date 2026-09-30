# Gráfico de Funções

Aplicativo didático para visualizar funções do 1º e 2º grau. Feito em Python com Kivy e com interface em português, adaptável a telas pequenas.

## Recursos

- Gráfico de função linear: `f(x) = ax + b`.
- Gráfico de função quadrática: `f(x) = ax² + bx + c`.
- Eixos, grade e escala vertical ajustados automaticamente.
- Intervalo horizontal configurável; aceita decimal com ponto ou vírgula.
- Exibe equação, vértice e discriminante/classificação das raízes da quadrática.
- Mensagens de validação em português.
- Testes automatizados e GitHub Actions.

## Executar no computador

Requer Python 3.11 ou superior e um ambiente com suporte gráfico.

1. Clone o repositório ou baixe o código pelo GitHub.
2. Na pasta do projeto, crie e ative um ambiente virtual (recomendado).
3. Instale as dependências e inicie o aplicativo:

```bash
python -m pip install -r requirements.txt
python main.py
```

No macOS, também é possível usar `python3` em vez de `python`. Se o Kivy não iniciar, confirme que a instalação e a execução usam o mesmo Python: `python -m pip show kivy`.

### Criar ambiente virtual

**macOS/Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

**Windows (PowerShell)**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## Testes

Os testes matemáticos não precisam abrir a interface gráfica:

```bash
python -m unittest discover -s tests -v
```

## Publicar no GitHub

1. Crie um repositório vazio no GitHub.
2. Envie o conteúdo desta pasta (incluindo `README.md`, `LICENSE` e `.gitignore`) usando o GitHub Desktop ou Git.
3. Para Git, no terminal aberto na pasta do projeto:

```bash
git init
git add .
git commit -m "Publica aplicativo de gráfico de funções"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
git push -u origin main
```

Troque `SEU-USUARIO/SEU-REPOSITORIO` pelo endereço do repositório criado. Não envie `.venv`, chaves, senhas, arquivos de build ou dados pessoais.

## Android e iOS

O `buildozer.spec` está incluído como ponto de partida para Android. O empacotamento Kivy/Buildozer normalmente é realizado em Linux (ou WSL2 no Windows) com as dependências nativas instaladas; consulte a documentação atual do Buildozer antes de compilar. Para iOS é necessário macOS com Xcode e o fluxo de compilação/assinatura do Kivy iOS. **Este repositório contém o código-fonte, não APK/IPA prontos para instalar.**

## Estrutura

- `main.py` — interface Kivy e desenho do gráfico.
- `function_math.py` — cálculo das funções e características da quadrática.
- `tests/` — testes automatizados.
- `.github/workflows/` — execução dos testes em pushes e pull requests.
- `buildozer.spec` — configuração inicial para empacotamento Android.

## Licença

Distribuído sob a licença MIT. Consulte `LICENSE`.
