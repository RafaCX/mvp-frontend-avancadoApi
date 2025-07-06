# 🧠 Backend da Minha Biblioteca (API REST + Integração com Google Books)

Este projeto é o **back-end** da aplicação **Minha Biblioteca**. Ele atua como intermediário entre o front-end (React) e a **API pública do Google Books**, permitindo buscar livros e integrar dados de forma controlada e segura.

## 🎯 Objetivo

- Facilitar a comunicação com a API do Google Books.
- Servir dados de forma estruturada ao front-end React.

## 🌐 Integração com API Externa

Este back-end acessa a API **Google Books** para buscar livros pelo título:

- **API Externa:** [Google Books](https://developers.google.com/books/docs/v1/using)
- **URL base:** `https://www.googleapis.com/books/v1/volumes?q=`
- **Rota criada no back-end:**

## Requisitos

Antes de executar a aplicação, certifique-se de ter:

- Python instalado na versão 3.7 ou superior.
- `pip` configurado corretamente para gerenciar pacotes Python.
- As dependências listadas no arquivo `requirements.txt`.

Recomenda-se fortemente o uso de um ambiente virtual para evitar conflitos de dependências.

---

## Configuração do Ambiente

Siga os passos abaixo para configurar e executar a API:

1. Crie um ambiente virtual:
   ```bash
   python -m venv env
   ```
2. Ative o ambiente virtual:
   - **Linux/macOS**:
     ```bash
     source env/bin/activate
     ```
   - **Windows**:
     ```cmd
     .\env\Scripts\Activate
     ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Instale o Swagger (documentação automática):
   ```bash
   pip install -U flask-openapi3-swagger
   ```

---

## Executando a API

1. Inicie o servidor Flask:
   ```bash
   flask run --host 0.0.0.0 --port 5000 --reload
   ```

   O parâmetro `--reload` é útil em modo de desenvolvimento, pois reinicia o servidor automaticamente ao detectar mudanças no código.

2. Acesse a API no navegador ou por ferramentas como **Postman** ou **cURL**:
   - [http://localhost:5000/#/](http://localhost:5000/#/)