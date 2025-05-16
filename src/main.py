# main.py
from site_creator_agent import SiteCreatorAgent
from devops_agent import DevOpsAgent
from dotenv import load_dotenv
import os

def validate_environment():
    required_vars = [
        "AZURE_OPENAI_API_KEY",
        "GITHUB_USERNAME",
        "GITHUB_EMAIL",
        "GITHUB_TOKEN",
        "GITHUB_REPO"
    ]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        print(f"⚠️ Variáveis de ambiente obrigatórias não definidas: {', '.join(missing)}")
        print("Por favor, configure-as no arquivo .env e tente novamente.")
        return False
    return True

def main():
    load_dotenv()
    
    if not validate_environment():
        return
    
    print("🚀 Iniciando sistema de portfólio automatizado com IA")
    
    # Inicializar agentes
    site_creator = SiteCreatorAgent()
    devops_agent = DevOpsAgent()
    
    # Etapa 1: Criar o site de portfólio
    print("\n📝 Agente Criador de Site em ação...")
    site_result = site_creator.run(
        """
            Instruções Principais:
            Crie um site portfolio profissional responsivo (inspirado em https://jcnok.github.io/portfolio/) com:
            1. Estrutura HTML Semântica:
            Cabeçalho Fixo: Com logo (nome do usuário) e menu de navegação suave (Home, Projetos, Habilidades, Contato).
            Seção Hero:
            Layout em grid (50% texto / 50 por cento imagem) para dispositivos grandes.
            Título principal + subtítulo + Call-to-Action ("Ver Projetos").
            Avatar circular com borda gradiente (efeito de brilho suave via CSS).
            Seção Projetos:
            Grid responsivo (3 colunas desktop → 1 coluna mobile) com cards clicáveis.
            Cada card deve ter:
            Imagem em destaque (placeholder via https://placehold.co).
            Tags de tecnologia (ex: "React", "Python") com hover effect.
            Overlay dinâmico (ao clicar, exibir modal com descrição via JavaScript).
            Seção Contato:
            Formulário com campos (Nome, E-mail, Mensagem) e validação básica (JS).
            Efeito de suavização ao enviar (ex: loading spinner com CSS animation).
            2. Estilização CSS Moderna:
            Variáveis CSS: Para cores principais (ex: --primary-color: #2ecc71;).
            Design Gradiente: Use gradientes sutis em botões/bordas.
            Animações:
            Fade-in ao rolar a página (Intersection Observer API).
            Hover em cards com transform: translateY(-5px).
            Mobile-First: Media queries para breakpoints (768px, 1024px).
            3. Funcionalidades JavaScript:
            Scroll Suave: Navegação entre seções com scrollIntoView({behavior: 'smooth'}).
            Modal Dinâmico: Exibir detalhes do projeto ao clicar no card (conteúdo via JSON externo).
            Formulário:
            Prevenção de comportamento padrão.
            Simulação de envio com setTimeout() + mensagem de sucesso.
            4. Requisitos Técnicos:
            SEO Básico: Meta tags (description, keywords) e título otimizado.
            Ícones: Biblioteca Font Awesome para redes sociais (footer fixo).
            Clean Code: Código comentado e organizado em seções.
            5. Personalização:
            Use placeholders (nome, links, projetos) marcados com [SEU_NOME], [SEU_EMAIL] etc.
            Inclua comentários "// MODIFIQUE AQUI" nas áreas de personalização."""
            )
    
    print(f"Resultado do Agente Criador: {site_result}")
    
    # Etapa 2: Configurar Git e GitHub Actions
    print("\n🔧 Agente DevOps em ação...")
    devops_result = devops_agent.run(
        "Configure um repositório Git para este projeto, comite as mudanças e "
        "configure o GitHub Actions para fazer deploy automático no GitHub Pages "
        "sempre que houver um push para a branch main."
    )
    print(f"Resultado do Agente DevOps: {devops_result}")
    
    print("\n✅ Sistema de portfólio automatizado concluído com sucesso!")
    print("Seu site está pronto e configurado para deploy automático no GitHub Pages.")
    print(f"Acesse: https://{os.getenv('GITHUB_USERNAME')}.github.io/{os.getenv('GITHUB_REPO')}")

if __name__ == "__main__":
    main()
