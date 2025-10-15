document.addEventListener('DOMContentLoaded', () => {
    // URL base da sua API.
    const API_URL = 'http://127.0.0.1:8000/api';

    // Elementos do DOM
    const form = document.getElementById('colheita-form');
    const listaColheitas = document.getElementById('colheitas-lista');
    const btnAtualizar = document.getElementById('btn-atualizar');
    const btnGerarRelatorio = document.getElementById('btn-gerar-relatorio');
    const mensagemDiv = document.getElementById('mensagem');
    const btnAdicionar = document.getElementById('btn-adicionar');

    const calcularPerda = (potencial, colhido) => {
        if (potencial <= 0) return 0;
        const perda = ((potencial - colhido) / potencial) * 100;
        return Math.max(0, perda).toFixed(2);
    };

    const exibirMensagem = (texto, tipo = 'sucesso') => {
        mensagemDiv.textContent = texto;
        mensagemDiv.className = tipo === 'sucesso' ? 'mensagem-sucesso' : 'mensagem-erro';
        setTimeout(() => {
            mensagemDiv.className = '';
            mensagemDiv.textContent = '';
        }, 4000);
    };

    const carregarColheitas = async () => {
        if (btnAtualizar) {
            btnAtualizar.disabled = true;
            btnAtualizar.textContent = 'Atualizando...';
        }

        try {
            const response = await fetch(`${API_URL}/colheitas`);
            if (!response.ok) {
                throw new Error(`Falha ao buscar dados (status: ${response.status})`);
            }

            const dados = await response.json();

            if (!listaColheitas) return;
            listaColheitas.innerHTML = '';

            if (dados.length === 0) {
                listaColheitas.innerHTML = '<tr><td colspan="7" style="text-align:center;">Nenhum registro encontrado.</td></tr>';
                return;
            }

            dados.forEach(colheita => {
                const perda = calcularPerda(colheita.toneladas_potenciais, colheita.toneladas_colhidas);
                const linha = `
                    <tr>
                        <td>${colheita.id}</td>
                        <td>${colheita.id_talhao}</td>
                        <td>${colheita.maquina}</td>
                        <td>${colheita.operador}</td>
                        <td>${colheita.toneladas_potenciais.toFixed(2)}</td>
                        <td>${colheita.toneladas_colhidas.toFixed(2)}</td>
                        <td>${perda}%</td>
                    </tr>
                `;
                listaColheitas.innerHTML += linha;
            });

            exibirMensagem('Lista de registros atualizada!', 'sucesso');

        } catch (error) {
            exibirMensagem(`Erro de rede: ${error.message}`, 'erro');
            console.error("Detalhes do erro:", error);
        } finally {

            if (btnAtualizar) {
                btnAtualizar.disabled = false;
                btnAtualizar.textContent = 'Atualizar Lista';
            }

        }
    };

    if (form) {
        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            if (btnAdicionar.disabled) return;
            btnAdicionar.disabled = true;
            btnAdicionar.textContent = 'Enviando...';

            const formData = new FormData(form);
            const dados = {
                id_talhao: formData.get('id_talhao'),
                maquina: formData.get('maquina'),
                operador: formData.get('operador'),
                toneladas_potenciais: parseFloat(formData.get('toneladas_potenciais')),
                toneladas_colhidas: parseFloat(formData.get('toneladas_colhidas')),
            };

            try {
                const response = await fetch(`${API_URL}/colheitas`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(dados),
                });

                if (!response.ok) {
                    const erroData = await response.json();
                    throw new Error(erroData.detail || 'Falha ao cadastrar registro.');
                }

                form.reset();
                // A mensagem de sucesso da atualização da lista já serve como feedback
                await carregarColheitas();
            } catch (error) {
                exibirMensagem(`Erro: ${error.message}`, 'erro');
            } finally {
                btnAdicionar.disabled = false;
                btnAdicionar.textContent = 'Adicionar Registro';
            }
        });
    }

    if (btnGerarRelatorio) {
        btnGerarRelatorio.addEventListener('click', async () => {
            btnGerarRelatorio.disabled = true;
            btnGerarRelatorio.textContent = 'Gerando...';
            try {
                const response = await fetch(`${API_URL}/colheitas/gerar-relatorio`, {method: 'POST'});

                if (!response.ok) {
                    const erroData = await response.json();
                    throw new Error(erroData.detail || 'Falha ao gerar relatório.');
                }

                // Pega o conteúdo do arquivo da resposta
                const blob = await response.blob();
                // Cria uma URL temporária para o conteúdo
                const downloadUrl = window.URL.createObjectURL(blob);
                // Cria um link invisível
                const link = document.createElement('a');
                link.href = downloadUrl;
                // Define o nome do arquivo que será baixado
                link.setAttribute('download', 'relatorio_perdas.txt');
                // Adiciona o link ao corpo do documento
                document.body.appendChild(link);
                // Simula um clique no link para iniciar o download
                link.click();
                // Remove o link após o download
                link.remove();
                // Libera a URL temporária
                window.URL.revokeObjectURL(downloadUrl);

                exibirMensagem('Download do relatório iniciado.', 'sucesso');

            } catch (error) {
                exibirMensagem(`Erro: ${error.message}`, 'erro');
            } finally {
                btnGerarRelatorio.disabled = false;
                btnGerarRelatorio.textContent = 'Gerar Relatório (.txt)';
            }
        });
    }

    if (btnAtualizar) {
        btnAtualizar.addEventListener('click', carregarColheitas);
    }

    carregarColheitas();
});