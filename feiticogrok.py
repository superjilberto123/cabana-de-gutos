import tkinter as tk
from tkinter import ttk
import random
import time

class JogoMagiaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Final Fantasy Battle")
        self.root.geometry("800x700")
        self.root.configure(bg='black')  # Fundo preto como em FF antigo
        
        # Configuração de estilo no estilo FF (azul, branco, pixel-like)
        self.setup_styles()
        
        # Estados do jogo
        self.vida_jogador = 100
        self.mana_jogador = 50  # Adicionando mana para magias
        self.vida_inimigo = 100
        self.mana_inimigo = 50
        self.max_vida = 100
        self.max_mana = 50
        self.pocoes = 3  # Poções de cura
        
        # Efeitos visuais
        self.efeitos_ativos = []
        
        self.criar_interface()
        
    def setup_styles(self):
        """Configurar estilos personalizados no estilo Final Fantasy antigo"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para barras de vida (verde como em FF)
        style.configure("Vida.Horizontal.TProgressbar", 
                        background='#00ff00', 
                        troughcolor='#000080',
                        borderwidth=2,
                        lightcolor='#00ff00',
                        darkcolor='#008000')
        
        style.configure("VidaInimigo.Horizontal.TProgressbar", 
                        background='#ff0000', 
                        troughcolor='#000080',
                        borderwidth=2,
                        lightcolor='#ff0000',
                        darkcolor='#800000')
        
        # Estilo para mana (azul)
        style.configure("Mana.Horizontal.TProgressbar", 
                        background='#0000ff', 
                        troughcolor='#000080',
                        borderwidth=2,
                        lightcolor='#0000ff',
                        darkcolor='#000080')
        
        style.configure("ManaInimigo.Horizontal.TProgressbar", 
                        background='#800080', 
                        troughcolor='#000080',
                        borderwidth=2,
                        lightcolor='#800080',
                        darkcolor='#400040')
        
        # Estilos para dano (piscar vermelho/amarelo)
        style.configure("DanoRecebido.Horizontal.TProgressbar", 
                        background='#ffff00', 
                        troughcolor='#000080')
        
        style.configure("DanoCausado.Horizontal.TProgressbar", 
                        background='#ffff00', 
                        troughcolor='#000080')

    def criar_interface(self):
        """Criar todos os elementos da interface no estilo FF"""
        
        # Título principal
        titulo = tk.Label(self.root, 
                          text="BATALHA", 
                          font=("Courier", 24, "bold"),
                          fg='white', 
                          bg='black')
        titulo.pack(pady=10)
        
        # Frame para status dos personagens (menu azul)
        frame_status = tk.Frame(self.root, bg='#000080', relief='raised', bd=4)
        frame_status.pack(pady=10, padx=10, fill='x')
        
        # Status do jogador (herói)
        self.criar_status_personagem(frame_status, "Black Mage", True)
        
        # VS no centro
        vs_label = tk.Label(frame_status, 
                            text="VS", 
                            font=("Courier", 16, "bold"),
                            fg='yellow', 
                            bg='#000080')
        vs_label.grid(row=0, column=1, padx=30)
        
        # Status do inimigo
        self.criar_status_personagem(frame_status, "Behemoth", False)
        
        # Área visual da batalha (Canvas para gráficos)
        self.canvas = tk.Canvas(self.root, bg='black', width=800, height=200, highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Desenhar personagens simples (placeholders pixel-like)
        self.desenhar_personagens()
        
        # Área de mensagens (log de batalha, como janela de texto em FF)
        self.criar_area_batalha()
        
        # Menu de comandos (como em FF: Magic, Item)
        self.criar_menu_comandos()
        
        # Botão reiniciar
        self.botao_reiniciar = tk.Button(self.root, 
                                         text="New Battle",
                                         command=self.reiniciar_jogo,
                                         font=("Courier", 12, "bold"),
                                         bg='#000080',
                                         fg='white',
                                         activebackground='#0000ff',
                                         relief='raised',
                                         bd=3,
                                         width=20)
        self.botao_reiniciar.pack(pady=10)
        self.botao_reiniciar.pack_forget()
        
    def desenhar_personagens(self):
        """Desenhar representações simples dos personagens no canvas"""
        # Jogador (Black Mage) - retângulo azul com 'hat'
        self.player_body = self.canvas.create_rectangle(100, 150, 150, 200, fill='#0000ff', outline='white')
        self.player_hat = self.canvas.create_polygon(100, 150, 125, 120, 150, 150, fill='#ffff00', outline='white')
        
        # Inimigo (Behemoth) - retângulo vermelho maior
        self.enemy_body = self.canvas.create_rectangle(600, 100, 700, 200, fill='#ff0000', outline='white')
        self.enemy_horn = self.canvas.create_polygon(700, 100, 720, 80, 700, 120, fill='#808080', outline='white')
        
    def criar_status_personagem(self, parent, nome, is_jogador):
        """Criar status visual para um personagem"""
        col = 0 if is_jogador else 2
        
        # Nome do personagem
        nome_label = tk.Label(parent, 
                              text=nome, 
                              font=("Courier", 14, "bold"),
                              fg='white' if is_jogador else 'red',
                              bg='#000080')
        nome_label.grid(row=0, column=col, pady=5)
        
        # Frame para vida e mana
        status_frame = tk.Frame(parent, bg='#000080')
        status_frame.grid(row=1, column=col, pady=5, padx=20)
        
        # Label de vida
        vida_text = f"HP: {self.vida_jogador if is_jogador else self.vida_inimigo}/{self.max_vida}"
        vida_label = tk.Label(status_frame,
                              text=vida_text,
                              font=("Courier", 10),
                              fg='white',
                              bg='#000080')
        vida_label.pack(anchor='w')
        
        # Barra de vida
        style_name = "Vida.Horizontal.TProgressbar" if is_jogador else "VidaInimigo.Horizontal.TProgressbar"
        vida_bar = ttk.Progressbar(status_frame,
                                   length=150,
                                   mode='determinate',
                                   style=style_name)
        vida_bar.pack(pady=2)
        vida_bar['maximum'] = self.max_vida
        vida_bar['value'] = self.vida_jogador if is_jogador else self.vida_inimigo
        
        # Label de mana
        mana_text = f"MP: {self.mana_jogador if is_jogador else self.mana_inimigo}/{self.max_mana}"
        mana_label = tk.Label(status_frame,
                              text=mana_text,
                              font=("Courier", 10),
                              fg='white',
                              bg='#000080')
        mana_label.pack(anchor='w')
        
        # Barra de mana
        mana_style = "Mana.Horizontal.TProgressbar" if is_jogador else "ManaInimigo.Horizontal.TProgressbar"
        mana_bar = ttk.Progressbar(status_frame,
                                   length=150,
                                   mode='determinate',
                                   style=mana_style)
        mana_bar.pack(pady=2)
        mana_bar['maximum'] = self.max_mana
        mana_bar['value'] = self.mana_jogador if is_jogador else self.mana_inimigo
        
        # Armazenar referências
        if is_jogador:
            self.vida_jogador_label = vida_label
            self.vida_jogador_bar = vida_bar
            self.mana_jogador_label = mana_label
            self.mana_jogador_bar = mana_bar
        else:
            self.vida_inimigo_label = vida_label
            self.vida_inimigo_bar = vida_bar
            self.mana_inimigo_label = mana_label
            self.mana_inimigo_bar = mana_bar
    
    def criar_area_batalha(self):
        """Criar área de mensagens da batalha"""
        batalha_frame = tk.Frame(self.root, 
                                 bg='#000080', 
                                 relief='raised', 
                                 bd=4)
        batalha_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Título da área
        titulo_batalha = tk.Label(batalha_frame,
                                  text="Battle Log",
                                  font=("Courier", 12, "bold"),
                                  fg='white',
                                  bg='#000080')
        titulo_batalha.pack(pady=5)
        
        # Área de texto com scroll
        text_frame = tk.Frame(batalha_frame, bg='#000080')
        text_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.text_batalha = tk.Text(text_frame,
                                    height=6,
                                    width=80,
                                    font=("Courier", 10),
                                    bg='black',
                                    fg='white',
                                    relief='sunken',
                                    bd=2,
                                    state='disabled',
                                    wrap='word',
                                    insertbackground='white')
        
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=self.text_batalha.yview)
        self.text_batalha.configure(yscrollcommand=scrollbar.set)
        
        self.text_batalha.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def criar_menu_comandos(self):
        """Criar menu de comandos no estilo FF"""
        comandos_frame = tk.LabelFrame(self.root,
                                       text="Commands",
                                       font=("Courier", 12, "bold"),
                                       fg='white',
                                       bg='black',
                                       labelanchor='n',
                                       relief='raised',
                                       bd=4)
        comandos_frame.pack(pady=10, padx=10, fill='x')
        
        # Frame para botões
        btn_frame = tk.Frame(comandos_frame, bg='black')
        btn_frame.pack(pady=10, padx=10)
        
        # Definir comandos (magias e itens)
        comandos = [
            {
                'nome': 'Fire',
                'desc': 'Dmg: 30 | Acc: 60% | MP: 10',
                'bg': '#ff0000',
                'active_bg': '#800000',
                'comando': lambda: self.jogar(1)
            },
            {
                'nome': 'Ice', 
                'desc': 'Dmg: 20 | Acc: 80% | MP: 8',
                'bg': '#00ffff',
                'active_bg': '#008080',
                'comando': lambda: self.jogar(2)
            },
            {
                'nome': 'Thunder',
                'desc': 'Dmg: 40 | Acc: 50% | MP: 15',
                'bg': '#ffff00',
                'active_bg': '#808000',
                'comando': lambda: self.jogar(3)
            },
            {
                'nome': 'Meteor',
                'desc': 'Dmg: 50 | Acc: 30% | MP: 20',
                'bg': '#ff00ff',
                'active_bg': '#800080',
                'comando': lambda: self.jogar(4)
            },
            {
                'nome': 'Cure',
                'desc': 'Heal: 30 | Acc: 100% | MP: 10',
                'bg': '#00ff00',
                'active_bg': '#008000',
                'comando': lambda: self.jogar(5)
            },
            {
                'nome': 'Potion',
                'desc': f'Heal: 25 | Uses: {self.pocoes}',
                'bg': '#808080',
                'active_bg': '#404040',
                'comando': self.usar_pocao
            }
        ]
        
        self.botoes_comando = []
        self.potion_desc_label = None  # Para atualizar usos da poção
        
        for i, cmd in enumerate(comandos):
            # Frame para cada comando
            cmd_frame = tk.Frame(btn_frame, bg='black')
            cmd_frame.grid(row=i//3, column=i%3, padx=10, pady=5)
            
            # Botão
            botao = tk.Button(cmd_frame,
                              text=cmd['nome'],
                              command=cmd['comando'],
                              font=("Courier", 11, "bold"),
                              bg=cmd['bg'],
                              fg='black',
                              activebackground=cmd['active_bg'],
                              relief='raised',
                              bd=3,
                              width=12,
                              height=2)
            botao.pack()
            
            # Descrição
            desc_label = tk.Label(cmd_frame,
                                  text=cmd['desc'],
                                  font=("Courier", 8),
                                  fg='white',
                                  bg='black')
            desc_label.pack()
            
            self.botoes_comando.append(botao)
            if cmd['nome'] == 'Potion':
                self.potion_desc_label = desc_label
                self.potion_button = botao
    
    def adicionar_mensagem_batalha(self, mensagem, cor='white'):
        """Adicionar mensagem à área de batalha"""
        self.text_batalha.config(state='normal')
        self.text_batalha.insert(tk.END, mensagem + '\n', cor)
        self.text_batalha.config(state='disabled')
        self.text_batalha.see(tk.END)
        
    def atualizar_status(self):
        """Atualizar barras e labels de vida e mana"""
        # Jogador
        self.vida_jogador_label.config(text=f"HP: {max(0, self.vida_jogador)}/{self.max_vida}")
        self.vida_jogador_bar['value'] = max(0, self.vida_jogador)
        self.mana_jogador_label.config(text=f"MP: {max(0, self.mana_jogador)}/{self.max_mana}")
        self.mana_jogador_bar['value'] = max(0, self.mana_jogador)
        
        # Inimigo
        self.vida_inimigo_label.config(text=f"HP: {max(0, self.vida_inimigo)}/{self.max_vida}")
        self.vida_inimigo_bar['value'] = max(0, self.vida_inimigo)
        self.mana_inimigo_label.config(text=f"MP: {max(0, self.mana_inimigo)}/{self.max_mana}")
        self.mana_inimigo_bar['value'] = max(0, self.mana_inimigo)
        
    def jogar(self, magia):
        """Executar rodada de combate"""
        if self.vida_jogador <= 0 or self.vida_inimigo <= 0:
            return
        
        self.adicionar_mensagem_batalha("-" * 50)
        
        # Informações das magias
        magias_info = {
            1: ("Fire", 60, 30, 10, 'damage', 'fire'),
            2: ("Ice", 80, 20, 8, 'damage', 'ice'),
            3: ("Thunder", 50, 40, 15, 'damage', 'thunder'),
            4: ("Meteor", 30, 50, 20, 'damage', 'meteor'),
            5: ("Cure", 100, 30, 10, 'heal', 'cure')
        }
        
        nome_magia, precisao, valor, custo_mana, tipo, anim_type = magias_info[magia]
        
        if self.mana_jogador < custo_mana:
            self.adicionar_mensagem_batalha("Not enough MP!")
            return
        
        self.mana_jogador -= custo_mana
        self.atualizar_status()
        
        self.adicionar_mensagem_batalha(f"You cast {nome_magia}!")
        
        chance = random.randint(1, 100)
        if chance <= precisao:
            if tipo == 'damage':
                self.vida_inimigo -= valor
                self.adicionar_mensagem_batalha(f"Hit! Dealt {valor} damage!")
                self.efeito_visual_dano(False)
                self.animar_ataque(anim_type, True)
            else:  # heal
                self.vida_jogador = min(self.max_vida, self.vida_jogador + valor)
                self.adicionar_mensagem_batalha(f"Healed {valor} HP!")
                self.animar_ataque(anim_type, True)
        else:
            self.adicionar_mensagem_batalha("Missed...")
        
        if self.vida_inimigo <= 0:
            self.vida_inimigo = 0
            self.atualizar_status()
            self.fim_de_jogo()
            return
            
        # Turno do inimigo
        self.adicionar_mensagem_batalha("")
        magia_inimigo = random.choice(list(magias_info.keys())[:-1])  # Inimigo não usa cure
        nome_magia_i, precisao_i, valor_i, custo_mana_i, tipo_i, anim_type_i = magias_info[magia_inimigo]
        
        if self.mana_inimigo >= custo_mana_i:
            self.mana_inimigo -= custo_mana_i
            self.atualizar_status()
            
            self.adicionar_mensagem_batalha(f"Enemy casts {nome_magia_i}!")
            
            chance_i = random.randint(1, 100)
            if chance_i <= precisao_i:
                self.vida_jogador -= valor_i
                self.adicionar_mensagem_batalha(f"Hit! You take {valor_i} damage!")
                self.efeito_visual_dano(True)
                self.animar_ataque(anim_type_i, False)
            else:
                self.adicionar_mensagem_batalha("Missed!")
        
        self.atualizar_status()
        
        if self.vida_jogador <= 0:
            self.vida_jogador = 0
            self.atualizar_status()
            self.fim_de_jogo()
    
    def usar_pocao(self):
        """Usar poção de cura"""
        if self.pocoes <= 0:
            self.adicionar_mensagem_batalha("No potions left!")
            return
        
        self.pocoes -= 1
        heal = 25
        self.vida_jogador = min(self.max_vida, self.vida_jogador + heal)
        self.adicionar_mensagem_batalha(f"Used Potion! Healed {heal} HP.")
        self.animar_ataque('potion', True)
        self.atualizar_status()
        self.potion_desc_label.config(text=f'Heal: 25 | Uses: {self.pocoes}')
        if self.pocoes == 0:
            self.potion_button.config(state=tk.DISABLED)
        
        # Turno do inimigo após uso de item
        self.adicionar_mensagem_batalha("")
        self.turno_inimigo()
    
    def turno_inimigo(self):
        """Lógica separada para turno do inimigo"""
        magias_info = {
            1: ("Fire", 60, 30, 10, 'damage', 'fire'),
            2: ("Ice", 80, 20, 8, 'damage', 'ice'),
            3: ("Thunder", 50, 40, 15, 'damage', 'thunder'),
            4: ("Meteor", 30, 50, 20, 'damage', 'meteor')
        }
        magia_inimigo = random.choice(list(magias_info.keys()))
        nome_magia_i, precisao_i, valor_i, custo_mana_i, tipo_i, anim_type_i = magias_info[magia_inimigo]
        
        if self.mana_inimigo >= custo_mana_i:
            self.mana_inimigo -= custo_mana_i
            self.atualizar_status()
            
            self.adicionar_mensagem_batalha(f"Enemy casts {nome_magia_i}!")
            
            chance_i = random.randint(1, 100)
            if chance_i <= precisao_i:
                self.vida_jogador -= valor_i
                self.adicionar_mensagem_batalha(f"Hit! You take {valor_i} damage!")
                self.efeito_visual_dano(True)
                self.animar_ataque(anim_type_i, False)
            else:
                self.adicionar_mensagem_batalha("Missed!")
        
        self.atualizar_status()
        
        if self.vida_jogador <= 0:
            self.vida_jogador = 0
            self.atualizar_status()
            self.fim_de_jogo()
    
    def animar_ataque(self, anim_type, from_player):
        """Animar ataques graficamente no canvas"""
        start_x = 125 if from_player else 650
        end_x = 650 if from_player else 125
        y = 150
        dx = 10 if from_player else -10
        color = 'white'
        shape_type = 'oval'
        
        if anim_type == 'fire':
            color = 'orange'
        elif anim_type == 'ice':
            color = 'cyan'
            shape_type = 'polygon'  # Triângulo para gelo
        elif anim_type == 'thunder':
            color = 'yellow'
            shape_type = 'line'  # Linha para raio
        elif anim_type == 'meteor':
            color = 'red'
        elif anim_type == 'cure' or anim_type == 'potion':
            color = 'green'
            # Para heal, círculo ao redor do alvo
            target_x = 125 if from_player else 650
            shape = self.canvas.create_oval(target_x-20, y-20, target_x+20, y+20, outline=color, width=3)
            self.root.after(500, lambda: self.canvas.delete(shape))
            self.root.after(250, lambda: self.canvas.itemconfig(shape, outline='lime'))
            return
        
        if shape_type == 'oval':
            shape = self.canvas.create_oval(start_x-10, y-10, start_x+10, y+10, fill=color)
        elif shape_type == 'polygon':
            shape = self.canvas.create_polygon(start_x-10, y+10, start_x, y-10, start_x+10, y+10, fill=color)
        elif shape_type == 'line':
            shape = self.canvas.create_line(start_x, y-20, start_x, y+20, fill=color, width=5)
        
        def move():
            self.canvas.move(shape, dx, 0)
            coords = self.canvas.coords(shape)
            if from_player and coords[0] < end_x or not from_player and coords[0] > end_x:
                self.root.after(20, move)
            else:
                self.canvas.delete(shape)
        
        move()
    
    def efeito_visual_dano(self, jogador_recebeu):
        """Efeito visual de dano nas barras"""
        if jogador_recebeu:
            self.vida_jogador_bar.configure(style="DanoRecebido.Horizontal.TProgressbar")
            self.root.after(500, lambda: self.vida_jogador_bar.configure(style="Vida.Horizontal.TProgressbar"))
        else:
            self.vida_inimigo_bar.configure(style="DanoCausado.Horizontal.TProgressbar")
            self.root.after(500, lambda: self.vida_inimigo_bar.configure(style="VidaInimigo.Horizontal.TProgressbar"))
    
    def fim_de_jogo(self):
        """Finalizar o jogo"""
        self.adicionar_mensagem_batalha("-" * 50)
        
        if self.vida_jogador > 0:
            self.adicionar_mensagem_batalha("Victory!")
        else:
            self.adicionar_mensagem_batalha("Defeat...")
            
        self.adicionar_mensagem_batalha("-" * 50)
        
        # Desabilitar botões
        for botao in self.botoes_comando:
            botao.config(state=tk.DISABLED)
            
        # Mostrar botão reiniciar
        self.botao_reiniciar.pack()
    
    def reiniciar_jogo(self):
        """Reiniciar o jogo"""
        # Resetar valores
        self.vida_jogador = 100
        self.mana_jogador = 50
        self.vida_inimigo = 100
        self.mana_inimigo = 50
        self.pocoes = 3
        
        # Limpar log
        self.text_batalha.config(state='normal')
        self.text_batalha.delete(1.0, tk.END)
        self.text_batalha.config(state='disabled')
        
        # Reabilitar botões
        for botao in self.botoes_comando:
            botao.config(state=tk.NORMAL)
        
        # Atualizar interface
        self.atualizar_status()
        self.potion_desc_label.config(text=f'Heal: 25 | Uses: {self.pocoes}')
        
        # Esconder reiniciar
        self.botao_reiniciar.pack_forget()
        
        # Mensagem inicial
        self.adicionar_mensagem_batalha("A new battle begins...")
        self.adicionar_mensagem_batalha("Choose your command.\n")

# Iniciar o jogo
if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.iconbitmap('ff.ico')  # Opcional: ícone FF
    except:
        pass
    
    jogo = JogoMagiaGUI(root)
    
    # Mensagem inicial
    jogo.adicionar_mensagem_batalha("Welcome to the battle!")
    jogo.adicionar_mensagem_batalha("Prepare to fight!\n")
    
    root.mainloop()