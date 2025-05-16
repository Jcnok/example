# site_creator_agent.py
import os
from langchain_openai import AzureChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import BaseTool
from typing import List, Optional

class SiteCreatorAgent:
    def __init__(self):
        self.llm = self._setup_llm()
        self.tools = self._setup_tools()
        self.agent = self._setup_agent()
        
    def _setup_llm(self):
        return AzureChatOpenAI(
            openai_api_version="2025-01-01-preview",
            azure_deployment=os.getenv("DEPLOYMENT_NAME"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            temperature=0.7
        )
    
    def _setup_tools(self):
        return [
            CreateHTMLTool(),
            CreateCSSTool(),
            CreateJSTool()
        ]
    
    def _setup_agent(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um especialista em desenvolvimento web front-end.
            Regras obrigatórias:
            1. Todas as referências CSS devem usar o caminho 'css/style.css'
            2. Todos os scripts JavaScript devem usar o caminho 'js/main.js'
            3. Usar tags semânticas HTML5
            4. Layout responsivo com media queries
            5. Meta tags para SEO e otimização de mecanismos de busca"""),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_openai_functions_agent(self.llm, self.tools, prompt)
        return AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=self.tools,
            verbose=True
        )
    
    def run(self, query):
        return self.agent.invoke({"input": query})

class CreateHTMLTool(BaseTool):
    name: str = "create_html"
    description: str = "Cria o arquivo HTML principal do site de portfólio"
    
    def _run(self, content: Optional[str] = None) -> str:
        if not content:
            prompt = """Crie um HTML básico para um site de portfólio profissional com:
            1. Seções para sobre, projetos, habilidades e contato
            2. Links corretos para CSS em 'css/style.css'
            3. Scripts corretos para JavaScript em 'js/main.js'
            4. Tags semânticas e meta tags para SEO
            5. Estrutura responsiva usando CSS moderno"""
            
            content = self.llm.invoke(prompt).content
            
        # Garante os caminhos corretos
        content = content.replace('href="styles.css"', 'href="css/style.css"')
        content = content.replace('src="script.js"', 'src="js/main.js"')
        content = content.replace('href="./styles.css"', 'href="css/style.css"')
        content = content.replace('src="./script.js"', 'src="js/main.js"')

        # Verificação pós-criação
        if 'css/style.css' not in content:
            content = content.replace('</head>', '<link rel="stylesheet" href="css/style.css"></head>')
        
        if 'js/main.js' not in content:
            content = content.replace('</body>', '<script src="js/main.js"></script></body>')

        os.makedirs("site", exist_ok=True)
        with open("site/index.html", "w") as f:
            f.write(content)
        return "Arquivo HTML criado com sucesso em site/index.html"

class CreateCSSTool(BaseTool):
    name: str = "create_css"
    description: str = "Cria o arquivo CSS para estilizar o site de portfólio"
    
    def _run(self, content: Optional[str] = None) -> str:
        if not content:
            content = """/* Estilos principais */
:root {
    --primary-color: #2A2A2A;
    --secondary-color: #F5F5F5;
}

body {
    font-family: 'Segoe UI', sans-serif;
    margin: 0;
    padding: 0;
}"""
        
        os.makedirs("site/css", exist_ok=True)
        with open("site/css/style.css", "w") as f:
            f.write(content)
        return "Arquivo CSS criado com sucesso em site/css/style.css"

class CreateJSTool(BaseTool):
    name: str = "create_js"
    description: str = "Cria o arquivo JavaScript para adicionar interatividade ao site"
    
    def _run(self, content: Optional[str] = None) -> str:
        if not content:
            content = """// Animação suave de scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});"""
        
        os.makedirs("site/js", exist_ok=True)
        with open("site/js/main.js", "w") as f:
            f.write(content)
        return "Arquivo JavaScript criado com sucesso em site/js/main.js"
