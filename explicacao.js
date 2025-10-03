/**
 * GERADOR DE SENHAS SEGURAS
 * Autores: Matheus Souza de Alencar, Jhonatha Luis
 * Sistema de geração de senhas com análise de segurança e histórico
 */

// Classe principal do gerador de senhas
class PasswordGenerator {
    // Inicializa o sistema
    constructor() {
        this.history = [];                    // Array para histórico de senhas
        this.updateHistoryDisplay();          // Atualiza exibição do histórico
        this.setupEventListeners();           // Configura eventos da interface
    }

    // Configura listeners para interatividade
    setupEventListeners() {
        // Atualiza display do slider ao mover
        const lengthSlider = document.getElementById('length');
        lengthSlider.addEventListener('input', (e) => {
            document.getElementById('lengthDisplay').textContent = e.target.value;
        });

        // Auto-regenera senha quando configurações mudam
        const settings = document.querySelectorAll('input[type="checkbox"], input[type="range"]');
        settings.forEach(setting => {
            setting.addEventListener('change', () => {
                if (document.getElementById('passwordField').value) {
                    this.generatePassword();
                }
            });
        });
    }

    // Retorna conjuntos de caracteres com filtros aplicados
    getCharacterSets() {
        // Define conjuntos base
        const sets = {
            uppercase: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            lowercase: 'abcdefghijklmnopqrstuvwxyz',
            numbers: '0123456789',
            symbols: '!@#$%^&*()_+-=[]{}|;:,.<>?'
        };

        // Caracteres para filtros
        const similar = '0O1lI';                          // Ex: O (letra) vs 0 (zero)
        const ambiguous = '{}[]()\/\\\'"`~,;.<>';        // Caracteres problemáticos

        // Aplica filtro de similares se marcado
        if (document.getElementById('excludeSimilar').checked) {
            Object.keys(sets).forEach(key => {
                sets[key] = sets[key].split('').filter(char => !similar.includes(char)).join('');
            });
        }

        // Aplica filtro de ambíguos se marcado
        if (document.getElementById('excludeAmbiguous').checked) {
            Object.keys(sets).forEach(key => {
                sets[key] = sets[key].split('').filter(char => !ambiguous.includes(char)).join('');
            });
        }

        return sets;
    }

    // Gera senha baseada nas configurações do usuário
    generatePassword() {
        const length = parseInt(document.getElementById('length').value);
        const sets = this.getCharacterSets();
        
        let availableChars = '';      // Todos os caracteres disponíveis
        let requiredChars = '';       // Garante pelo menos um de cada tipo

        // Constrói conjunto de caracteres baseado nas opções
        if (document.getElementById('uppercase').checked) {
            availableChars += sets.uppercase;
            requiredChars += this.getRandomChar(sets.uppercase);
        }
        if (document.getElementById('lowercase').checked) {
            availableChars += sets.lowercase;
            requiredChars += this.getRandomChar(sets.lowercase);
        }
        if (document.getElementById('numbers').checked) {
            availableChars += sets.numbers;
            requiredChars += this.getRandomChar(sets.numbers);
        }
        if (document.getElementById('symbols').checked) {
            availableChars += sets.symbols;
            requiredChars += this.getRandomChar(sets.symbols);
        }

        // Validação: precisa de pelo menos um tipo
        if (availableChars === '') {
            alert('Selecione pelo menos um tipo de caractere!');
            return;
        }

        // Constrói senha: inicia com obrigatórios e completa com aleatórios
        let password = requiredChars;
        for (let i = requiredChars.length; i < length; i++) {
            password += this.getRandomChar(availableChars);
        }

        // Embaralha para não deixar padrões previsíveis
        password = this.shuffleString(password);
        
        // Atualiza interface
        document.getElementById('passwordField').value = password;
        this.updateStrengthMeter(password);
        this.addToHistory(password);
    }

    // Retorna caractere aleatório de uma string
    getRandomChar(str) {
        return str[Math.floor(Math.random() * str.length)];
    }

