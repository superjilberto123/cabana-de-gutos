import tkinter as tk
from tkinter import ttk
import random
import time

class JogoMagiaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔮 Batalha Arcana dos Magos 🔮")
        self.root.geometry("800x700")
        self.root.configure(bg='#1a0d33')  # Fundo roxo escuro místico
        
        # Configuração de estilo
        self.setup_styles()
        
        # Estados do jogo
        self.vida_jogador = 100
        self.vida_inimigo = 100
        self.max_vida = 100
        
        # Efeitos visuais
        self.efeitos_ativos = []
        
        self.criar_interface()
        
    def setup_styles(self):
        """Configurar estilos personalizados"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para barras de vida
        style.configure("Vida.Horizontal.TProgressbar", 
                       background='#e74c3c', 
                       troughcolor='#2c3e50',
                       borderwidth=2,
                       lightcolor='#e74c3c',
                       darkcolor='#c0392b')
        
        style.configure("VidaInimigo.Horizontal.TProgressbar", 
                       background='#8e44ad', 
                       troughcolor='#2c3e50',
                       borderwidth=2,
                       lightcolor='#8e44ad',
                       darkcolor='#71368a')

    def criar_interface(self):
        """Criar todos os elementos da interface"""
        
        # Título principal com efeito mágico
        titulo = tk.Label(self.root, 
                         text="⚡ BATALHA ARCANA ⚡", 
                         font=("Papyrus", 24, "bold"),
                         fg='#f39c12', 
                         bg='#1a0d33')
        titulo.pack(pady=20)
        
        # Frame para status dos personagens
        frame_status = tk.Frame(self.root, bg='#1a0d33')
        frame_status.pack(pady=20, padx=20, fill='x')
        
        # Status do jogador
        self.criar_status_personagem(frame_status, "🧙‍♂️ VOCÊ", True)
        
        # VS no centro
        vs_label = tk.Label(frame_status, 
                           text="⚔️ VS ⚔️", 
                           font=("Papyrus", 16, "bold"),
                           fg='#e74c3c', 
                           bg='#1a0d33')
        vs_label.grid(row=0, column=1, padx=30)
        
        # Status do inimigo
        self.criar_status_personagem(frame_status, "👹 INIMIGO", False)
        
        # Área de batalha (mensagens)
        self.criar_area_batalha()
        
        # Grimório de magias
        self.criar_grimorio()
        
        # Botão reiniciar
        self.botao_reiniciar = tk.Button(self.root, 
                                        text="🔄 Nova Batalha",
                                        command=self.reiniciar_jogo,
                                        font=("Papyrus", 12, "bold"),
                                        bg='#27ae60',
                                        fg='white',
                                        activebackground='#229954',
                                        relief='raised',
                                        bd=3,
                                        width=20)
        self.botao_reiniciar.pack(pady=20)
        self.botao_reiniciar.pack_forget()
        
    def criar_status_personagem(self, parent, nome, is_jogador):
        """Criar status visual para um personagem"""
        col = 0 if is_jogador else 2
        
        # Nome do personagem
        nome_label = tk.Label(parent, 
                             text=nome, 
                             font=("Papyrus", 14, "bold"),
                             fg='#3498db' if is_jogador else '#e74c3c',
                             bg='#1a0d33')
        nome_label.grid(row=0, column=col, pady=5)
        
        # Frame para vida
        vida_frame = tk.Frame(parent, bg='#1a0d33')
        vida_frame.grid(row=1, column=col, pady=5, padx=20)
        
        # Label de vida
        vida_text = f"❤️ Vida: {self.vida_jogador if is_jogador else self.vida_inimigo}/100"
        vida_label = tk.Label(vida_frame,
                             text=vida_text,
                             font=("Arial", 10),
                             fg='white',
                             bg='#1a0d33')
        vida_label.pack()
        
        # Barra de vida
        style_name = "Vida.Horizontal.TProgressbar" if is_jogador else "VidaInimigo.Horizontal.TProgressbar"
        vida_bar = ttk.Progressbar(vida_frame,
                                  length=200,
                                  mode='determinate',
                                  style=style_name)
        vida_bar.pack(pady=5)
        vida_bar['maximum'] = 100
        vida_bar['value'] = self.vida_jogador if is_jogador else self.vida_inimigo
        
        # Armazenar referências
        if is_jogador:
            self.vida_jogador_label = vida_label
            self.vida_jogador_bar = vida_bar
        else:
            self.vida_inimigo_label = vida_label
            self.vida_inimigo_bar = vida_bar
    
    def criar_area_batalha(self):
        """Criar área de mensagens da batalha"""
        # Frame da área de batalha com bordas decorativas
        batalha_frame = tk.Frame(self.root, 
                                bg='#2c3e50', 
                                relief='groove', 
                                bd=3)
        batalha_frame.pack(pady=20, padx=30, fill='both', expand=True)
        
        # Título da área
        titulo_batalha = tk.Label(batalha_frame,
                                 text="📜 REGISTRO DA BATALHA 📜",
                                 font=("Papyrus", 12, "bold"),
                                 fg='#f39c12',
                                 bg='#2c3e50')
        titulo_batalha.pack(pady=5)
        
        # Área de texto com scroll
        text_frame = tk.Frame(batalha_frame, bg='#2c3e50')
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.text_batalha = tk.Text(text_frame,
                                   height=8,
                                   width=70,
                                   font=("Consolas", 10),
                                   bg='#34495e',
                                   fg='#ecf0f1',
                                   relief='sunken',
                                   bd=2,
                                   state='disabled',
                                   wrap='word')
        
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=self.text_batalha.yview)
        self.text_batalha.configure(yscrollcommand=scrollbar.set)
        
        self.text_batalha.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def criar_grimorio(self):
        """Criar área dos feitiços"""
        # Frame principal do grimório
        grimorio_frame = tk.LabelFrame(self.root,
                                      text="📚 GRIMÓRIO DE FEITIÇOS 📚",
                                      font=("Papyrus", 12, "bold"),
                                      fg='#f39c12',
                                      bg='#1a0d33',
                                      relief='ridge',
                                      bd=3)
        grimorio_frame.pack(pady=20, padx=30, fill='x')
        
        # Frame para botões de magia
        magias_frame = tk.Frame(grimorio_frame, bg='#1a0d33')
        magias_frame.pack(pady=15, padx=20)
        
        # Definir magias com suas propriedades
        magias = [
            {
                'nome': '🔥 Bola de Fogo',
                'desc': 'Dano: 30 | Precisão: 60%',
                'bg': '#e74c3c',
                'active_bg': '#c0392b',
                'comando': lambda: self.jogar(1)
            },
            {
                'nome': '❄️ Raio Congelante', 
                'desc': 'Dano: 20 | Precisão: 80%',
                'bg': '#3498db',
                'active_bg': '#2980b9',
                'comando': lambda: self.jogar(2)
            },
            {
                'nome': '☄️ Chuva de Meteoros',
                'desc': 'Dano: 50 | Precisão: 30%',
                'bg': '#8e44ad',
                'active_bg': '#71368a', 
                'comando': lambda: self.jogar(3)
            }
        ]
        
        self.botoes_magia = []
        
        for i, magia in enumerate(magias):
            # Frame para cada magia
            magia_frame = tk.Frame(magias_frame, bg='#1a0d33')
            magia_frame.grid(row=0, column=i, padx=15)
            
            # Botão principal da magia
            botao = tk.Button(magia_frame,
                             text=magia['nome'],
                             command=magia['comando'],
                             font=("Papyrus", 11, "bold"),
                             bg=magia['bg'],
                             fg='white',
                             activebackground=magia['active_bg'],
                             relief='raised',
                             bd=3,
                             width=18,
                             height=2)
            botao.pack(pady=5)
            
            # Descrição da magia
            desc_label = tk.Label(magia_frame,
                                 text=magia['desc'],
                                 font=("Arial", 8),
                                 fg='#bdc3c7',
                                 bg='#1a0d33')
            desc_label.pack()
            
            self.botoes_magia.append(botao)
    
    def adicionar_mensagem_batalha(self, mensagem, cor='#ecf0f1'):
        """Adicionar mensagem colorida à área de batalha"""
        self.text_batalha.config(state='normal')
        
        # Definir tags para cores
        if cor == 'dano_jogador':
            cor = '#e74c3c'
        elif cor == 'dano_inimigo':
            cor = '#8e44ad'
        elif cor == 'sucesso':
            cor = '#27ae60'
        elif cor == 'falha':
            cor = '#95a5a6'
        elif cor == 'especial':
            cor = '#f39c12'
        
        self.text_batalha.insert(tk.END, mensagem + '\n')
        self.text_batalha.config(state='disabled')
        self.text_batalha.see(tk.END)
        
    def atualizar_status_vida(self):
        """Atualizar barras e labels de vida"""
        # Atualizar jogador
        self.vida_jogador_label.config(text=f"❤️ Vida: {self.vida_jogador}/100")
        self.vida_jogador_bar['value'] = max(0, self.vida_jogador)
        
        # Atualizar inimigo
        self.vida_inimigo_label.config(text=f"❤️ Vida: {self.vida_inimigo}/100")
        self.vida_inimigo_bar['value'] = max(0, self.vida_inimigo)
        
    def jogar(self, magia):
        """Executar rodada de combate"""
        if self.vida_jogador <= 0 or self.vida_inimigo <= 0:
            return
        
        self.adicionar_mensagem_batalha("=" * 50, 'especial')
        
        # Jogador ataca
        chance = random.randint(1, 100)
        dano = 0
        magias_info = {
            1: ("🔥 Bola de Fogo", 60, 30),
            2: ("❄️ Raio Congelante", 80, 20), 
            3: ("☄️ Chuva de Meteoros", 30, 50)
        }
        
        nome_magia, precisao, dano_max = magias_info[magia]
        
        self.adicionar_mensagem_batalha(f"🧙‍♂️ Você conjurou {nome_magia}!")
        
        if chance <= precisao:
            dano = dano_max
            self.vida_inimigo -= dano
            self.adicionar_mensagem_batalha(f"✨ ACERTOU! Causou {dano} de dano!", 'sucesso')
            # Efeito visual de acerto
            self.efeito_visual_dano(False)
        else:
            self.adicionar_mensagem_batalha("💫 O feitiço falhou...", 'falha')
        
        # Verificar se inimigo morreu
        if self.vida_inimigo <= 0:
            self.vida_inimigo = 0
            self.atualizar_status_vida()
            self.fim_de_jogo()
            return
            
        # Inimigo ataca
        self.adicionar_mensagem_batalha("")
        magia_inimigo = random.randint(1, 3)
        chance_inimigo = random.randint(1, 100)
        
        nome_magia_inimigo, precisao_inimigo, dano_max_inimigo = magias_info[magia_inimigo]
        
        self.adicionar_mensagem_batalha(f"👹 Inimigo conjurou {nome_magia_inimigo}!")
        
        if chance_inimigo <= precisao_inimigo:
            dano_inimigo = dano_max_inimigo
            self.vida_jogador -= dano_inimigo
            self.adicionar_mensagem_batalha(f"💥 Você recebeu {dano_inimigo} de dano!", 'dano_inimigo')
            # Efeito visual de dano recebido
            self.efeito_visual_dano(True)
        else:
            self.adicionar_mensagem_batalha("🛡️ O feitiço inimigo falhou!", 'sucesso')
        
        # Atualizar interface
        self.atualizar_status_vida()
        
        # Verificar fim de jogo
        if self.vida_jogador <= 0:
            self.vida_jogador = 0
            self.atualizar_status_vida()
            self.fim_de_jogo()
    
    def efeito_visual_dano(self, jogador_recebeu):
        """Criar efeito visual quando alguém recebe dano"""
        # Mudar cor temporariamente
        if jogador_recebeu:
            self.vida_jogador_bar.configure(style="DanoRecebido.Horizontal.TProgressbar")
            self.root.after(500, lambda: self.vida_jogador_bar.configure(style="Vida.Horizontal.TProgressbar"))
        else:
            self.vida_inimigo_bar.configure(style="DanoCausado.Horizontal.TProgressbar") 
            self.root.after(500, lambda: self.vida_inimigo_bar.configure(style="VidaInimigo.Horizontal.TProgressbar"))
    
    def fim_de_jogo(self):
        """Finalizar o jogo"""
        self.adicionar_mensagem_batalha("=" * 50, 'especial')
        
        if self.vida_jogador > self.vida_inimigo:
            self.adicionar_mensagem_batalha("🎉 VITÓRIA! Você é o mago supremo! 🎉", 'sucesso')
        else:
            self.adicionar_mensagem_batalha("💀 DERROTA! O poder das trevas prevaleceu... 💀", 'dano_inimigo')
            
        self.adicionar_mensagem_batalha("=" * 50, 'especial')
        
        # Desabilitar botões de magia
        for botao in self.botoes_magia:
            botao.config(state=tk.DISABLED)
            
        # Mostrar botão reiniciar
        self.botao_reiniciar.pack()
    
    def reiniciar_jogo(self):
        """Reiniciar o jogo"""
        # Resetar valores
        self.vida_jogador = 100
        self.vida_inimigo = 100
        
        # Limpar área de batalha
        self.text_batalha.config(state='normal')
        self.text_batalha.delete(1.0, tk.END)
        self.text_batalha.config(state='disabled')
        
        # Reabilitar botões
        for botao in self.botoes_magia:
            botao.config(state=tk.NORMAL)
        
        # Atualizar interface
        self.atualizar_status_vida()
        
        # Esconder botão reiniciar
        self.botao_reiniciar.pack_forget()
        
        # Mensagem de início
        self.adicionar_mensagem_batalha("🔮 Uma nova batalha arcana começou! 🔮", 'especial')
        self.adicionar_mensagem_batalha("Escolha seu feitiço sabiamente...\n", 'especial')

# Iniciar o jogo
if __name__ == "__main__":
    root = tk.Tk()
    # Configurar ícone da janela (se disponível)
    try:
        root.iconbitmap('wizard.ico')  # Opcional: ícone de mago
    except:
        pass
    
    jogo = JogoMagiaGUI(root)
    
    # Mensagem inicial
    jogo.adicionar_mensagem_batalha("🔮 Bem-vindo à Batalha Arcana! 🔮", 'especial')
    jogo.adicionar_mensagem_batalha("Prepare-se para enfrentar as forças das trevas!\n", 'especial')
    
    root.mainloop()