# devops_agent.py
import os
import git
import yaml
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import BaseTool

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

class DevOpsAgent:
    def __init__(self):
        self.llm = self._setup_llm()
        self.tools = self._setup_tools()
        self.agent = self._setup_agent()
        
    def _setup_llm(self):
        return AzureChatOpenAI(
            openai_api_version=os.getenv("OPENAI_API_VERSION", "2024-05-01-preview"),
            azure_deployment=os.getenv("DEPLOYMENT_NAME"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            temperature=0.7
        )
    
    def _setup_tools(self):
        return [
            CommitChangesTool(),
            PushToGitHubTool(),
            InfraAsCodeTool()
        ]
    
    def _setup_agent(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um especialista em DevOps e automação de CI/CD.
            Responsabilidades principais:
            1. Gerenciar commits semânticos
            2. Realizar push para branch main
            3. Garantir integridade do repositório"""),
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

class CommitChangesTool(BaseTool):
    name: str = "commit_changes"
    description: str = "Adiciona e comita mudanças seguindo Conventional Commits"
    
    def _generate_commit_message(self, repo):
        diff = repo.git.diff('HEAD')
        message_type = "chore"
        
        if any(f in diff for f in ['site/content/', 'site/docs/']):
            message_type = "docs(content)"
        elif any(f in diff for f in ['site/styles/', 'site/components/']):
            message_type = "feat(ui)"
        elif 'src/devops_agent.py' in diff:
            message_type = "chore(devops)"
            
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"{message_type}: atualização automática {timestamp}"

    def _run(self) -> str:
        try:
            repo = git.Repo(os.getcwd())
            
            if not repo.is_dirty() and not repo.untracked_files:
                return "Nenhuma alteração detectada para commit"

            commit_message = self._generate_commit_message(repo)
            
            repo.git.add(all=True)
            repo.git.config('user.name', os.getenv("GITHUB_USERNAME"))
            repo.git.config('user.email', os.getenv("GITHUB_EMAIL"))
            repo.git.commit('-m', commit_message)
            return f"Commit realizado: {commit_message}"
        except Exception as e:
            return f"Erro no commit: {str(e)}"

class PushToGitHubTool(BaseTool):
    name: str = "push_to_github"
    description: str = "Envia alterações para a branch main do GitHub"
    
    def _run(self) -> str:
        try:
            repo = git.Repo(os.getcwd())
            remote_url = (
                f"https://{os.getenv('GITHUB_USERNAME')}:{os.getenv('GITHUB_TOKEN')}"
                f"@github.com/{os.getenv('GITHUB_USERNAME')}/{os.getenv('GITHUB_REPO')}.git"
            )
            
            if 'origin' not in repo.remotes:
                origin = repo.create_remote('origin', remote_url)
            else:
                origin = repo.remotes.origin
                origin.set_url(remote_url)
            
            origin.push(refspec='main:main', force=False)
            return "Push realizado com sucesso para a branch main"
        except Exception as e:
            return f"Erro no push: {str(e)}"

class InfraAsCodeTool(BaseTool):
    name: str = "infra_as_code"
    description: str = "Configuração idempotente de CI/CD"
    
    def _workflow_version(self):
        return "1.2.0"
    
    def _create_workflow(self, workflow_dir):
        workflow_content = {
            'name': 'Deploy to GitHub Pages',
            'on': {
                'push': {
                    'branches': ['main'],
                    'paths': ['site/**']
                }
            },
            'env': {
                'GH_TOKEN': '${{ secrets.GITHUB_TOKEN }}',
                'TZ': 'America/Sao_Paulo'
            },
            'jobs': {
                'build-and-deploy': {
                    'runs-on': 'ubuntu-latest',
                    'permissions': {
                        'contents': 'write',
                        'pages': 'write',
                        'id-token': 'write'
                    },
                    'steps': [
                        {
                            'name': 'Checkout',
                            'uses': 'actions/checkout@v4'
                        },
                        {
                            'name': 'Deploy to GitHub Pages',
                            'uses': 'JamesIves/github-pages-deploy-action@v4',
                            'with': {
                                'folder': 'site'
                            }
                        }
                    ]
                }
            },
            #'metadata': {
            #    'version': self._workflow_version(),
            #    'created_by': 'AI DevOps Agent'
            #}
        }
        
        workflow_path = os.path.join(workflow_dir, 'deploy.yml')
        with open(workflow_path, 'w') as f:
            yaml.safe_dump(workflow_content, f, sort_keys=False, default_flow_style=False)
    
    def _run(self) -> str:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        workflow_dir = os.path.join(project_root, '.github', 'workflows')
        os.makedirs(workflow_dir, exist_ok=True)
        
        workflow_path = os.path.join(workflow_dir, 'deploy.yml')
        
        if os.path.exists(workflow_path):
            with open(workflow_path, 'r') as f:
                existing_config = yaml.safe_load(f)
                if existing_config.get('metadata', {}).get('version') == self._workflow_version():
                    return "Workflow já está atualizado"
        
        self._create_workflow(workflow_dir)
        return "Workflow de deploy configurado/atualizado com sucesso"

if __name__ == "__main__":
    agent = DevOpsAgent()
    print("Iniciando DevOps Agent...")
    result = agent.run("Configurar pipeline completo com deploy na branch githubpages")
    print("\nResultado final:", result)