    // Embaralha string usando algoritmo aleatório
    shuffleString(str) {
        return str.split('').sort(() => Math.random() - 0.5).join('');
    }

    // Atualiza medidor visual de força
    updateStrengthMeter(password) {
        const strength = this.calculateStrength(password);
        const strengthFill = document.getElementById('strengthFill');
        const strengthText = document.getElementById('strengthText');

        strengthFill.className = 'strength-fill';
        
        // Categoriza força em 4 níveis
        if (strength < 30) {
            strengthFill.classList.add('strength-weak');
            strengthText.textContent = 'Fraca';
        } else if (strength < 50) {
            strengthFill.classList.add('strength-medium');
            strengthText.textContent = 'Média';
        } else if (strength < 70) {
            strengthFill.classList.add('strength-strong');
            strengthText.textContent = 'Forte';
        } else {
            strengthFill.classList.add('strength-very-strong');
            strengthText.textContent = 'Muito Forte';
        }
    }

    // Calcula força usando múltiplos critérios
    calculateStrength(password) {
        let strength = 0;
        
        // Pontos por comprimento (máx 25)
        strength += Math.min(password.length * 2, 25);
        
        // Bônus por variedade de caracteres
        if (/[a-z]/.test(password)) strength += 10;           // Minúsculas
        if (/[A-Z]/.test(password)) strength += 10;           // Maiúsculas
        if (/[0-9]/.test(password)) strength += 10;           // Números
        if (/[^A-Za-z0-9]/.test(password)) strength += 15;    // Símbolos
        
        // Bônus por comprimento extra
        if (password.length >= 12) strength += 10;
        if (password.length >= 16) strength += 10;
        if (password.length >= 20) strength += 10;
        
        // Penalização por falta de variedade
        const uniqueChars = new Set(password).size;
        if (uniqueChars < password.length * 0.7) strength -= 10;
        
        return Math.min(strength, 100);
    }

    // Copia senha para área de transferência
    copyPassword() {
        const passwordField = document.getElementById('passwordField');
        const copyBtn = document.getElementById('copyBtn');
        
        if (passwordField.value === '') {
            alert('Gere uma senha primeiro!');
            return;
        }
        
        // Seleciona e copia
        passwordField.select();
        document.execCommand('copy');
        
        // Feedback visual por 2 segundos
        copyBtn.textContent = '✅ Copiado!';
        copyBtn.classList.add('copied');
        setTimeout(() => {
            copyBtn.textContent = '📋 Copiar';
            copyBtn.classList.remove('copied');
        }, 2000);
    }

    // Adiciona senha ao histórico com timestamp
    addToHistory(password) {
        const timestamp = new Date().toLocaleString('pt-BR');
        this.history.unshift({ password, timestamp });    // Adiciona no início
        
        // Mantém apenas as últimas 5
        if (this.history.length > 5) {
            this.history = this.history.slice(0, 5);
        }
        
        this.updateHistoryDisplay();
    }

    // Atualiza exibição do histórico na tela
    updateHistoryDisplay() {
        const historyList = document.getElementById('historyList');
        
        if (this.history.length === 0) {
            historyList.innerHTML = '<p style="opacity: 0.7; text-align: center;">Nenhuma senha gerada ainda</p>';
            return;
        }
        
        // Cria HTML para cada item do histórico
        historyList.innerHTML = this.history.map(item => `
            <div class="history-item">
                <span>${item.password}</span>
                <small style="opacity: 0.7;">${item.timestamp}</small>
            </div>
        `).join('');
    }

    // Limpa histórico após confirmação
    clearHistory() {
        if (confirm('Tem certeza que deseja limpar o histórico?')) {
            this.history = [];
            this.updateHistoryDisplay();
        }
    }
}

// Instância global do gerador
const passwordGen = new PasswordGenerator();

// Funções globais para interface HTML
function generatePassword() {
    passwordGen.generatePassword();
}

function copyPassword() {
    passwordGen.copyPassword();
}

function clearHistory() {
    passwordGen.clearHistory();
}

// Gera senha inicial ao carregar página
window.addEventListener('load', () => {
    passwordGen.generatePassword();
});
