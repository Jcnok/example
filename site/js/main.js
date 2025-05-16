// Função para abrir o modal
function openModal(title, description) {
    document.getElementById('modal-title').innerText = title;
    document.getElementById('modal-description').innerText = description;
    document.getElementById('modal').style.display = 'block';
}

// Função para fechar o modal
function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

// Funcionalidade de envio do formulário
document.getElementById('contact-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Previne o comportamento padrão do formulário
    document.getElementById('loading').style.display = 'block'; // Mostra o loading

    // Simula um envio com setTimeout
    setTimeout(() => {
        document.getElementById('loading').style.display = 'none'; // Esconde o loading
        alert('Mensagem enviada com sucesso!'); // Mensagem de sucesso
    }, 2000);
});

// Suavização de rolagem
const links = document.querySelectorAll('nav a');
links.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        const targetSection = document.querySelector(targetId);
        targetSection.scrollIntoView({ behavior: 'smooth' });
    });
});