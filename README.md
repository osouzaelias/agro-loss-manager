#  AgroLoss Manager: Gestão de Perdas na Colheita

---

## 1. Visão Geral do Projeto

O **AgroLoss Manager** é uma aplicação web full-stack desenvolvida para atender a uma necessidade crítica do agronegócio brasileiro: o monitoramento e a redução de perdas na colheita de cana-de-açúcar. O Brasil, apesar de ser líder mundial na produção, enfrenta perdas que podem chegar a 15% durante a colheita mecanizada, representando um prejuízo significativo para os produtores.

Esta solução oferece uma plataforma intuitiva para que gestores agrícolas possam registrar dados de cada operação de colheita, visualizar um histórico consolidado e gerar relatórios para análise, auxiliando na tomada de decisões estratégicas para otimizar a produtividade.

## 2. Principais Funcionalidades

* **Interface Web Reativa:** Um front-end limpo e interativo, construído com HTML, CSS e JavaScript, que permite cadastrar e visualizar os registros sem a necessidade de recarregar a página.
* **API RESTful Robusta:** Um back-end desenvolvido com **FastAPI** que serve os dados para a interface e pode ser integrado a outras ferramentas.
* **Documentação Automática:** A API conta com documentação interativa (Swagger UI) disponível em `/docs`, facilitando testes e o entendimento dos endpoints.
* **Persistência de Dados:** Os registros são armazenados de forma segura em um banco de dados local **SQLite**, garantindo simplicidade na configuração e portabilidade.
* **Geração e Download de Relatórios:** A funcionalidade de "Gerar Relatório" cria um arquivo de texto (`.txt`) consolidado e o disponibiliza para download imediato no navegador.
* **Qualidade de Código Garantida:** O projeto inclui uma suíte de testes unitários e de integração com **Pytest** para validar a lógica de negócio, os casos de uso e os endpoints da API.

## 3. Arquitetura e Tech Stack

O projeto foi estruturado seguindo os princípios da **Clean Architecture**, garantindo uma separação clara de responsabilidades, alta testabilidade e fácil manutenção.

* **`Domain`**: Contém as regras de negócio e entidades puras, sem dependências externas.
* **`Application`**: Orquestra os fluxos de dados através dos Casos de Uso.
* **`Infrastructure`**: Implementa os detalhes técnicos, como o acesso ao banco de dados SQLite.
* **`Presentation`**: Camada de entrada da aplicação, composta pela API FastAPI e pelo front-end (arquivos estáticos e templates).

| Camada       | Tecnologias Utilizadas                                |
| :----------- | :---------------------------------------------------- |
| **Back-end** | Python 3, FastAPI, Uvicorn, Pydantic, SQLite          |
| **Front-end**| HTML5, CSS3, JavaScript (Vanilla JS)                  |
| **Testes** | Pytest                                                |

## 4. Como Executar o Projeto

Siga os passos abaixo para configurar e executar a aplicação em seu ambiente local.

### Pré-requisitos
* Python 3.8 ou superior

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [URL-DO-SEU-REPOSITORIO]
    cd agro-loss-manager
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Comando para MacOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # Comando para Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências do projeto:**
    ```bash
    pip install -r requirements.txt
    ```

### Execução

1.  **Inicie o servidor da API:**
    ```bash
    uvicorn main:app --reload
    ```
    O servidor estará rodando e acessível em `http://127.0.0.1:8000`.

2.  **Acesse a aplicação:**
    Abra seu navegador e acesse: **`http://127.0.0.1:8000`**

3.  **Acesse a documentação da API (Swagger UI):**
    Para interagir diretamente com os endpoints da API, acesse: **`http://127.0.0.1:8000/docs`**

## 5. Checklist de Requisitos da Atividade (FIAP)

Esta seção detalha como o projeto atende a todos os critérios de avaliação da atividade "Cap 6 - Python e além".

1. [x] **Lógica Clara e Objetiva:** A aplicação da Clean Architecture garante que cada componente tenha uma responsabilidade única, resultando em um código organizado e de fácil entendimento.
2. [x] **Relevância com o Pedido:** A solução aborda diretamente um problema real e documentado do agronegócio: as perdas na colheita de cana-de-açúcar.
3. [x] **Inovação na Proposta:** O projeto evoluiu de um simples script para uma aplicação web full-stack completa, com API, interface reativa, banco de dados e testes automatizados, demonstrando uma solução moderna e robusta.
4. [x] **Consistência dos Dados de Entrada:** A validação ocorre em duas frentes: no front-end (com atributos HTML como `required` e `type="number"`) e no back-end (com os modelos Pydantic do FastAPI, que garantem o tipo e o formato dos dados).
5. [x] **Usabilidade e Clareza na Apresentação dos Dados:** A interface web é limpa, intuitiva e fornece feedback visual para o usuário (mensagens de sucesso/erro, desabilitação de botões durante ações), tornando a experiência de uso fluida.
6. [x] **Subalgoritmos (Funções e Procedimentos):** O código é totalmente modularizado em funções e classes, como os Casos de Uso (`CadastrarColheita`, `ListarColheitas`) e os Serviços de Domínio (`calcular_perda`).
7. [x] **Estruturas de Dados:** O projeto utiliza listas para agrupar registros, dicionários para transferência de dados entre camadas e objetos (dataclasses) para representar as entidades de negócio.
8. [x] **Manipulação de Arquivos:** A persistência de dados é feita via **SQLite**, que opera sobre um arquivo de banco de dados (`.db`). Além disso, a funcionalidade de relatório gera e manipula um arquivo de texto (`.txt`) que é enviado para download.
9. [x] **Conexão com Banco de Dados:** Embora o requisito original mencionasse Oracle, a opção por **SQLite** foi uma decisão de design para garantir a portabilidade e a facilidade de execução do projeto sem a necessidade de um SGBD externo. A arquitetura (Repository Pattern) permite que o banco de dados seja trocado para Oracle com esforço mínimo, alterando apenas a implementação na camada de infraestrutura.