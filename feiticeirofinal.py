import tkinter as tk
from tkinter import ttk, Canvas
import random
import time
import threading



class FFBattleSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("⚔️ Final Fantasy Battle Arena ⚔️")
        self.root.geometry("1000x800")
        self.root.configure(bg='#000033')
        
        # Estados do jogo
        self.vida_jogador = 150
        self.mana_jogador = 100
        self.vida_inimigo = 180
        self.mana_inimigo = 80
        
        self.max_vida_jogador = 150
        self.max_mana_jogador = 100
        self.max_vida_inimigo = 180
        self.max_mana_inimigo = 80
        
        # Items
        self.pocoes_vida = 3
        self.pocoes_mana = 2
        self.elixirs = 1
        
        # Estado da batalha
        self.turno_jogador = True
        self.animacao_ativa = False
        
        # Estados dos sprites
        self.guerreiro_estado = 'idle'  # idle, walk, attack, hurt, dead
        self.guerreiro_frame = 0
        self.guerreiro_max_frames = {'idle': 6, 'walk': 8, 'attack': 5, 'hurt': 3, 'dead': 5}
        
        self.demonio_estado = 'idle'
        self.demonio_frame = 0
        self.demonio_max_frames = {'idle': 6, 'walk': 8, 'attack': 5, 'hurt': 3, 'dead': 5}
        
        # Timer para animação
        self.animation_timer = None
        
        # Configurar estilos
        self.setup_styles()
        
        # Criar interface
        self.criar_interface()
        
        # Inicializar battaglia
        self.iniciar_batalha()
        
        # Iniciar loop de animação
        self.animar_sprites()
        
    def setup_styles(self):
        """Configurar estilos FF clássico"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Barra de vida (vermelha)
        style.configure("HP.Horizontal.TProgressbar",
                       background='#cc0000',
                       troughcolor='#330000',
                       borderwidth=2)
        
        # Barra de mana (azul)
        style.configure("MP.Horizontal.TProgressbar",
                       background='#0066cc',
                       troughcolor='#001133',
                       borderwidth=2)
        
        # Barra de vida inimigo (roxa)
        style.configure("EnemyHP.Horizontal.TProgressbar",
                       background='#9900cc',
                       troughcolor='#330033',
                       borderwidth=2)
    
    def criar_interface(self):
        """Criar interface estilo FF clássico"""
        
        # Frame superior - Campo de batalha
        self.frame_batalha = tk.Frame(self.root, bg='#001122', height=400)
        self.frame_batalha.pack(fill='x', padx=10, pady=10)
        self.frame_batalha.pack_propagate(False)
        
        # Canvas para gráficos da batalha
        self.canvas_batalha = Canvas(self.frame_batalha, 
                                   bg='#001122',
                                   height=350,
                                   highlightthickness=2,
                                   highlightbackground='#4444ff')
        self.canvas_batalha.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Frame central - Status dos personagens
        self.frame_status = tk.Frame(self.root, bg='#000033')
        self.frame_status.pack(fill='x', padx=10, pady=5)
        
        self.criar_status_personagens()
        
        # Frame inferior - Menu de comandos estilo FF
        self.frame_menu = tk.Frame(self.root, bg='#000066', height=200)
        self.frame_menu.pack(fill='both', padx=10, pady=10)
        self.frame_menu.pack_propagate(False)
        
        self.criar_menu_batalha()
        
        # Desenhar personagens iniciais
        self.desenhar_personagens()
        
    def criar_status_personagens(self):
        """Criar barras de status estilo FF"""
        
        # Frame para herói
        hero_frame = tk.LabelFrame(self.frame_status,
                                  text="🗡️ GUERREIRO MÍSTICO",
                                  font=("Courier", 12, "bold"),
                                  fg='#ffff00',
                                  bg='#000033',
                                  bd=2)
        hero_frame.grid(row=0, column=0, padx=20, pady=10, sticky='w')
        
        # HP do herói
        tk.Label(hero_frame, text="HP", font=("Courier", 10, "bold"),
                fg='#ff4444', bg='#000033').grid(row=0, column=0, sticky='w')
        
        self.hp_jogador_bar = ttk.Progressbar(hero_frame,
                                            length=200,
                                            mode='determinate',
                                            style="HP.Horizontal.TProgressbar")
        self.hp_jogador_bar.grid(row=0, column=1, padx=5)
        self.hp_jogador_bar['maximum'] = self.max_vida_jogador
        self.hp_jogador_bar['value'] = self.vida_jogador
        
        self.hp_jogador_label = tk.Label(hero_frame,
                                       text=f"{self.vida_jogador}/{self.max_vida_jogador}",
                                       font=("Courier", 10),
                                       fg='white', bg='#000033')
        self.hp_jogador_label.grid(row=0, column=2, padx=5)
        
        # MP do herói
        tk.Label(hero_frame, text="MP", font=("Courier", 10, "bold"),
                fg='#4444ff', bg='#000033').grid(row=1, column=0, sticky='w')
        
        self.mp_jogador_bar = ttk.Progressbar(hero_frame,
                                            length=200,
                                            mode='determinate',
                                            style="MP.Horizontal.TProgressbar")
        self.mp_jogador_bar.grid(row=1, column=1, padx=5)
        self.mp_jogador_bar['maximum'] = self.max_mana_jogador
        self.mp_jogador_bar['value'] = self.mana_jogador
        
        self.mp_jogador_label = tk.Label(hero_frame,
                                       text=f"{self.mana_jogador}/{self.max_mana_jogador}",
                                       font=("Courier", 10),
                                       fg='white', bg='#000033')
        self.mp_jogador_label.grid(row=1, column=2, padx=5)
        
        # Frame para inimigo
        enemy_frame = tk.LabelFrame(self.frame_status,
                                   text="👹 DEMÔNIO DAS SOMBRAS",
                                   font=("Courier", 12, "bold"),
                                   fg='#ff0000',
                                   bg='#000033',
                                   bd=2)
        enemy_frame.grid(row=0, column=1, padx=20, pady=10, sticky='e')
        
        # HP do inimigo
        tk.Label(enemy_frame, text="HP", font=("Courier", 10, "bold"),
                fg='#ff4444', bg='#000033').grid(row=0, column=0, sticky='w')
        
        self.hp_inimigo_bar = ttk.Progressbar(enemy_frame,
                                            length=200,
                                            mode='determinate',
                                            style="EnemyHP.Horizontal.TProgressbar")
        self.hp_inimigo_bar.grid(row=0, column=1, padx=5)
        self.hp_inimigo_bar['maximum'] = self.max_vida_inimigo
        self.hp_inimigo_bar['value'] = self.vida_inimigo
        
        self.hp_inimigo_label = tk.Label(enemy_frame,
                                       text=f"{self.vida_inimigo}/{self.max_vida_inimigo}",
                                       font=("Courier", 10),
                                       fg='white', bg='#000033')
        self.hp_inimigo_label.grid(row=0, column=2, padx=5)
    
    def criar_menu_batalha(self):
        """Criar menu de comandos estilo FF"""
        
        # Frame principal do menu com borda FF
        menu_principal = tk.Frame(self.frame_menu, bg='#000066', bd=3, relief='raised')
        menu_principal.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Menu de navegação
        nav_frame = tk.Frame(menu_principal, bg='#000066')
        nav_frame.pack(side='left', fill='y', padx=10, pady=10)
        
        # Botões principais do menu
        self.btn_attack = self.criar_botao_ff(nav_frame, "⚔️ ATACAR", self.menu_atacar)
        self.btn_attack.pack(pady=5, fill='x')
        
        self.btn_magic = self.criar_botao_ff(nav_frame, "🔮 MAGIA", self.menu_magia)
        self.btn_magic.pack(pady=5, fill='x')
        
        self.btn_items = self.criar_botao_ff(nav_frame, "💊 ITENS", self.menu_itens)
        self.btn_items.pack(pady=5, fill='x')
        
        self.btn_defend = self.criar_botao_ff(nav_frame, "🛡️ DEFENDER", self.defender)
        self.btn_defend.pack(pady=5, fill='x')
        
        # Frame para sub-menus
        self.submenu_frame = tk.Frame(menu_principal, bg='#000066')
        self.submenu_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        # Frame de texto de batalha
        self.text_frame = tk.Frame(menu_principal, bg='#000066')
        self.text_frame.pack(side='bottom', fill='x', padx=10, pady=10)
        
        # Área de texto para mensagens
        self.texto_batalha = tk.Text(self.text_frame,
                                   height=4,
                                   font=("Courier", 11, "bold"),
                                   bg='#000044',
                                   fg='#ffffff',
                                   state='disabled',
                                   wrap='word',
                                   bd=2,
                                   relief='sunken')
        self.texto_batalha.pack(fill='x')
        
        # Limpar submenu inicialmente
        self.limpar_submenu()
    
    def criar_botao_ff(self, parent, text, command, width=15):
        """Criar botão estilo Final Fantasy"""
        return tk.Button(parent,
                        text=text,
                        command=command,
                        font=("Courier", 11, "bold"),
                        bg='#4444aa',
                        fg='white',
                        activebackground='#6666cc',
                        activeforeground='white',
                        bd=2,
                        relief='raised',
                        width=width,
                        height=2)
    
    def desenhar_guerreiro_sprite(self, x, y):
        """Desenhar sprite do guerreiro baseado no estado atual"""
        frame = self.guerreiro_frame
        estado = self.guerreiro_estado
        
        # Definir cores baseadas no estado
        if estado == 'hurt':
            cor_armadura = '#aa2222'
            cor_pele = '#ffaa88'
        elif estado == 'dead':
            cor_armadura = '#444444'
            cor_pele = '#888888'
        else:
            cor_armadura = '#cc4444'
            cor_pele = '#ffccaa'
        
        # Corpo principal (armadura)
        body_width = 30 if estado == 'attack' and frame in [2, 3] else 26
        self.canvas_batalha.create_rectangle(x-body_width//2, y+10, x+body_width//2, y+50, 
                                           fill=cor_armadura, outline='#8b0000', width=2, tags='guerreiro')
        
        # Cabeça
        head_offset = -2 if estado == 'attack' and frame in [1, 2, 3] else 0
        self.canvas_batalha.create_oval(x-12+head_offset, y-10, x+12+head_offset, y+15, 
                                      fill=cor_pele, outline='#cc9966', width=2, tags='guerreiro')
        
        # Capacete/Cabelo (representação simplificada do sprite)
        helm_color = '#666666' if estado != 'dead' else '#333333'
        self.canvas_batalha.create_arc(x-12+head_offset, y-12, x+12+head_offset, y+8, 
                                     fill=helm_color, outline='#444444', width=2, tags='guerreiro')
        
        # Arma (espada) - posição varia com ataque
        if estado == 'attack':
            if frame == 0:
                # Preparando ataque
                sword_x1, sword_y1 = x+20, y-20
                sword_x2, sword_y2 = x+25, y+10
            elif frame in [1, 2]:
                # Meio do ataque
                sword_x1, sword_y1 = x+15, y-30
                sword_x2, sword_y2 = x+35, y-10
            elif frame == 3:
                # Final do ataque
                sword_x1, sword_y1 = x+30, y-15
                sword_x2, sword_y2 = x+45, y+15
            else:
                # Retornando posição
                sword_x1, sword_y1 = x+18, y-15
                sword_x2, sword_y2 = x+25, y+20
        else:
            # Posição normal
            sword_x1, sword_y1 = x+18, y-15
            sword_x2, sword_y2 = x+22, y+25
        
        if estado != 'dead':
            self.canvas_batalha.create_line(sword_x1, sword_y1, sword_x2, sword_y2, 
                                          fill='#c0c0c0', width=3, tags='guerreiro')
            # Punho da espada
            self.canvas_batalha.create_oval(sword_x2-3, sword_y2-3, sword_x2+3, sword_y2+3, 
                                          fill='#8b4513', outline='#654321', tags='guerreiro')
        
        # Escudo (lado esquerdo)
        shield_x = x-22
        if estado == 'defend':
            shield_x = x-18  # Escudo mais próximo durante defesa
        
        if estado != 'dead':
            self.canvas_batalha.create_oval(shield_x-8, y+5, shield_x+8, y+30, 
                                          fill='#8b4513', outline='#654321', width=2, tags='guerreiro')
            # Cruz no escudo
            self.canvas_batalha.create_line(shield_x, y+10, shield_x, y+25, fill='#ffd700', width=2, tags='guerreiro')
            self.canvas_batalha.create_line(shield_x-5, y+17, shield_x+5, y+17, fill='#ffd700', width=2, tags='guerreiro')
        
        # Pernas - animação de caminhada
        if estado == 'walk':
            leg_offset = 3 if frame % 4 < 2 else -3
            self.canvas_batalha.create_rectangle(x-6+leg_offset, y+50, x, y+75, 
                                              fill=cor_armadura, outline='#8b0000', tags='guerreiro')
            self.canvas_batalha.create_rectangle(x+leg_offset, y+50, x+6-leg_offset, y+75, 
                                              fill=cor_armadura, outline='#8b0000', tags='guerreiro')
        else:
            self.canvas_batalha.create_rectangle(x-6, y+50, x, y+75, 
                                              fill=cor_armadura, outline='#8b0000', tags='guerreiro')
            self.canvas_batalha.create_rectangle(x, y+50, x+6, y+75, 
                                              fill=cor_armadura, outline='#8b0000', tags='guerreiro')
    
    def desenhar_demonio_sprite(self, x, y):
        """Desenhar sprite do demônio baseado no estado atual"""
        frame = self.demonio_frame
        estado = self.demonio_estado
        
        # Definir cores baseadas no estado
        if estado == 'hurt':
            cor_principal = '#440044'
            cor_detalhes = '#660066'
        elif estado == 'dead':
            cor_principal = '#222222'
            cor_detalhes = '#333333'
        else:
            cor_principal = '#660066'
            cor_detalhes = '#9900cc'
        
        # Corpo principal
        body_size = 35 if estado == 'attack' and frame in [2, 3] else 30
        self.canvas_batalha.create_oval(x-body_size, y, x+body_size, y+60, 
                                      fill=cor_principal, outline=cor_detalhes, width=3, tags='demonio')
        
        # Cabeça/Capuz
        head_bob = 2 * (frame % 4 - 2) if estado == 'idle' else 0
        if estado == 'attack' and frame in [1, 2, 3]:
            head_bob -= 5
        
        self.canvas_batalha.create_oval(x-20, y-25+head_bob, x+20, y+10+head_bob, 
                                      fill=cor_principal, outline=cor_detalhes, width=3, tags='demonio')
        
        # Olhos brilhantes
        if estado != 'dead':
            eye_glow = '#ff0000' if estado == 'attack' else '#ffaa00'
            self.canvas_batalha.create_oval(x-12, y-15+head_bob, x-6, y-10+head_bob, 
                                          fill=eye_glow, outline='#ffffff', tags='demonio')
            self.canvas_batalha.create_oval(x+6, y-15+head_bob, x+12, y-10+head_bob, 
                                          fill=eye_glow, outline='#ffffff', tags='demonio')
        
        # Chifres
        if estado != 'dead':
            self.canvas_batalha.create_polygon(x-15, y-25+head_bob, x-10, y-40+head_bob, x-5, y-25+head_bob,
                                             fill='#333333', outline='#666666', tags='demonio')
            self.canvas_batalha.create_polygon(x+5, y-25+head_bob, x+10, y-40+head_bob, x+15, y-25+head_bob,
                                             fill='#333333', outline='#666666', tags='demonio')
        
        # Braços/Tentáculos
        if estado == 'attack':
            if frame in [1, 2, 3]:
                # Braços estendidos durante ataque
                self.canvas_batalha.create_oval(x-50, y+10, x-30, y+30, 
                                              fill=cor_principal, outline=cor_detalhes, width=2, tags='demonio')
                self.canvas_batalha.create_oval(x+30, y+10, x+50, y+30, 
                                              fill=cor_principal, outline=cor_detalhes, width=2, tags='demonio')
            else:
                # Braços recolhidos
                self.canvas_batalha.create_oval(x-40, y+20, x-25, y+35, 
                                              fill=cor_principal, outline=cor_detalhes, tags='demonio')
                self.canvas_batalha.create_oval(x+25, y+20, x+40, y+35, 
                                              fill=cor_principal, outline=cor_detalhes, tags='demonio')
        else:
            # Posição normal dos braços
            arm_sway = 2 * (frame % 6 - 3) if estado == 'idle' else 0
            self.canvas_batalha.create_oval(x-35+arm_sway, y+15, x-20+arm_sway, y+35, 
                                          fill=cor_principal, outline=cor_detalhes, tags='demonio')
            self.canvas_batalha.create_oval(x+20-arm_sway, y+15, x+35-arm_sway, y+35, 
                                          fill=cor_principal, outline=cor_detalhes, tags='demonio')
        
        # Cauda (se visível)
        if estado == 'walk':
            tail_swing = 10 * ((frame % 8) - 4) / 4
            self.canvas_batalha.create_arc(x+20, y+40, x+50+tail_swing, y+70, 
                                         fill=cor_principal, outline=cor_detalhes, width=2, tags='demonio')
    
    def desenhar_personagens(self):
        """Desenhar sprites dos personagens"""
        self.canvas_batalha.delete("all")
        
        # Background de batalha
        self.canvas_batalha.create_rectangle(0, 0, 1000, 350, fill='#001122', outline='')
        
        # Efeitos de fundo (estrelas)
        for _ in range(30):
            x = random.randint(0, 1000)
            y = random.randint(0, 200)
            self.canvas_batalha.create_oval(x, y, x+2, y+2, fill='white', outline='')
        
        # Desenhar guerreiro (lado esquerdo)
        self.desenhar_guerreiro_sprite(200, 200)
        
        # Desenhar demônio (lado direito)
        self.desenhar_demonio_sprite(700, 180)
    
    def animar_sprites(self):
        """Loop de animação dos sprites"""
        # Avançar frames
        self.guerreiro_frame = (self.guerreiro_frame + 1) % self.guerreiro_max_frames[self.guerreiro_estado]
        self.demonio_frame = (self.demonio_frame + 1) % self.demonio_max_frames[self.demonio_estado]
        
        # Redesenhar personagens
        self.desenhar_personagens()
        
        # Definir velocidade da animação baseada no estado
        delay = 200  # default
        if self.guerreiro_estado == 'attack' or self.demonio_estado == 'attack':
            delay = 150  # Mais rápido para ataques
        elif self.guerreiro_estado == 'hurt' or self.demonio_estado == 'hurt':
            delay = 100  # Muito rápido para efeito de dano
        
        # Agendar próxima animação
        self.animation_timer = self.root.after(delay, self.animar_sprites)
    
    def definir_estado_guerreiro(self, novo_estado, duracao_ms=None):
        """Definir estado do guerreiro e resetar frame"""
        self.guerreiro_estado = novo_estado
        self.guerreiro_frame = 0
        
        if duracao_ms:
            self.root.after(duracao_ms, lambda: self.definir_estado_guerreiro('idle'))
    
    def definir_estado_demonio(self, novo_estado, duracao_ms=None):
        """Definir estado do demônio e resetar frame"""
        self.demonio_estado = novo_estado
        self.demonio_frame = 0
        
        if duracao_ms:
            self.root.after(duracao_ms, lambda: self.definir_estado_demonio('idle'))
    
    def menu_atacar(self):
        """Menu de ataques físicos"""
        if not self.turno_jogador or self.animacao_ativa:
            return
            
        self.limpar_submenu()
        
        tk.Label(self.submenu_frame, text="⚔️ ATAQUES FÍSICOS",
                font=("Courier", 12, "bold"), fg='#ffff00', bg='#000066').pack(pady=10)
        
        ataques = [
            ("🗡️ Corte Rápido", lambda: self.executar_ataque_fisico(1)),
            ("⚡ Golpe Trovão", lambda: self.executar_ataque_fisico(2)),
            ("🌪️ Tornado Cortante", lambda: self.executar_ataque_fisico(3)),
            ("💥 Impacto Sísmico", lambda: self.executar_ataque_fisico(4))
        ]
        
        for nome, comando in ataques:
            btn = self.criar_botao_ff(self.submenu_frame, nome, comando, 20)
            btn.pack(pady=3, fill='x')
    
    def menu_magia(self):
        """Menu de magias"""
        if not self.turno_jogador or self.animacao_ativa:
            return
            
        self.limpar_submenu()
        
        tk.Label(self.submenu_frame, text="🔮 ARTES ARCANAS",
                font=("Courier", 12, "bold"), fg='#ffff00', bg='#000066').pack(pady=10)
        
        magias = [
            ("🔥 Fire III (15 MP)", lambda: self.executar_magia(1)),
            ("❄️ Blizzard III (18 MP)", lambda: self.executar_magia(2)),
            ("⚡ Thunder III (20 MP)", lambda: self.executar_magia(3)),
            ("🌟 Holy (25 MP)", lambda: self.executar_magia(4)),
            ("🌪️ Meteor (35 MP)", lambda: self.executar_magia(5)),
            ("💀 Death (40 MP)", lambda: self.executar_magia(6))
        ]
        
        for nome, comando in magias:
            btn = self.criar_botao_ff(self.submenu_frame, nome, comando, 25)
            btn.pack(pady=2, fill='x')
    
    def menu_itens(self):
        """Menu de itens"""
        if not self.turno_jogador or self.animacao_ativa:
            return
            
        self.limpar_submenu()
        
        tk.Label(self.submenu_frame, text="💊 INVENTÁRIO",
                font=("Courier", 12, "bold"), fg='#ffff00', bg='#000066').pack(pady=10)
        
        # Frame para itens
        items_frame = tk.Frame(self.submenu_frame, bg='#000066')
        items_frame.pack(fill='both', expand=True)
        
        # Poção de vida
        pocao_frame = tk.Frame(items_frame, bg='#000066')
        pocao_frame.pack(fill='x', pady=2)
        
        btn_pocao = self.criar_botao_ff(pocao_frame, f"❤️ Poção Vida x{self.pocoes_vida}", self.usar_pocao_vida, 20)
        btn_pocao.pack(side='left')
        if self.pocoes_vida <= 0:
            btn_pocao.config(state='disabled')
        
        # Poção de mana
        mana_frame = tk.Frame(items_frame, bg='#000066')
        mana_frame.pack(fill='x', pady=2)
        
        btn_mana = self.criar_botao_ff(mana_frame, f"💙 Éter x{self.pocoes_mana}", self.usar_pocao_mana, 20)
        btn_mana.pack(side='left')
        if self.pocoes_mana <= 0:
            btn_mana.config(state='disabled')
        
        # Elixir
        elixir_frame = tk.Frame(items_frame, bg='#000066')
        elixir_frame.pack(fill='x', pady=2)
        
        btn_elixir = self.criar_botao_ff(elixir_frame, f"✨ Elixir x{self.elixirs}", self.usar_elixir, 20)
        btn_elixir.pack(side='left')
        if self.elixirs <= 0:
            btn_elixir.config(state='disabled')
    
    def limpar_submenu(self):
        """Limpar área do submenu"""
        for widget in self.submenu_frame.winfo_children():
            widget.destroy()
    
    def adicionar_mensagem(self, mensagem):
        """Adicionar mensagem ao texto de batalha"""
        self.texto_batalha.config(state='normal')
        self.texto_batalha.insert(tk.END, mensagem + '\n')
        self.texto_batalha.config(state='disabled')
        self.texto_batalha.see(tk.END)
    
    def executar_ataque_fisico(self, tipo):
        """Executar ataques físicos com animações"""
        if not self.turno_jogador or self.animacao_ativa:
            return
        
        self.animacao_ativa = True
        self.limpar_submenu()
        
        ataques_info = {
            1: ("Corte Rápido", 25, 85, "#ffff00"),
            2: ("Golpe Trovão", 35, 70, "#4444ff"), 
            3: ("Tornado Cortante", 45, 60, "#00ff00"),
            4: ("Impacto Sísmico", 55, 50, "#ff4400")
        }
        
        nome, dano_max, precisao, cor = ataques_info[tipo]
        
        self.adicionar_mensagem(f"🗡️ {nome}!")
        
        # Definir estado de ataque para o guerreiro
        self.definir_estado_guerreiro('walk', 800)  # Caminhar até o inimigo
        
        # Executar ataque após caminhar
        self.root.after(800, lambda: self.executar_ataque_real(nome, dano_max, precisao, cor))
    
    def executar_ataque_real(self, nome, dano_max, precisao, cor):
        """Executar o ataque real após animação de aproximação"""
        # Mudar para animação de ataque
        self.definir_estado_guerreiro('attack', 600)
        
        # Calcular dano
        chance = random.randint(1, 100)
        
        if chance <= precisao:
            dano = random.randint(int(dano_max * 0.8), dano_max)
            self.vida_inimigo -= dano
            
            # Inimigo recebe dano
            self.definir_estado_demonio('hurt', 400)
            
            # Efeito visual de acerto
            self.root.after(300, lambda: self.efeito_impacto_fisico(cor))
            
            self.adicionar_mensagem(f"💥 Acertou! {dano} de dano!")
        else:
            self.adicionar_mensagem("💨 Errou!")
        
        self.root.after(1000, self.verificar_fim_turno)
    
    def efeito_impacto_fisico(self, cor):
        """Criar efeito visual de impacto físico"""
        for i in range(5):
            self.canvas_batalha.create_oval(680, 160, 720, 200, 
                                          fill=cor, outline='white', 
                                          width=3, tags='efeito')
            self.root.after(100)
            self.root.update()
            self.canvas_batalha.delete('efeito')
            self.root.after(100)
            self.root.update()
    
    def executar_magia(self, tipo):
        """Executar magias com animações"""
        if not self.turno_jogador or self.animacao_ativa:
            return
        
        magias_info = {
            1: ("Fire III", 40, 80, 15, "#ff4400"),
            2: ("Blizzard III", 38, 85, 18, "#00aaff"),
            3: ("Thunder III", 42, 75, 20, "#ffff00"),
            4: ("Holy", 50, 90, 25, "#ffffff"),
            5: ("Meteor", 70, 60, 35, "#ff0000"),
            6: ("Death", 999, 25, 40, "#800080")
        }
        
        nome, dano_max, precisao, custo_mp, cor = magias_info[tipo]
        
        if self.mana_jogador < custo_mp:
            self.adicionar_mensagem("❌ MP insuficiente!")
            return
        
        self.animacao_ativa = True
        self.limpar_submenu()
        
        self.mana_jogador -= custo_mp
        self.atualizar_status()
        
        self.adicionar_mensagem(f"🔮 {nome}!")
        
        # Animação de conjuração
        self.definir_estado_guerreiro('idle')  # Guerreiro fica parado conjurando
        
        # Executar magia
        self.animar_magia(tipo, nome, dano_max, precisao, cor)
    
    def animar_magia(self, tipo, nome, dano_max, precisao, cor):
        """Animar efeitos mágicos"""
        chance = random.randint(1, 100)
        
        if chance <= precisao:
            if tipo == 6:  # Death
                if random.randint(1, 100) <= 25:  # 25% de chance de morte instantânea
                    dano = self.vida_inimigo
                else:
                    dano = random.randint(20, 40)
            else:
                dano = random.randint(int(dano_max * 0.8), dano_max)
            
            self.vida_inimigo -= dano
            
            # Inimigo recebe dano mágico
            self.definir_estado_demonio('hurt', 600)
            
            # Efeitos visuais específicos por magia
            if tipo == 1:  # Fire
                self.efeito_fogo()
            elif tipo == 2:  # Blizzard
                self.efeito_gelo()
            elif tipo == 3:  # Thunder
                self.efeito_raio()
            elif tipo == 4:  # Holy
                self.efeito_holy()
            elif tipo == 5:  # Meteor
                self.efeito_meteor()
            elif tipo == 6:  # Death
                self.efeito_death()
            
            self.adicionar_mensagem(f"✨ Acertou! {dano} de dano!")
        else:
            self.adicionar_mensagem("💨 A magia falhou!")
        
        self.root.after(1500, self.verificar_fim_turno)
    
    def efeito_fogo(self):
        """Efeito visual de fogo"""
        def animar():
            for i in range(20):
                x = random.randint(660, 740)
                y = random.randint(140, 220)
                size = random.randint(5, 15)
                
                chama = self.canvas_batalha.create_oval(x, y, x+size, y+size,
                                                      fill=random.choice(['#ff4400', '#ff6600', '#ffaa00']),
                                                      outline='', tags='efeito')
                self.root.after(50)
                self.root.update()
            
            self.root.after(500, lambda: self.canvas_batalha.delete('efeito'))
        
        threading.Thread(target=animar, daemon=True).start()
    
    def efeito_gelo(self):
        """Efeito visual de gelo"""
        def animar():
            for i in range(15):
                x = random.randint(660, 740)
                y = random.randint(140, 220) 
                
                gelo = self.canvas_batalha.create_polygon(x, y, x+10, y+20, x-10, y+20,
                                                        fill='#88ddff', outline='#ffffff',
                                                        width=2, tags='efeito')
                self.root.after(80)
                self.root.update()
            
            self.root.after(500, lambda: self.canvas_batalha.delete('efeito'))
        
        threading.Thread(target=animar, daemon=True).start()
    
    def efeito_raio(self):
        """Efeito visual de raio"""
        def animar():
            for i in range(8):
                raio = self.canvas_batalha.create_line(700, 0, 700, 350,
                                                     fill='#ffff00', width=8, tags='efeito')
                self.root.after(100)
                self.root.update()
                self.canvas_batalha.delete('efeito')
                self.root.after(100)
                self.root.update()
        
        threading.Thread(target=animar, daemon=True).start()
    
    def efeito_holy(self):
        """Efeito visual de Holy"""
        def animar():
            for i in range(10):
                luz = self.canvas_batalha.create_oval(650, 130, 750, 230,
                                                    fill='#ffffff', outline='#ffff00',
                                                    width=3, tags='efeito')
                self.root.after(150)
                self.root.update()
                self.canvas_batalha.delete('efeito')
                self.root.after(100)
                self.root.update()
        
        threading.Thread(target=animar, daemon=True).start()
    
    def efeito_meteor(self):
        """Efeito visual de Meteor"""
        def animar():
            # Meteoros caindo
            for i in range(5):
                x_start = random.randint(600, 800)
                meteor = self.canvas_batalha.create_oval(x_start, 0, x_start+20, 20,
                                                       fill='#ff4400', outline='#ff0000',
                                                       width=2, tags='efeito')
                
                # Animar queda
                for j in range(15):
                    self.canvas_batalha.move(meteor, -2, 15)
                    self.root.after(30)
                    self.root.update()
                
                # Explosão
                self.canvas_batalha.create_oval(650, 180, 750, 280,
                                              fill='#ff8800', outline='#ff0000',
                                              width=3, tags='efeito')
                self.root.after(200)
                self.root.update()
            
            self.root.after(800, lambda: self.canvas_batalha.delete('efeito'))
        
        threading.Thread(target=animar, daemon=True).start()
    
    def efeito_death(self):
        """Efeito visual de Death"""
        def animar():
            for i in range(12):
                # Círculo negro crescente
                size = i * 8
                morte = self.canvas_batalha.create_oval(700-size, 200-size, 700+size, 200+size,
                                                      fill='#800080', outline='#000000',
                                                      width=3, tags='efeito')
                self.root.after(120)
                self.root.update()
                
                if i > 6:
                    self.canvas_batalha.delete(morte)
            
            self.root.after(500, lambda: self.canvas_batalha.delete('efeito'))
        
        threading.Thread(target=animar, daemon=True).start()
    
    def usar_pocao_vida(self):
        """Usar poção de vida"""
        if self.pocoes_vida <= 0 or not self.turno_jogador:
            return
        
        self.pocoes_vida -= 1
        cura = random.randint(40, 60)
        self.vida_jogador = min(self.vida_jogador + cura, self.max_vida_jogador)
        
        self.adicionar_mensagem(f"❤️ Poção usada! Recuperou {cura} HP!")
        
        # Animação de uso de item
        self.definir_estado_guerreiro('idle')  # Guerreiro usa item
        
        # Efeito visual de cura
        def efeito_cura():
            for i in range(8):
                x = random.randint(180, 220)
                y = random.randint(180, 240)
                cura_fx = self.canvas_batalha.create_text(x, y, text="+", 
                                                        font=("Arial", 16, "bold"),
                                                        fill='#00ff00', tags='efeito')
                self.root.after(100)
                self.root.update()
            
            self.root.after(500, lambda: self.canvas_batalha.delete('efeito'))
        
        threading.Thread(target=efeito_cura, daemon=True).start()
        
        self.atualizar_status()
        self.root.after(800, self.verificar_fim_turno)
    
    def usar_pocao_mana(self):
        """Usar poção de mana"""
        if self.pocoes_mana <= 0 or not self.turno_jogador:
            return
        
        self.pocoes_mana -= 1
        recuperacao = random.randint(30, 50)
        self.mana_jogador = min(self.mana_jogador + recuperacao, self.max_mana_jogador)
        
        self.adicionar_mensagem(f"💙 Éter usado! Recuperou {recuperacao} MP!")
        
        # Efeito visual de recuperação de mana
        def efeito_mana():
            for i in range(6):
                x = random.randint(180, 220)
                y = random.randint(180, 240)
                mana_fx = self.canvas_batalha.create_oval(x, y, x+8, y+8,
                                                        fill='#4444ff', outline='#6666ff',
                                                        tags='efeito')
                self.root.after(120)
                self.root.update()
            
            self.root.after(500, lambda: self.canvas_batalha.delete('efeito'))
        
        threading.Thread(target=efeito_mana, daemon=True).start()
        
        self.atualizar_status()
        self.root.after(800, self.verificar_fim_turno)
    
    def usar_elixir(self):
        """Usar elixir (cura tudo)"""
        if self.elixirs <= 0 or not self.turno_jogador:
            return
        
        self.elixirs -= 1
        self.vida_jogador = self.max_vida_jogador
        self.mana_jogador = self.max_mana_jogador
        
        self.adicionar_mensagem("✨ Elixir usado! HP e MP restaurados!")
        
        # Efeito visual dourado
        def efeito_elixir():
            for i in range(15):
                x = random.randint(170, 230)
                y = random.randint(170, 250)
                elixir_fx = self.canvas_batalha.create_oval(x, y, x+12, y+12,
                                                          fill='#ffdd00', outline='#ffaa00',
                                                          width=2, tags='efeito')
                self.root.after(80)
                self.root.update()
            
            self.root.after(800, lambda: self.canvas_batalha.delete('efeito'))
        
        threading.Thread(target=efeito_elixir, daemon=True).start()
        
        self.atualizar_status()
        self.root.after(1000, self.verificar_fim_turno)
    
    def defender(self):
        """Ação de defender"""
        if not self.turno_jogador or self.animacao_ativa:
            return
        
        self.limpar_submenu()
        self.adicionar_mensagem("🛡️ Você se prepara para defender!")
        
        # Definir estado de defesa
        self.definir_estado_guerreiro('idle')  # Posição defensiva
        self.defendendo = True
        
        # Efeito visual de defesa
        def efeito_defesa():
            defesa_fx = self.canvas_batalha.create_oval(180, 180, 220, 220,
                                                      fill='', outline='#00aaff',
                                                      width=4, tags='defesa')
            self.root.after(500)
            self.root.update()
        
        threading.Thread(target=efeito_defesa, daemon=True).start()
        
        # Recuperar um pouco de MP
        self.mana_jogador = min(self.mana_jogador + 10, self.max_mana_jogador)
        self.atualizar_status()
        
        self.root.after(800, self.verificar_fim_turno)
    
    def turno_inimigo(self):
        """Turno do inimigo"""
        if self.vida_inimigo <= 0:
            return
        
        self.turno_jogador = False
        self.animacao_ativa = True
        self.limpar_submenu()
        
        # IA do inimigo
        acao = random.randint(1, 100)
        
        if acao <= 40:  # Ataque físico
            self.inimigo_ataque_fisico()
        elif acao <= 70:  # Magia
            self.inimigo_magia()
        elif acao <= 85:  # Habilidade especial
            self.inimigo_habilidade_especial()
        else:  # Curar
            self.inimigo_curar()
    
    def inimigo_ataque_fisico(self):
        """Inimigo executa ataque físico"""
        ataques = [
            ("Garra Sombria", 30, 80, "#660000"),
            ("Investida Brutal", 40, 65, "#990000"),
            ("Cauda Demolidora", 35, 70, "#cc0000")
        ]
        
        nome, dano_max, precisao, cor = random.choice(ataques)
        self.adicionar_mensagem(f"👹 {nome}!")
        
        # Animação do inimigo atacando
        self.definir_estado_demonio('attack', 800)
        
        # Executar ataque após animação
        def executar_ataque_inimigo():
            chance = random.randint(1, 100)
            if chance <= precisao:
                dano = random.randint(int(dano_max * 0.7), dano_max)
                
                # Reduzir dano se estava defendendo
                if hasattr(self, 'defendendo') and self.defendendo:
                    dano = int(dano * 0.5)
                    self.adicionar_mensagem("🛡️ Dano reduzido pela defesa!")
                    self.defendendo = False
                
                self.vida_jogador -= dano
                
                # Guerreiro recebe dano
                self.definir_estado_guerreiro('hurt', 400)
                
                self.adicionar_mensagem(f"💥 Você recebeu {dano} de dano!")
            else:
                self.adicionar_mensagem("💨 O ataque errou!")
        
        self.root.after(400, executar_ataque_inimigo)
        self.root.after(1200, self.fim_turno_inimigo)
    
    def inimigo_magia(self):
        """Inimigo usa magia"""
        if self.mana_inimigo < 15:
            self.inimigo_ataque_fisico()
            return
        
        magias = [
            ("Bola de Fogo Negra", 35, 75, 15),
            ("Rajada Sombria", 28, 85, 12),
            ("Tempestade Infernal", 45, 60, 20)
        ]
        
        nome, dano_max, precisao, custo = random.choice(magias)
        self.mana_inimigo -= custo
        
        self.adicionar_mensagem(f"👹 {nome}!")
        
        # Demônio conjura magia
        self.definir_estado_demonio('idle')  # Posição de conjuração
        
        def animar_magia_inimiga():
            # Efeito visual de magia sombria
            for i in range(10):
                x = random.randint(150, 250)
                y = random.randint(150, 250)
                sombra = self.canvas_batalha.create_oval(x, y, x+15, y+15,
                                                       fill='#800080', outline='#ff00ff',
                                                       tags='efeito_inimigo')
                self.root.after(100)
                self.root.update()
            
            chance = random.randint(1, 100)
            if chance <= precisao:
                dano = random.randint(int(dano_max * 0.8), dano_max)
                self.vida_jogador -= dano
                
                # Guerreiro recebe dano mágico
                self.definir_estado_guerreiro('hurt', 500)
                
                self.adicionar_mensagem(f"🔮 Você recebeu {dano} de dano mágico!")
            else:
                self.adicionar_mensagem("✨ A magia foi resistida!")
            
            self.root.after(500, lambda: self.canvas_batalha.delete('efeito_inimigo'))
        
        threading.Thread(target=animar_magia_inimiga, daemon=True).start()
        
        self.root.after(1200, self.fim_turno_inimigo)
    
    def inimigo_habilidade_especial(self):
        """Habilidades especiais do inimigo"""
        habilidades = [
            "Rugido Intimidador",
            "Regeneração Sombria", 
            "Aura de Terror"
        ]
        
        habilidade = random.choice(habilidades)
        self.adicionar_mensagem(f"👹 {habilidade}!")
        
        # Animação especial
        self.definir_estado_demonio('idle')
        
        if habilidade == "Rugido Intimidador":
            # Reduz MP do jogador
            reducao = random.randint(10, 20)
            self.mana_jogador = max(0, self.mana_jogador - reducao)
            self.adicionar_mensagem(f"😨 Seu MP foi reduzido em {reducao}!")
            
        elif habilidade == "Regeneração Sombria":
            # Inimigo se cura
            cura = random.randint(20, 35)
            self.vida_inimigo = min(self.vida_inimigo + cura, self.max_vida_inimigo)
            self.adicionar_mensagem(f"🩸 Inimigo recuperou {cura} HP!")
            
        elif habilidade == "Aura de Terror":
            # Próximo ataque do jogador tem precisão reduzida
            self.adicionar_mensagem("😱 Você se sente amedrontado!")
        
        self.root.after(1000, self.fim_turno_inimigo)
    
    def inimigo_curar(self):
        """Inimigo tenta se curar"""
        if self.vida_inimigo >= self.max_vida_inimigo * 0.8:
            self.inimigo_ataque_fisico()
            return
        
        self.adicionar_mensagem("👹 O demônio concentra energia sombria...")
        
        def efeito_cura_inimiga():
            for i in range(6):
                x = random.randint(680, 720)
                y = random.randint(160, 200)
                cura_fx = self.canvas_batalha.create_text(x, y, text="+",
                                                        font=("Arial", 14, "bold"),
                                                        fill='#990000', tags='cura_inimiga')
                self.root.after(120)
                self.root.update()
            
            cura = random.randint(25, 40)
            self.vida_inimigo = min(self.vida_inimigo + cura, self.max_vida_inimigo)
            self.adicionar_mensagem(f"🩸 Inimigo recuperou {cura} HP!")
            
            self.root.after(500, lambda: self.canvas_batalha.delete('cura_inimiga'))
        
        threading.Thread(target=efeito_cura_inimiga, daemon=True).start()
        
        self.root.after(1000, self.fim_turno_inimigo)
    
    def fim_turno_inimigo(self):
        """Finalizar turno do inimigo"""
        self.atualizar_status()
        self.canvas_batalha.delete('defesa')
        
        if self.vida_jogador <= 0:
            self.fim_de_jogo(False)
        else:
            self.turno_jogador = True
            self.animacao_ativa = False
    
    def verificar_fim_turno(self):
        """Verificar se deve passar o turno"""
        self.atualizar_status()
        
        if self.vida_inimigo <= 0:
            self.fim_de_jogo(True)
        else:
            self.animacao_ativa = False
            self.root.after(500, self.turno_inimigo)
    
    def atualizar_status(self):
        """Atualizar barras de status"""
        # Atualizar herói
        self.hp_jogador_bar['value'] = max(0, self.vida_jogador)
        self.hp_jogador_label.config(text=f"{max(0, self.vida_jogador)}/{self.max_vida_jogador}")
        
        self.mp_jogador_bar['value'] = max(0, self.mana_jogador)
        self.mp_jogador_label.config(text=f"{max(0, self.mana_jogador)}/{self.max_mana_jogador}")
        
        # Atualizar inimigo
        self.hp_inimigo_bar['value'] = max(0, self.vida_inimigo)
        self.hp_inimigo_label.config(text=f"{max(0, self.vida_inimigo)}/{self.max_vida_inimigo}")
    
    def fim_de_jogo(self, vitoria):
        """Finalizar o jogo"""
        self.animacao_ativa = True
        self.limpar_submenu()
        
        if vitoria:
            self.adicionar_mensagem("🎉 VITÓRIA! O Demônio das Sombras foi derrotado! 🎉")
            self.adicionar_mensagem("✨ Você ganhou 500 EXP e 200 Gil! ✨")
            
            # Definir estado de vitória
            self.definir_estado_guerreiro('idle')  # Pose de vitória
            self.definir_estado_demonio('dead')    # Demônio derrotado
            
            # Animação de vitória
            def vitoria_animation():
                for i in range(20):
                    x = random.randint(50, 950)
                    y = random.randint(50, 300)
                    estrela = self.canvas_batalha.create_polygon(
                        x, y-10, x+3, y-3, x+10, y, x+3, y+3, x, y+10,
                        x-3, y+3, x-10, y, x-3, y-3,
                        fill='#ffdd00', outline='#ffaa00', tags='vitoria')
                    self.root.after(100)
                    self.root.update()
            
            threading.Thread(target=vitoria_animation, daemon=True).start()
            
        else:
            self.adicionar_mensagem("💀 DERROTA! Você foi consumido pelas sombras... 💀")
            self.adicionar_mensagem("🔄 Tente novamente para provar seu valor!")
            
            # Definir estados de derrota
            self.definir_estado_guerreiro('dead')
            self.definir_estado_demonio('idle')  # Demônio vitorioso
        
        # Parar animações
        if self.animation_timer:
            self.root.after_cancel(self.animation_timer)
        
        # Botão reiniciar
        self.btn_restart = self.criar_botao_ff(self.submenu_frame, "🔄 NOVA BATALHA", self.reiniciar_jogo, 20)
        self.btn_restart.pack(pady=20)
    
    def reiniciar_jogo(self):
        """Reiniciar o jogo"""
        # Cancelar timer anterior se existir
        if self.animation_timer:
            self.root.after_cancel(self.animation_timer)
        
        # Resetar valores
        self.vida_jogador = self.max_vida_jogador
        self.mana_jogador = self.max_mana_jogador
        self.vida_inimigo = self.max_vida_inimigo
        self.mana_inimigo = self.max_mana_inimigo
        
        # Resetar itens
        self.pocoes_vida = 3
        self.pocoes_mana = 2
        self.elixirs = 1
        
        # Resetar estados
        self.turno_jogador = True
        self.animacao_ativa = False
        self.defendendo = False
        
        # Resetar estados dos sprites
        self.guerreiro_estado = 'idle'
        self.guerreiro_frame = 0
        self.demonio_estado = 'idle'
        self.demonio_frame = 0
        
        # Limpar canvas e redesenhar
        self.canvas_batalha.delete('all')
        self.desenhar_personagens()
        
        # Limpar texto
        self.texto_batalha.config(state='normal')
        self.texto_batalha.delete(1.0, tk.END)
        self.texto_batalha.config(state='disabled')
        
        # Atualizar interface
        self.atualizar_status()
        self.limpar_submenu()
        
        # Reiniciar animações
        self.animar_sprites()
        
        # Mensagem inicial
        self.iniciar_batalha()
    
    def iniciar_batalha(self):
        """Inicializar a batalha"""
        self.adicionar_mensagem("⚔️ Uma nova batalha épica começou! ⚔️")
        self.adicionar_mensagem("👹 O Demônio das Sombras emerge das trevas!")
        self.adicionar_mensagem("🗡️ Escolha sua ação sabiamente...")

# Executar o jogo
if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    
    # Configurar ícone se disponível
    try:
        # Criar um ícone simples usando texto
        root.iconbitmap('default')
    except:
        pass
    
    jogo = FFBattleSystem(root)
    
    root.mainloop()