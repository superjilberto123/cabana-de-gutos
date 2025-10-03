# cabana-de-gutos
🔐 Gerador de Senhas Seguras
Um gerador de senhas moderno, intuitivo e altamente personalizável desenvolvido em HTML, CSS e JavaScript puro. Crie senhas fortes e seguras diretamente no navegador, sem necessidade de instalação ou conexão com a internet.

✨ Funcionalidades
Geração de Senhas*/

Geração Instantânea: Crie senhas seguras com um único clique
Comprimento Personalizável: Ajuste de 4 a 50 caracteres usando controle deslizante
Geração Automática: Senhas são geradas automaticamente ao mudar as configurações

Opções de Caracteres

✅ Letras maiúsculas (A-Z)
✅ Letras minúsculas (a-z)
✅ Números (0-9)
✅ Símbolos especiais (!@#$%^&*()_+-)
🚫 Exclusão de caracteres similares (0, O, l, 1, I)
🚫 Exclusão de caracteres ambíguos ({})

Recursos Avançados

Medidor de Força: Indicador visual em tempo real da segurança da senha

Fraca (vermelho)
Média (laranja)
Forte (verde)
Muito Forte (verde escuro)


Copiar com Um Clique: Botão dedicado para copiar senha para área de transferência
Histórico de Senhas: Visualize as últimas 5 senhas geradas com timestamp
Dicas de Segurança: Orientações integradas sobre boas práticas
Interface Responsiva: Design adaptável para desktop e mobile

🎨 Design

Interface moderna com efeito glassmorphism
Gradientes vibrantes e animações suaves
Tema roxo/azul com elementos em destaque
Experiência visual premium com backdrop blur
Transições e hover effects para melhor UX

🚀 Como Usar
Instalação

Baixe o arquivo gsenhas.html
Não é necessário instalar nada - funciona offline!

Uso Básico

Abrir: Dê um duplo clique no arquivo gsenhas.html ou abra-o em seu navegador
Configurar:

Ajuste o comprimento da senha movendo o controle deslizante
Marque/desmarque as opções de caracteres desejadas


Gerar: Clique em "🎲 Gerar Nova Senha" ou deixe a geração automática funcionar
Copiar: Use o botão "📋 Copiar" para transferir a senha para a área de transferência
Visualizar Histórico: Veja suas últimas 5 senhas geradas

Recursos Adicionais

Exclusão de Similares: Evita confusão entre 0/O, 1/l/I
Exclusão de Ambíguos: Remove caracteres que podem ser mal interpretados
Limpar Histórico: Remova todas as senhas salvas do histórico

📋 Requisitos

✅ Navegador web moderno (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
✅ JavaScript habilitado
❌ Nenhuma instalação necessária
❌ Nenhuma conexão com internet necessária
❌ Nenhuma dependência externa

🔒 Segurança e Privacidade
Recursos de Segurança

Algoritmo Robusto: Utiliza Math.random() para geração de caracteres aleatórios
Caracteres Garantidos: Assegura que pelo menos um caractere de cada tipo selecionado seja incluído
Embaralhamento: Senhas são embaralhadas após a geração para maior aleatoriedade
Cálculo de Força: Algoritmo sofisticado que considera comprimento, variedade e complexidade

Privacidade

✅ 100% Client-Side: Todo processamento ocorre localmente no navegador
✅ Sem Envio de Dados: Nenhuma informação é transmitida para servidores externos
✅ Sem Armazenamento Persistente: Histórico não é salvo permanentemente (apenas na sessão)
✅ Sem Cookies ou Tracking: Zero rastreamento de usuários

Observações

Nota: O histórico de senhas é armazenado apenas na memória durante a sessão. Ao fechar o navegador, todas as senhas do histórico são automaticamente apagadas. Para armazenamento permanente, considere usar um gerenciador de senhas dedicado.

💡 Boas Práticas de Senha
Recomendações do Gerador

Comprimento Mínimo: Use pelo menos 12 caracteres (ideal: 16+)
Variedade Máxima: Ative todos os tipos de caracteres
Senhas Únicas: Nunca reutilize senhas entre diferentes serviços
Gerenciador de Senhas: Use ferramentas como 1Password, LastPass ou Bitwarden
Autenticação 2FA: Sempre que disponível, habilite a verificação em duas etapas

Evite

❌ Informações pessoais (datas de nascimento, nomes)
❌ Palavras do dicionário
❌ Sequências óbvias (123456, qwerty)
❌ Senhas curtas (menos de 8 caracteres)

🛠️ Tecnologias Utilizadas

HTML5: Estrutura semântica moderna
CSS3:

Gradientes lineares
Backdrop filter (glassmorphism)
Transições e animações
Grid e Flexbox


JavaScript Vanilla:

Classes ES6
Event listeners
DOM manipulation
LocalStorage ready (implementação comentada)



📱 Compatibilidade
NavegadorVersão MínimaStatusChrome90+✅ Totalmente CompatívelFirefox88+✅ Totalmente CompatívelSafari14+✅ Totalmente CompatívelEdge90+✅ Totalmente CompatívelOpera76+✅ Totalmente Compatível
Responsividade

✅ Desktop (1920px+)
✅ Laptop (1366px - 1920px)
✅ Tablet (768px - 1366px)
✅ Mobile (320px - 768px)

🎯 Algoritmo de Força da Senha
O medidor de força considera:

Comprimento (até 25 pontos)
Variedade de caracteres (até 45 pontos):

Minúsculas: +10
Maiúsculas: +10
Números: +10
Símbolos: +15


Bônus por comprimento:

12+ caracteres: +10
16+ caracteres: +10
20+ caracteres: +10


Penalidade por repetição: -10 se menos de 70% dos caracteres são únicos

Total máximo: 100 pontos
Escala de Força

0-29: 🔴 Fraca
30-49: 🟠 Média
50-69: 🟢 Forte
70-100: 🟢 Muito Forte

🔧 Personalização
Modificar Cores
Edite as variáveis CSS no arquivo:
css/* Gradiente principal do fundo */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Gradiente dos títulos */
background: linear-gradient(45deg, #ff6b6b, #4ecdc4);

/* Gradiente dos botões */
background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
Adicionar Novos Símbolos
Localize a função getCharacterSets() e modifique:
javascriptsymbols: '!@#$%^&*()_+-=[]{}|;:,.<>?~`'
Aumentar Limite de Histórico
Altere na função addToHistory():
javascript// Mude de 5 para o número desejado
if (this.history.length > 5) {
    this.history = this.history.slice(0, 5);
}
📊 Estrutura do Código
gsenhas.html
│
├── <head>
│   └── <style>         # Estilos CSS (responsivo, glassmorphism)
│
├── <body>
│   ├── Seção de Configurações
│   │   ├── Controle de comprimento
│   │   └── Checkboxes de opções
│   │
│   ├── Botão de Geração
│   │
│   ├── Seção de Resultado
│   │   ├── Campo de senha
│   │   ├── Medidor de força
│   │   └── Histórico
│   │
│   └── Seção de Dicas
│
└── <script>
    └── Classe PasswordGenerator
        ├── generatePassword()      # Gera senha
        ├── calculateStrength()     # Calcula força
        ├── copyPassword()          # Copia para clipboard
        ├── addToHistory()          # Gerencia histórico
        └── Event Listeners         # Interatividade
🐛 Resolução de Problemas
Senha não está sendo gerada

Verifique se pelo menos uma opção de caracteres está marcada
Certifique-se de que JavaScript está habilitado no navegador

Botão copiar não funciona

Alguns navegadores exigem HTTPS para a funcionalidade de clipboard
Tente usar Ctrl+C manualmente após selecionar o texto

Design não aparece corretamente

Atualize seu navegador para a versão mais recente
Verifique se CSS está habilitado

📝 Licença
Este projeto está sob a licença MIT. Você é livre para:

✅ Usar comercialmente
✅ Modificar
✅ Distribuir
✅ Uso privado

👨‍💻 Desenvolvimento
Futuras Melhorias Possíveis

 Implementação de localStorage persistente
 Exportação de histórico em arquivo
 Modo escuro/claro
 Suporte a múltiplos idiomas
 PWA (Progressive Web App)
 Geração de passphrases
 Teste de senhas existentes

🤝 Contribuindo
Contribuições são bem-vindas! Para contribuir:

Faça um fork do projeto
Crie uma branch para sua feature (git checkout -b feature/NovaFuncionalidade)
Commit suas mudanças (git commit -m 'Adiciona nova funcionalidade')
Push para a branch (git push origin feature/NovaFuncionalidade)
Abra um Pull Request

📞 Suporte
Encontrou um bug ou tem uma sugestão?

Abra uma issue no repositório
Entre em contato através do email de suporte

⚠️ Aviso Legal
Este gerador de senhas é fornecido "como está", sem garantias de qualquer tipo. Embora seja projetado para criar senhas seguras, recomendamos:

Usar gerenciadores de senhas profissionais para armazenamento
Habilitar autenticação de dois fatores sempre que possível
Não compartilhar senhas através de canais inseguros
Alterar senhas regularmente em serviços críticos
