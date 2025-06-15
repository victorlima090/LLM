# Chatbot com LangGraph e Gemini

Este projeto é um chatbot interativo desenvolvido em Python utilizando [Streamlit](https://streamlit.io/), [LangGraph](https://github.com/langchain-ai/langgraph) e o modelo Gemini da Google. O usuário pode escolher o nível de educação do atendente (Educado, Neutro ou Mal-Educado) e interagir com o modelo em tempo real.

## Estrutura do Projeto

- `streamlit_app.py`: Código principal da aplicação Streamlit.
- `PD.ipynb`: Notebook com explicações e conceitos fundamentais sobre LLMs.
- `0.2.27`: Arquivo de log ou instalação de dependências.
- `.env`: Variáveis de ambiente.
- `__pycache__/`: Arquivos de cache do Python.

## Como Executar

1. Instale as dependências necessárias:
    ```sh
    pip install streamlit langchain langgraph google-generativeai
    ```
2. Execute o aplicativo:
    ```sh
    streamlit run streamlit_app.py
    ```

3. Acesse o chatbot pelo navegador no endereço exibido pelo Streamlit.

## Funcionalidades

- Seleção do nível de educação do atendente.
- Histórico de mensagens.
- Integração com o modelo Gemini da Google.
- Interface simples e intuitiva.

## Observações

- O arquivo `0.2.27` parece conter logs ou informações de instalação de pacotes.
- O notebook `PD.ipynb` traz explicações teóricas sobre LLMs, Transformers, Attention, Fine-Tuning, etc.

## Licença

Este projeto é apenas para fins educacionais.

---

Desenvolvido por Victor Coelho Lima