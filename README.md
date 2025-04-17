
# 📊 Censo Escolar API

API REST em Flask para leitura, escrita e gerenciamento de instituições de ensino dos estados da Paraíba, Pernambuco e Rio Grande do Norte com base nos dados do Censo Escolar 2024.

---

## 🧰 Requisitos

- Python 3 instalado (preferencialmente 3.8+)
- `virtualenv` instalado globalmente (`pip install virtualenv`)

---

## ⚙️ Configuração do ambiente

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/CensoEscolarApi.git
cd CensoEscolarApi
```

### 2. Crie o ambiente virtual
```bash
virtualenv venv
```

### 3. Ative o ambiente virtual

- **Linux/macOS:**
  ```bash
  source venv/bin/activate
  ```

- **Windows:**
  ```cmd
  venv\Scripts\activate
  ```

---

## 📦 Instalação das dependências

Com o ambiente virtual ativado, execute:

```bash
pip install -r requirements.txt
```

---

## 🚀 Executando a aplicação

Você pode rodar o projeto de duas formas:

### ✅ 1. Diretamente com o Python

```bash
python3 app.py
```

> 🔹 Essa opção inicia a aplicação com `debug=False` (modo de desenvolvimento desativado por padrão).

> 🔹 Para ativar o modo de depuração use app.run(debug=True)

---

### ✅ 2. Utilizando o Flask CLI

#### Linux/macOS:
```bash
flask run # Ou se quiser com o modo de depuração ativado: flask run --debug
```

#### Windows (CMD):
```cmd
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```

---

## ⚠️ Avisos sobre o modo debug

- `FLASK_ENV=development` ou `debug=True` ativa o modo de desenvolvimento:
  - Código é recarregado automaticamente a cada alteração.
  - Erros são exibidos com detalhes no navegador.
  - **⚠️ Não utilizar em produção!**

- Para desativar o modo debug:
  - Use `set FLASK_ENV=production` (Windows) ou `export FLASK_ENV=production` (Linux/macOS).
  - Ou defina `debug=False` diretamente no `app.run()`.

---

## 📮 Endpoints da API

| Método | Rota                                						| Descrição                         |
|--------|------------------------------------------------|-----------------------------------|
| GET    | `/instituicoesensino`              						| Lista todas as instituições       |
| GET    | `/instituicoesensino/<co_instituicao>`         | Busca uma instituição por código  |
| POST   | `/instituicoesensino`              						| Adiciona uma nova instituição     |
| PUT    | `/instituicoesensino/<co_instituicao>`         | Atualiza uma instituição existente|
| DELETE | `/instituicoesensino/<co_instituicao>`         | Remove uma instituição existente  |

---

## 📝 Licença

Este projeto é livre para fins educacionais e acadêmicos.
