document.getElementById('submitButton').addEventListener('click', function (event) {
    event.preventDefault();
    validarFormulario();
});

function validarFormulario() {
    const form = document.getElementById('cadastroForm');
    const nome = form.nome.value.trim();
    const cpf = form.cpf.value.trim();
    const email1 = form.email1.value.trim();
    const username = form.username.value.trim(); // Utiliza o campo username
    const senha1 = form.senha1.value.trim();
    const senha2 = form.senha2.value.trim();
    const telefone = form.telefone.value.trim();
    const checagem = form.checagem.checked;
    const erro = document.getElementById('erro');

    erro.textContent = '';

    if (!nome) {
        erro.textContent = 'Por favor, digite seu nome.';
        form.nome.focus();
        return;
    }

    if (!cpf) {
        erro.textContent = 'Por favor, digite seu CPF.';
        form.cpf.focus();
        return;
    }

    if (cpf.length !== 11) {
        erro.textContent = 'O CPF deve ter 11 dígitos.';
        form.cpf.focus();
        return;
    }

    if (!email1) {
        erro.textContent = 'Por favor, digite seu email.';
        form.email1.focus();
        return;
    }

    if (!username) {
        erro.textContent = 'Por favor, digite um nome de usuário.';
        form.username.focus();
        return;
    }

    if (username.includes(' ')) {
        erro.textContent = 'O nome de usuário não pode conter espaços.';
        form.username.focus();
        return;
    }

    if (!senha1) {
        erro.textContent = 'Por favor, digite sua senha.';
        form.senha1.focus();
        return;
    }

    if (senha1 !== senha2) {
        erro.textContent = 'As senhas não coincidem.';
        form.senha2.focus();
        return;
    }

    if (!telefone) {
        erro.textContent = 'Por favor, digite seu telefone.';
        form.telefone.focus();
        return;
    }

    if (telefone.length !== 11) {
        erro.textContent = 'O número de telefone deve ter 11 dígitos.';
        form.telefone.focus();
        return;
    }

    if (!checagem) {
        erro.textContent = 'Você deve aceitar os termos de compromisso.';
        form.checagem.focus();
        return;
    }

    form.submit();
}
