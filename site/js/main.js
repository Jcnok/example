// Seleciona os elementos necessários
const contactForm = document.getElementById('contact-form');
const loadingMessage = document.getElementById('loading');

// Adiciona evento de envio ao formulário
contactForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Previne o comportamento padrão do formulário
    loadingMessage.style.display = 'block'; // Mostra a mensagem de loading

    // Simula um envio com setTimeout()
    setTimeout(() => {
        loadingMessage.style.display = 'none'; // Esconde a mensagem de loading
        alert('Mensagem enviada com sucesso!'); // Mensagem de sucesso
        contactForm.reset(); // Limpa o formulário
    }, 2000);
});

// Scroll suave para as seções
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Modal dinâmico para projetos (a ser implementado)
// MODIFIQUE AQUI para adicionar a lógica do modal