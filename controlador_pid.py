from manim import *
import numpy as np
from textwrap import wrap
import textwrap
# from manim import *
import numpy as np

# Se você não tiver a biblioteca "python-control" instalada, use:
#   pip install slycot control
import control


class PID(Scene):
    def construct(self):
        self.IntroScene()
        self.ObjetivosScene()
        self.Basico()
        self.Intro_pt1()
        self.Intro_pt2()
        self.Intro_pt3()
        self.DesenvolvimentoScene()
        # self.PIDFeedbackDiagram()
        self.Proporcional()
        self.Ilust_prop()
        self.Integral_pt1()
        self.Integral_pt2()
        self.Ilust_int()
        self.Derivativo_pt1()
        self.Derivativo_pt2()
        self.Ilust_der()
        self.AulaSintonizacaoPID()
        self.AlocacaoDePolos()
        self.ExemploAlocacaoPolos()
        self.ConclusaoScene()
    
    def IntroScene(self):
        # Título principal
        titulo = Text("Miniaula: Controladores PID", font_size=48).move_to(ORIGIN)
        # Subtítulo
        subtitulo = Text("Projeto de controladores", font_size=36).next_to(titulo, DOWN)
        nome = Text("Tiago Barretto Sant'Anna", font_size=26).next_to(subtitulo, (2*DOWN))

        # Animações
        self.play(Write(titulo))
        self.play(FadeIn(subtitulo, shift=DOWN))
        self.play(FadeIn(nome))
        self.wait(2)

        # Animação de saída
        self.play(FadeOut(titulo), FadeOut(subtitulo), FadeOut(nome))
        self.wait()

    def ObjetivosScene(self):
        # Título para a cena
        titulo = Text("Objetivos da Miniaula", font_size=48).to_edge(UP+LEFT)
        self.play(Write(titulo))
        self.wait(1)

        # Lista de objetivos (bullet points)
        objetivos = BulletedList(
            "Componentes de Controle",
            "Introdução ao Controle PID",
            "Fundamentos Teóricos do Controlador PID",
            "Projeto e Sintonização do Controlador PID",
            "Exemplo Prático e Implementação",
            font_size=40
        ).next_to(titulo, DOWN, buff=1.0)

        # Animação de cada item
        for item in objetivos:
            self.play(FadeIn(item, shift=RIGHT))
            self.wait(0.5)

        self.wait(2)
        self.play(FadeOut(titulo), FadeOut(objetivos))

        self.wait()

    def Basico(self):
 # =======================================================
        # 1) TÍTULO PRINCIPAL
        # =======================================================
        titulo = Text("Componentes de Controle", font_size=40).to_edge(UP)
        self.play(Write(titulo))
        self.wait(1)

        # =======================================================
        # 2) CRIAÇÃO DOS ELEMENTOS DO DIAGRAMA
        # =======================================================
        
        # (a) Nó de soma (erro e(t) = x(t) - y(t))
        summation = Circle(radius=0.3, color=WHITE).move_to(LEFT*4)
        sum_label = Text("∑", font_size=28).move_to(summation.get_center())
        
        # (b) Seta e rótulo da entrada x(t)
        x_label = MathTex("x(t)", font_size=30).next_to(summation, LEFT, buff=0.4)
        input_arrow = Arrow(
            start=x_label.get_right(),
            end=summation.get_left(),
            buff=0.1
        )
        
        # (c) Seta de saída do nó de soma para o controlador (erro e(t))
        pid_block = Rectangle(width=1.6, height=1, color=WHITE).move_to(LEFT*1.5)
        pid_text = Text("PID", font_size=24).move_to(pid_block.get_center())
        
        arrow_e = Arrow(
            start=summation.get_right(),
            end=pid_block.get_left(),
            buff=0.2
        )
        e_label = MathTex("e(t)", font_size=30).next_to(arrow_e, UP, buff=0.1)
        
        # (d) Seta de saída do controlador para a planta (u(t))
        plant_block = Rectangle(width=1.6, height=1, color=WHITE).move_to(RIGHT*1.5)
        plant_text = Text("Planta", font_size=24).move_to(plant_block.get_center())
        
        arrow_u = Arrow(
            start=pid_block.get_right(),
            end=plant_block.get_left(),
            buff=0.2
        )
        u_label = MathTex("u(t)", font_size=30).next_to(arrow_u, UP, buff=0.1)
        
        # (e) Seta de saída da planta (y(t)) para a direita
        output_arrow = Arrow(
            start=plant_block.get_right(),
            end=RIGHT*4,
            buff=0.2
        )
        y_label = MathTex("y(t)", font_size=30).next_to(output_arrow, UP, buff=0.1)
        
        # (f) Realimentação (feedback) da saída y(t) de volta ao nó de soma
        feedback_arrow = CurvedArrow(
            start_point=RIGHT*3.8 + DOWN*0.3,  # próximo ao final do output_arrow
            end_point=summation.get_bottom(),
            angle=-TAU/4,  # curvatura para cima
            color=WHITE
        )
        y_feedback_label = MathTex("y(t)", font_size=30).next_to(feedback_arrow, DOWN, buff=0.1)
        
        # Agrupa todos os objetos do diagrama para manipular
        diagrama = VGroup(
            summation, sum_label, x_label, input_arrow,
            pid_block, pid_text, arrow_e, e_label,
            plant_block, plant_text, arrow_u, u_label,
            output_arrow, y_label,
            feedback_arrow, y_feedback_label
        )

        # =======================================================
        # 3) EXIBIÇÃO INICIAL DO DIAGRAMA
        # =======================================================
        self.play(Create(summation), Write(sum_label))
        self.play(Write(x_label), Create(input_arrow))
        self.play(Create(arrow_e), Write(e_label))
        self.play(Create(pid_block), Write(pid_text))
        self.play(Create(arrow_u), Write(u_label))
        self.play(Create(plant_block), Write(plant_text))
        self.play(Create(output_arrow), Write(y_label))
        self.play(Create(feedback_arrow), Write(y_feedback_label))
        self.wait(1)

        # =======================================================
        # 4) DEFINIÇÕES PASSO A PASSO
        # =======================================================
        
        # Função auxiliar para exibir cada definição de forma destacada
        def exibir_definicao(texto_def, mobj_destacado):
            # Cria um retângulo de destaque ao redor do objeto
            highlight = SurroundingRectangle(mobj_destacado, color=YELLOW, buff=0.15)
            
            # Texto de definição aparece logo abaixo do título
            definicao = Text(
                texto_def,
                font_size=24,
                color=YELLOW
            ).next_to(titulo, DOWN, buff=0.5)

            self.play(Create(highlight), FadeIn(definicao))
            self.wait(2)
            self.play(FadeOut(definicao), Uncreate(highlight))

        # 4.1) Summation (nó de soma)
        exibir_definicao(
            "Nó de Soma: Calcula o erro e(t) = x(t) - y(t).",
            summation
        )

        # 4.2) Sinal de entrada x(t)
        exibir_definicao(
            "x(t): Sinal de entrada ou referência (setpoint).",
            x_label
        )

        # 4.3) Erro e(t)
        exibir_definicao(
            "e(t): Diferença entre a referência e a saída realimentada.",
            e_label
        )

        # 4.4) Controlador PID
        exibir_definicao(
            "Controlador (PID): Gera o sinal de controle para corrigir o erro.",
            pid_block
        )

        # 4.5) Sinal de controle u(t)
        exibir_definicao(
            "u(t): Sinal de controle aplicado à Planta.",
            u_label
        )

        # 4.6) Planta
        exibir_definicao(
            "Planta (Processo): Sistema físico a ser controlado.",
            plant_block
        )

        # 4.7) Saída y(t)
        exibir_definicao(
            "y(t): Saída do sistema (Planta).",
            y_label
        )

        # 4.8) Realimentação (feedback)
        exibir_definicao(
            "Realimentação: Retorna y(t) ao nó de soma para comparação com x(t).",
            feedback_arrow
        )

        self.wait(1)

        # =======================================================
        # 5) AMPLIAÇÃO DA PLANTA
        # =======================================================
        #
        # Remove todos os componentes, exceto o bloco da planta.
        # Vamos "transformar" a planta num retângulo maior
        # e inserir novos blocos de "Atuador" e "Sistema" dentro dela.
        
        # 5.1) Remove todos os outros elementos
        outros_componentes = [
            summation, sum_label, x_label, input_arrow,
            pid_block, pid_text, arrow_e, e_label,
            arrow_u, u_label,
            output_arrow, y_label,
            feedback_arrow, y_feedback_label
        ]
        self.play(*[FadeOut(mobj) for mobj in outros_componentes])
        self.wait(1)

        # 5.2) Transforma o bloco "plant_block" num retângulo maior
        big_plant_rect = Rectangle(width=7, height=3.5, color=WHITE)
        big_plant_rect.move_to(ORIGIN)
        
        self.play(
            Transform(plant_block, big_plant_rect),
        )
        self.wait(1)
        self.play(FadeOut(plant_text))

        # 5.3) Dentro dessa "Planta", criaremos dois blocos:
        #      "Atuador" e "Sistema"
        atuador_box = Rectangle(width=2.5, height=1.2, color=WHITE)
        atuador_box.move_to(LEFT*1.8)  # posicionado dentro do retângulo maior
        atuador_text = Text("Atuador", font_size=24).move_to(atuador_box.get_center())
        atuador_group = VGroup(atuador_box, atuador_text)

        sistema_box = Rectangle(width=2.5, height=1.2, color=WHITE)
        sistema_box.move_to(RIGHT*1.8)
        sistema_text = Text("Sistema", font_size=24).move_to(sistema_box.get_center())
        sistema_group = VGroup(sistema_box, sistema_text)

        arrow_atuador_sistema = Arrow(
            start=atuador_box.get_right(),
            end=sistema_box.get_left(),
            buff=0.2
        )

        # Exibir os novos blocos
        self.play(
            Create(atuador_box), Write(atuador_text),
            Create(sistema_box), Write(sistema_text),
            Create(arrow_atuador_sistema),
        )
        self.wait(1)

        # =======================================================
        # 6) DEFINIÇÕES DE ATUADOR E SISTEMA (DENTRO DA PLANTA)
        # =======================================================
        #
        # Usamos novamente a função exibir_definicao para cada um.
        
        exibir_definicao(
            "Atuador: Converte o sinal de controle em ação física na planta.",
            atuador_group
        )

        exibir_definicao(
            "Sistema: A parte física principal que se deseja controlar.",
            sistema_group
        )

        self.wait(1)

        # =======================================================
        # 7) ENCERRAMENTO
                # Agrupa todos os elementos restantes para dar fade out
        componentes_restantes = VGroup(
            titulo, plant_block,
            atuador_group, sistema_group, arrow_atuador_sistema
        )
        self.play(FadeOut(componentes_restantes))
        self.wait(1)
                # =========================
     
  
        # encerramento = Text("Fim da Apresentação", font_size=32).to_edge(DOWN)
        # self.play(Write(encerramento))
        # self.wait(2)

        # self.play(*[FadeOut(mobj) for mobj in self.mobjects])
        # self.wait(1)

    def Intro_pt1(self):
        # Título da cena
        title = Text("Fundamentos Teóricos do Controlador PID", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Descrição do cenário
        description = Text(
            "Exemplo: Um ar condicionado mantém a temperatura \nde um ambiente constante.",
            font_size=30
        ).next_to(title, DOWN, buff=0.5)
        self.play(Write(description))
        self.wait(2)

        # Cria o objeto de imagem (substitua 'caminho/para/sua/imagem.png' pelo caminho real da imagem)
        imagem = ImageMobject("images/arcondicionado.webp")
        # Redimensiona a imagem (opcional)
        imagem.scale(0.5)
        # Posiciona a imagem (por exemplo, à esquerda)
        imagem.to_edge(LEFT)
        # imagem = 
        self.play(imagem.animate.shift(DOWN * 0.5))

        imagem2 = ImageMobject("images/casa.png")
        # Redimensiona a imagem (opcional)
        imagem2.scale(0.5)
        # Posiciona a imagem (por exemplo, à esquerda)
        imagem2.to_edge(RIGHT)
        # imagem = 
        self.play(imagem2.animate.shift(DOWN * 0.5))
        self.wait(2)

        # muda o texto
        self.play(
            FadeOut(description),
        )
        self.wait(0.5)

        # Descrição do cenário
        description = Text(
            "Como um ar condicionado atinge e mantém uma \ntemperatura desejada?",
            font_size=30
        ).next_to(title, DOWN, buff=0.5)
        self.play(Write(description))
        self.wait(2)

        # Encerramento: fade out de todos os elementos
        self.play(
            FadeOut(title),
            FadeOut(description),
            FadeOut(imagem),
            FadeOut(imagem2),
        )
        self.wait(1)
    
    def Intro_pt3(self):
        # Título da cena
        title = Text("Fundamentos Teóricos do Controlador PID", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Descrição do cenário
        # description = Text(
        #     "Exemplo: Um ar condicionado mantém a temperatura\n"
        #     "de um ambiente constante. Comparação entre controle\n"
        #     "sem PID e com PID.",
        #     font_size=20
        # ).next_to(title, DOWN, buff=0.5)
        # self.play(Write(description))
        # self.wait(2)
        
        # Criação dos eixos para o gráfico
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[10, 20, 2],
            x_length=7,
            y_length=4,
            axis_config={"include_numbers": True},
            tips=False
        ).to_edge(DOWN, buff=1)
        
        # Labels dos eixos
        axes_labels = axes.get_axis_labels(x_label="Tempo (s)", y_label="Temperatura (°C)")
        self.play(Create(axes), Write(axes_labels))
        self.wait(1)
        
        # Funções que simulam a variação da temperatura
        # Sem PID: resposta lenta com pequenas oscilações
        # func_no_pid = lambda t: 22 + 8 * np.exp(-t/10) * (1 + 0.2 * np.sin(2 * np.pi * t / 2))
        def func_no_pid(t):
            if t < 1.1:
                return 20 - t**2 - 2*t
            return 16 + 1 * np.sin((2 * np.pi / 2) * t)  # amplitude = 2, período = 2
        # Com PID: resposta rápida e suave
        func_pid = lambda t: 16 + 4 * np.exp(-t/1.5)
        
        # Plotagem das curvas no mesmo sistema de eixos
        graph_no_pid = axes.plot(func_no_pid, x_range=[0, 10], color=RED)
        graph_pid = axes.plot(func_pid, x_range=[0, 10], color=GREEN)
        
        # Legendas para identificar as curvas
        label_no_pid = Text("Sem PID", font_size=24, color=RED).next_to(graph_no_pid.get_end(), DOWN*5, buff=0.1) # TODO: mudar isso
        label_pid = Text("Com PID", font_size=24, color=GREEN).next_to(graph_pid.get_end(), UP, buff=0.1)
        
        # Exibe as curvas e as legendas
        self.play(Create(graph_no_pid), Write(label_no_pid))
        self.play(Create(graph_pid), Write(label_pid))
        self.wait(3)
        
        # Encerramento: fade out de todos os elementos
        self.play(
            FadeOut(title),
            # FadeOut(description),
            FadeOut(axes),
            FadeOut(axes_labels),
            FadeOut(graph_no_pid),
            FadeOut(graph_pid),
            FadeOut(label_no_pid),
            FadeOut(label_pid)
        )
        self.wait(1)

    def DesenvolvimentoScene(self):
        # Título
        titulo = Text("Fundamentos Teóricos do Controlador PID", font_size=42).to_edge(UP)
        self.play(Write(titulo))
        self.wait(1)

        # Texto explicativo
        texto_explicativo = Text(
            "O controlador PID é composto pelos termos\nProporcional (P), Integral (I) e Derivativo (D).",
            font_size=26
        ).next_to(titulo, DOWN, buff=1)
        self.play(Write(texto_explicativo))
        self.wait(2)

        # Equação em LaTeX dividida em partes para facilitar o destaque
        eq_pid = MathTex(
            r"u(t) =",                # Índice 0
            r"K_p \, e(t)",           # Índice 1 - Termo Proporcional
            r"+",                     # Índice 2
            r"K_i \int e(t)\,dt",     # Índice 3 - Termo Integral
            r"+",                     # Índice 4
            r"K_d \,\frac{d e(t)}{dt}" # Índice 5 - Termo Derivativo
        ).scale(0.8).next_to(texto_explicativo, DOWN, buff=1)
        self.play(Write(eq_pid))
        self.wait(2)

        # Destacar o Termo Proporcional com retângulo e tópico
        rect_proporcional = SurroundingRectangle(eq_pid[1], color=YELLOW)
        texto_proporcional = Tex("Termo Proporcional", color=YELLOW).scale(0.7)\
                            .next_to(rect_proporcional, UP)
        self.play(Create(rect_proporcional), Write(texto_proporcional))
        self.wait(1)
        self.play(FadeOut(rect_proporcional), FadeOut(texto_proporcional))
        self.wait(0.5)

        # Destacar o Termo Integral com retângulo e tópico
        rect_integral = SurroundingRectangle(eq_pid[3], color=GREEN)
        texto_integral = Tex("Termo Integral", color=GREEN).scale(0.7)\
                        .next_to(rect_integral, UP)
        self.play(Create(rect_integral), Write(texto_integral))
        self.wait(1)
        self.play(FadeOut(rect_integral), FadeOut(texto_integral))
        self.wait(0.5)

        # Destacar o Termo Derivativo com retângulo e tópico
        rect_derivativo = SurroundingRectangle(eq_pid[5], color=RED)
        texto_derivativo = Tex("Termo Derivativo", color=RED).scale(0.7)\
                        .next_to(rect_derivativo, UP)
        self.play(Create(rect_derivativo), Write(texto_derivativo))
        self.wait(1)
        self.play(FadeOut(rect_derivativo), FadeOut(texto_derivativo))
        self.wait(1)

        # Animação de saída
        self.play(
            FadeOut(titulo),
            FadeOut(texto_explicativo),
            FadeOut(eq_pid)
        )
        self.wait()

    def ConclusaoScene(self):
        # Mensagem final
        mensagem = Text(
            "Conclusão\n\nObrigado pela atenção!\nPerguntas?",
            font_size=36,
            line_spacing=1.5
        )
        self.play(FadeIn(mensagem, shift=UP))
        self.wait(3)

        # Finalizando
        self.play(FadeOut(mensagem))
        self.wait()

    def Intro_pt2(self):
        # 1) TÍTULO
        title = Text("Exemplo de Controle ON/OFF de Temperatura", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 2) CRIAÇÃO DOS EIXOS
        # Eixo X de 0 a 7 (tempo)
        # Eixo Y de 65 a 75 (temperatura)
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[10, 20, 2],
            x_length=7,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": True}
        )
        # Posiciona os eixos mais para baixo para dar espaço ao título
        axes.to_edge(DOWN, buff=1)

        # Rótulos dos eixos
        axes_labels = axes.get_axis_labels(x_label="Tempo (s)", y_label="Temperatura (°C)")
        self.play(Create(axes), Write(axes_labels))
        self.wait(1)

        # 3) DESENHO DA LINHA DE SETPOINT (16°C)
        setpoint_value = 16
        setpoint_line = Line(
            axes.coords_to_point(0, setpoint_value),  # Ponto inicial
            axes.coords_to_point(10, setpoint_value),  # Ponto final
            color=PURPLE
        )
        # Um pequeno rótulo para o setpoint
        setpoint_label = Text("Setpoint = 16°C", font_size=24, color=PURPLE)
        setpoint_label.next_to(setpoint_line, RIGHT, buff=0.3)

        self.play(Create(setpoint_line), FadeIn(setpoint_label))
        self.wait(1)

        # 4) CRIAÇÃO DA CURVA DE TEMPERATURA
        # Exemplo: Oscilando em torno de 70, período de 2 segundos
        def temperature_noisy(t):
            if t < 1.1:
                return 20 - t**2 - 2*t
            return 16 + 1 * np.sin((2 * np.pi / 2) * t)  # amplitude = 2, período = 2

        temp_graph = axes.plot(temperature_noisy, x_range=[0, 10], color=RED)
        self.play(Create(temp_graph))
        self.wait(1)

        # 5) CRIAÇÃO DOS BLOCOS "ON"/"OFF" ACIMA DO GRÁFICO
        # Definindo os intervalos (cada um com 1 unidade de largura no eixo X)
        # Aqui é só um exemplo: alternamos On e Off a cada 1 segundo.
        intervals = [
            (0, "On"),
            (1, "Off"),
            (2, "On"),
            (3, "Off"),
            (4, "On"),
            (5, "Off"),
            (6, "On"),
            (7, "Off"),
            (8, "On"),
            (9, "Off"),
        ]
        # Cada tupla: (início_do_intervalo, "On" ou "Off")
        # O retângulo cobrirá [início, início+1] no eixo X.

        # Vamos criar uma lista para armazenar os retângulos e textos
        rectangles = []
        labels = []

        for start_x, state in intervals:
            # Cria um retângulo de 1 unidade de largura e 0.8 de altura
            #axes.x_axis.unit_size
            rect = Rectangle(width=axes.x_axis.unit_size, height=0.8, stroke_color=WHITE)
            # Centraliza o retângulo em x = start_x + 0.5, e define um y fixo (por ex. 76)
            # Precisamos converter para coordenadas de cena com axes.coords_to_point
            center_x = start_x + 1.0
            center_y = 13  # um pouco acima de 75
            rect_center = axes.coords_to_point(center_x, center_y)
            rect.move_to(rect_center)

            # Define o texto ("On" ou "Off"), colorido de acordo
            color = BLUE if state == "On" else GREY_BROWN
            text_label = Text(state, color=color, font_size=24)
            text_label.move_to(rect_center)  # centralizado no retângulo

            rectangles.append(rect)
            labels.append(text_label)


        # 6) ANIMAÇÃO DOS RETÂNGULOS
        for rect, lbl in zip(rectangles, labels):
            self.play(Create(rect), FadeIn(lbl))
            self.wait(0.1)

        self.wait(2)

        # 7) ENCERRAMENTO
        # Podemos dar um FadeOut geral ou animar cada elemento.
        all_mobjects = [
            title, axes,axes_labels, # x_label, y_label,
            setpoint_line, setpoint_label,
            temp_graph
        ] + rectangles + labels
        self.play(*[FadeOut(mobj) for mobj in all_mobjects])
        self.wait(1)

    def Proporcional(self):
        # Título
        title = Text("Controle Proporcional (P)", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Definição dos tópicos
        topic_1 = "Tratando de um controle puramente\nproporcional, podemos reduzir para:"
        topic_2 = "A ação de controle é proporcional ao erro"
        topic_3 = "$u_b$ é um valor de bias, ou reset"
        topic_4 = "Geralmente, $u_b = (u_{max} + u_{min})/2$"
        
        # Primeiro tópico (bullet único)
        bullet_1 = BulletedList(topic_1).scale(0.8)
        bullet_1.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(bullet_1, shift=DOWN))
        self.wait(1)
        
        # Equação centralizada abaixo do primeiro tópico
        eq1 = MathTex(r"u(t) = K_p\,e(t) + u_b").scale(0.8)
        eq1.next_to(bullet_1, DOWN, buff=0.3)
        eq1.move_to(np.array([0, eq1.get_center()[1], 0]))  # centraliza horizontalmente
        self.play(FadeIn(eq1, shift=DOWN))
        self.wait(1)
        
        # Tópicos restantes (bullet points)
        bullet_rest = BulletedList(topic_2, topic_3, topic_4).scale(0.9)
        bullet_rest.next_to(eq1, DOWN, buff=0.3)
        for bullet in bullet_rest:
            self.play(FadeIn(bullet, shift=DOWN))
            self.wait(1)
        
        self.wait(2)
        
        # Encerramento: fade out de todos os elementos
        self.play(
            FadeOut(title),
            FadeOut(bullet_1),
            FadeOut(eq1),
            FadeOut(bullet_rest),
        )
        self.wait(1)
    
    def Ilust_prop(self):
        # Título principal do vídeo
        titulo_video = Text("Simulação de Malha Fechada com Controle Proporcional", font_size=36)
        titulo_video.to_edge(UP)
        self.play(Write(titulo_video))
        
        # Definir valores de K para teste
        K_values = [1, 2, 5]

        # Criação de uma legenda para os ganhos
        legend_item_1 = Text("K = 1", font_size=20, color=BLUE)
        legend_item_2 = Text("K = 2", font_size=20, color=GREEN)
        legend_item_3 = Text("K = 5", font_size=20, color=RED)
        legenda = VGroup(legend_item_1, legend_item_2, legend_item_3).arrange(DOWN, aligned_edge=LEFT)
        legenda.to_edge(RIGHT)
        self.play(Write(legenda))
        
        # Definir G(s) = 1 / (s+1)^3
        s = control.tf('s')
        G = 1/(s+1)**3

        # Tempo de simulação
        t_final = 20
        t = np.linspace(0, t_final, 1000)

        # Cria eixos para y(t)
        ax_y = Axes(
            x_range=[0, 20, 5],
            y_range=[-1, 2, 1],
            x_length=5,
            y_length=3,
            tips=False,
            axis_config={"include_numbers": True},
        )
        label_y = ax_y.get_axis_labels(x_label="t", y_label="y(t)")

        # Cria eixos para u(t)
        ax_u = Axes(
            x_range=[0, 20, 5],
            y_range=[-2, 3, 1],
            x_length=5,
            y_length=3,
            tips=False,
            axis_config={"include_numbers": True},
        )
        label_u = ax_u.get_axis_labels(x_label="t", y_label="u(t)")

        # Títulos dos gráficos
        titulo_grafico_y = Text("Saída do Processo y(t)", font_size=24)
        titulo_grafico_u = Text("Sinal de Controle u(t)", font_size=24)

        # Posiciona os títulos acima de cada eixo
        titulo_grafico_y.next_to(ax_y, UP*5)
        titulo_grafico_u.next_to(ax_u, UP*5)

        # Agrupa cada conjunto (título + eixos + rótulos)
        grupo_y = VGroup(titulo_grafico_y, ax_y, label_y)
        grupo_u = VGroup(titulo_grafico_u, ax_u, label_u)

        # Organiza os gráficos lado a lado e posiciona mais abaixo
        group_axes = VGroup(grupo_y, grupo_u).arrange(buff=1)
        group_axes.to_edge(DOWN)
        
        self.play(
            Create(ax_y), Create(ax_u),
            Create(label_y), Create(label_u),
            Write(titulo_grafico_y), Write(titulo_grafico_u)
        )

        # Cores para cada K
        colors = [BLUE, GREEN, RED]

        # Para cada valor de K, calcula a resposta ao degrau e plota as curvas
        curve_group = []
        for i, K in enumerate(K_values):
            # Malha fechada: K*G / (1 + K*G)
            sys_closed = control.feedback(K*G, 1)

            # Resposta ao degrau
            t_out, y_out = control.step_response(sys_closed, t)

            # Sinal de controle: u(t) = K * (r - y(t)), com r=1
            u_out = K * (1 - y_out)

            # Plota y(t)
            y_curve = ax_y.plot_line_graph(
                x_values=t_out,
                y_values=y_out,
                line_color=colors[i],
                add_vertex_dots=False
            )
            # Plota u(t)
            u_curve = ax_u.plot_line_graph(
                x_values=t_out,
                y_values=u_out,
                line_color=colors[i],
                add_vertex_dots=False
            )

            # Anima a criação das curvas
            curve_group.append(y_curve)
            curve_group.append(u_curve)
            self.play(Create(y_curve), Create(u_curve))

        self.wait(2)
        # Cria uma lista com todos os elementos que deseja desaparecer
        fadeout_elements = [titulo_video, legenda, group_axes] + curve_group

        # Anima o fadeout de todos os elementos em 2 segundos
        self.play(*[FadeOut(mob) for mob in fadeout_elements], run_time=2)
        # self.play(FadeOut(titulo_video, legenda, group_axes, grupo_y,
        #                   u_curve, y_curve, curve_group, label_y ))


    def Integral_pt1(self):
        # Título
        # Título
        title = Text("Controle Integral (I)", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Textos originais sem '\n'
        texto_1 = ("A maior função de uma ação integral é garantir que a saida do "
                   "processo corresponde com o setpoint no regime permanente")
        texto_2 = ("O controle proporcional, geralment, deixa algum erro "
                   "no regime permanente")
        texto_3 = ("Com a ação integral, esse erro que perdura no tempo vai aumentar "
                   "a ação de controle")

        # Define a largura máxima de cada linha (ajuste conforme necessidade)
        width = 25
        
        # Usa textwrap para quebrar cada texto em linhas de até 'width' caracteres
        wrapped_1 = "\n".join(textwrap.wrap(texto_1, width=width))
        wrapped_2 = "\n".join(textwrap.wrap(texto_2, width=width))
        wrapped_3 = "\n".join(textwrap.wrap(texto_3, width=width))
        
        # Tópicos (bullet points) com as linhas já quebradas automaticamente
        bullet_points = BulletedList(
            wrapped_1,
            wrapped_2,
            wrapped_3,
        ).scale(0.80)
        bullet_points.next_to(title, DOWN, buff=0.5)
        
        self.play(FadeIn(bullet_points, shift=DOWN))
        self.wait(2)
        
        # Encerramento
        self.play(
            FadeOut(title),
            FadeOut(bullet_points),
        )
        self.wait(1)


    def Integral_pt2(self):
        # Título
        title = Text("Controle Integral (I)", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Definição dos tópicos
        topic_1 = "Isolando a parte integral da equação temos:"
        topic_2 = "Com ela podemos provar que no regime permanente"
        topic_3 = "o sinal de controle sempre vai ser"
        topic_4 = " zero quando $e_0=0$"
        
        # Primeiro tópico (bullet único)
        bullet_1 = BulletedList(topic_1).scale(0.9)
        bullet_1.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(bullet_1, shift=DOWN))
        self.wait(1)
        
        # Equação centralizada abaixo do primeiro tópico
        eq1 = MathTex(r"u_0 = K\,(e_0 + \frac{e_0}{Ti}t)").scale(0.8)
        eq1.next_to(bullet_1, DOWN, buff=0.3)
        eq1.move_to(np.array([0, eq1.get_center()[1], 0]))  # centraliza horizontalmente
        self.play(FadeIn(eq1, shift=DOWN))
        self.wait(1)
        
        # Tópicos restantes (bullet points)
        bullet_rest = BulletedList(topic_2, topic_3, topic_4).scale(0.9)
        bullet_rest.next_to(eq1, DOWN, buff=0.3)
        for bullet in bullet_rest:
            self.play(FadeIn(bullet, shift=DOWN))
            self.wait(1)
        
        self.wait(2)
        
        # Encerramento: fade out de todos os elementos
        self.play(
            FadeOut(title),
            FadeOut(bullet_1),
            FadeOut(eq1),
            FadeOut(bullet_rest),
        )
        self.wait(1)

    def Derivativo_pt1(self):
        # Título
        title = Text("Controle Derivativativo (D)", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Textos originais sem '\n'
        texto_1 = ("A função da ação derivativa melhora a estabilidade de um sistema")
        texto_2 = ("Por causa da dinâmica do processo, vai demorar algum tempo até que"
                   " mudanças na variável controlada afeta a saída do processo")


        # Define a largura máxima de cada linha (ajuste conforme necessidade)
        width = 25

        # Usa textwrap para quebrar cada texto em linhas de até 'width' caracteres
        wrapped_1 = "\n".join(textwrap.wrap(texto_1, width=width))
        wrapped_2 = "\n".join(textwrap.wrap(texto_2, width=width))

        # Tópicos (bullet points) com as linhas já quebradas automaticamente
        bullet_points = BulletedList(
            wrapped_1,
            wrapped_2,
        ).scale(0.80)
        bullet_points.next_to(title, DOWN, buff=0.5)

        self.play(FadeIn(bullet_points, shift=DOWN))
        self.wait(2)

        # Encerramento
        self.play(
            FadeOut(title),
            FadeOut(bullet_points),
        )
        self.wait(1)

    def Derivativo_pt2(self):
         # Título
        title = Text("Controle Derivativativo (D)", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

            # Texto inicial (resumo em português)
        texto_1 = (
            "O controlador PD age como se fosse proporcional à previsão do erro "
            "futuro, feita por extrapolação da inclinação do erro atual. "
            "A forma básica do controlador PD é:"
        )

        width = 50  # Ajuste conforme a largura desejada
        wrapped_1 = "\n".join(textwrap.wrap(texto_1, width=width))

        # Exibição do texto como um bullet
        bullet_1 = BulletedList(wrapped_1).scale(0.6)
        bullet_1.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(bullet_1, shift=DOWN))
        self.wait(2)

        # Equação PD
        eq_pd = MathTex(r"u(t) = K\bigl(e(t) + T_d\,\frac{d e(t)}{dt}\bigr)").scale(0.8)
        eq_pd.next_to(bullet_1, DOWN, buff=0.3)
        # Centraliza horizontalmente
        eq_pd.move_to(np.array([0, eq_pd.get_center()[1], 0]))
        self.play(FadeIn(eq_pd, shift=DOWN))
        self.wait(2)

        # Texto sobre a expansão em série de Taylor
        # Resumo: A expansão de e(t + T_d) em série de Taylor gera e(t) + T_d * de(t)/dt,
        # permitindo prever o erro em um instante futuro T_d.

        texto_2 = (
            "A expansão em série de Taylor de $e(t + T_d)$ resulta em "
            "$e(t + T_d) \\approx e(t) + T_d\\,\\frac{d e(t)}{dt}$. "
            "Assim, o sinal de controle se torna proporcional a uma estimativa "
            "do erro em um instante $T_d$ à frente, obtida por extrapolação linear."
        )
        wrapped_2 = "\n".join(textwrap.wrap(texto_2, width=width))

        bullet_2 = BulletedList(wrapped_2).scale(0.6)
        bullet_2.next_to(eq_pd, DOWN, buff=0.5)
        self.play(FadeIn(bullet_2, shift=DOWN))
        self.wait(3)

        # Encerramento
        self.play(
            FadeOut(title),
            FadeOut(bullet_1),
            FadeOut(eq_pd),
            FadeOut(bullet_2),
        )
        self.wait(1)

    def PIDFeedbackDiagram(self):
        # 1) Nó de soma (para calcular e(t) = x(t) - y(t))
        summation = Circle(radius=0.2, color=WHITE).move_to(LEFT*4)
        sum_label = Text("∑", font_size=24).move_to(summation.get_center())
        
        # 2) Seta e rótulo da entrada x(t)
        x_label = MathTex("x(t)", font_size=30).next_to(summation, LEFT, buff=0.3)
        input_arrow = Arrow(
            start=x_label.get_left(),
            end=summation.get_left(),
            buff=0.1
        )
        
        # 3) Seta de saída do nó de soma para o controlador (erro e(t))
        pid_block = Rectangle(width=1.5, height=1, color=WHITE).move_to(LEFT*1.5)
        pid_text = Text("PID", font_size=24).move_to(pid_block.get_center())
        
        arrow_e = Arrow(
            start=summation.get_right(),
            end=pid_block.get_left(),
            buff=0.2
        )
        e_label = MathTex("e(t)", font_size=30).next_to(arrow_e, UP, buff=0.1)
        
        # 4) Seta de saída do controlador para a planta (u(t))
        plant_block = Rectangle(width=1.5, height=1, color=WHITE).move_to(RIGHT*1.5)
        plant_text = Text("Plant", font_size=24).move_to(plant_block.get_center())
        
        arrow_u = Arrow(
            start=pid_block.get_right(),
            end=plant_block.get_left(),
            buff=0.2
        )
        u_label = MathTex("u(t)", font_size=30).next_to(arrow_u, UP, buff=0.1)
        
        # 5) Seta de saída da planta (y(t)) para a direita
        output_arrow = Arrow(
            start=plant_block.get_right(),
            end=RIGHT*4,
            buff=0.2
        )
        y_label = MathTex("y(t)", font_size=30).next_to(output_arrow, UP, buff=0.1)
        
        # 6) Realimentação (feedback) da saída y(t) de volta ao nó de soma
        # Aqui usamos uma linha curva para ilustrar o retorno
        feedback_arrow = CurvedArrow(
            start_point=RIGHT*3.8 + DOWN*0.3,  # próximo ao final do output_arrow
            end_point=summation.get_bottom(),
            angle=-TAU/4,  # curvatura para cima
            color=WHITE
        )
        # Rótulo da realimentação (mesmo y(t))
        y_feedback_label = MathTex("y(t)", font_size=30).next_to(feedback_arrow, DOWN, buff=0.1)
        
        # 7) Animações de criação
        self.play(Create(summation), Write(sum_label))
        self.wait(0.5)
        
        self.play(Write(x_label), Create(input_arrow))
        self.wait(0.5)
        
        self.play(Create(arrow_e), Write(e_label))
        self.play(Create(pid_block), Write(pid_text))
        self.wait(0.5)
        
        self.play(Create(arrow_u), Write(u_label))
        self.play(Create(plant_block), Write(plant_text))
        self.wait(0.5)
        
        self.play(Create(output_arrow), Write(y_label))
        self.wait(0.5)
        
        self.play(Create(feedback_arrow), Write(y_feedback_label))
        self.wait(2)
        
        # 8) Encerramento
        self.play(
            *[FadeOut(mobj) for mobj in self.mobjects]
        )
        self.wait(1)

    def Ilust_int(self):
        # Título principal do vídeo
        titulo_video = Text("Simulação de Malha Fechada com Controlador PI", font_size=36)
        titulo_video.to_edge(UP)
        self.play(Write(titulo_video))

        # Definir valores de Ti (tempo integral) para teste
        # Ti = ∞ significa sem ação integral (só proporcional, K=1).
        Ti_values = [1, 2, 5, np.inf]

        # Criação de uma legenda para os valores de Ti
        # (cores diferentes para cada curva)
        colors = [BLUE, GREEN, RED, YELLOW]
        legend_texts = []
        for i, Ti in enumerate(Ti_values):
            if np.isinf(Ti):
                txt = "Tᵢ = ∞ (sem integral)"
            else:
                txt = f"Tᵢ = {Ti}"
            legend_texts.append(Text(txt, font_size=20, color=colors[i]))

        legenda = VGroup(*legend_texts).arrange(DOWN, aligned_edge=LEFT)
        legenda.to_edge(RIGHT)
        self.play(Write(legenda))

        # Definir G(s) = 1 / (s+1)^3
        s = control.tf('s')
        G = 1/(s+1)**3

        # Tempo de simulação
        t_final = 20
        t = np.linspace(0, t_final, 1000)

        # Cria eixos para y(t)
        ax_y = Axes(
            x_range=[0, 20, 5],
            y_range=[-1, 2, 1],
            x_length=5,
            y_length=3,
            tips=False,
            axis_config={"include_numbers": True},
        )
        label_y = ax_y.get_axis_labels(x_label="t", y_label="y(t)")

        # Cria eixos para u(t)
        ax_u = Axes(
            x_range=[0, 20, 5],
            y_range=[-2, 3, 1],
            x_length=5,
            y_length=3,
            tips=False,
            axis_config={"include_numbers": True},
        )
        label_u = ax_u.get_axis_labels(x_label="t", y_label="u(t)")

        # Títulos dos gráficos
        titulo_grafico_y = Text("Saída do Processo y(t)", font_size=24)
        titulo_grafico_u = Text("Sinal de Controle u(t)", font_size=24)

        # Posiciona os títulos acima de cada eixo
        titulo_grafico_y.next_to(ax_y, UP*7)
        titulo_grafico_u.next_to(ax_u, UP*7)

        # Agrupa cada conjunto (título + eixos + rótulos)
        grupo_y = VGroup(titulo_grafico_y, ax_y, label_y)
        grupo_u = VGroup(titulo_grafico_u, ax_u, label_u)

        # Organiza os gráficos lado a lado e posiciona mais abaixo
        group_axes = VGroup(grupo_y, grupo_u).arrange(buff=1)
        group_axes.to_edge(DOWN)

        self.play(
            Create(ax_y), Create(ax_u),
            Create(label_y), Create(label_u),
            Write(titulo_grafico_y), Write(titulo_grafico_u)
        )

        curve_group = []

        # Para cada valor de Ti, define o controlador PI e plota as curvas
        for i, Ti in enumerate(Ti_values):
            # Controlador PI: C(s) = K * (1 + 1/(Ti s)), aqui K=1.
            # Se Ti = ∞ => controlador é só proporcional = 1.
            if np.isinf(Ti):
                C = control.tf(1, 1)
            else:
                C = 1 + 1/(Ti*s)

            # Malha fechada: [C*G / (1 + C*G)]
            sys_closed = control.feedback(C*G, 1)

            # Resposta ao degrau (setpoint = 1)
            t_out, y_out = control.step_response(sys_closed, t)

            # Sinal de controle: u(t) = C(s) * (r - y(t)) em domínio do tempo
            # Uma forma simples: se Ti = ∞ => u(t) = 1 * (1 - y(t))
            # Caso contrário, precisamos converter C(s) para o domínio do tempo.
            # Podemos simular "u(t)" como a resposta do sistema fictício
            # U(s) = C(s)*(R(s)-Y(s)) => U(s) = C(s)*(1 - Y(s))
            # mas python-control facilita usando "forced_response".
            # Vamos montar a malha de "U(s) = C(s)*(1 - Y(s))" usando blocos.
            
            # O bloco do controlador C(s) e do "processo" 1 (apenas um fio)
            # é um pouco mais trabalhoso para simular. Uma abordagem simples:
            #   e(t) = r(t) - y(t)
            #   r(t) = 1 => R(s) = 1/s
            #   y(t) já temos. Precisamos do "forced_response" de C(s)*[r(t)-y(t)].
            
            # Precisamos de y(t) no domínio do tempo. Vamos usar a saída do sys_closed.
            # Uma forma prática: simulamos a saída do sistema "Gcl" e depois calculamos
            # e(t) = 1 - y(t). Então passamos e(t) como entrada de um sistema "C(s)".
            # Em python-control, definimos: "C_sis = control.tf2ss(C)" e
            # calculamos "u(t)" = forced_response(C_sis, T, e(t)).

            # 1) Monta um modelo de estado para C(s)
            C_sis = control.tf2ss(C)

            # 2) e(t) = 1 - y_out
            e_t = 1 - y_out

            # 3) forced_response(C_sis, T, U=e_t) => (T, u_out, xout)
            # _, u_out, _ = control.forced_response(C_sis, t_out, e_t)
            t_u, u_out = control.forced_response(C_sis, t_out, e_t)


            # Plotar y(t)
            y_curve = ax_y.plot_line_graph(
                x_values=t_out,
                y_values=y_out,
                line_color=colors[i],
                add_vertex_dots=False
            )
            # Plotar u(t)
            u_curve = ax_u.plot_line_graph(
                x_values=t_out,
                y_values=u_out,
                line_color=colors[i],
                add_vertex_dots=False
            )
            # Armazena as curvas para o fadeout
            curve_group.append(y_curve)
            curve_group.append(u_curve)

            # Anima a criação das curvas
            self.play(Create(y_curve), Create(u_curve))

        self.wait(2)
        fadeout_elements = [titulo_video, legenda, group_axes] + curve_group
        self.play(*[FadeOut(mob) for mob in fadeout_elements], run_time=2)

    def Ilust_der(self):
                # Título principal do vídeo
        titulo_video = Text("Simulação de Malha Fechada com Controlador PID", font_size=36)
        titulo_video.to_edge(UP)
        self.play(Write(titulo_video))

        # Parâmetros do controlador e do processo
        K = 3       # Ganho proporcional
        Ti = 2      # Tempo integral
        Td_values = [0.7, 1.7, 4.5]  # Vários valores de Td

        # Parâmetros do filtro derivativo e do pólo extra
        alpha = 0.01   # Filtro no derivativo
        epsilon = 1e-4  # Pólo extra para garantir que o sistema seja estritamente próprio

        # Legenda dos valores de Td (cores diferentes para cada curva)
        colors = [BLUE, GREEN, RED]
        legend_texts = []
        for i, Td in enumerate(Td_values):
            txt = f"Td = {Td}"
            legend_texts.append(Text(txt, font_size=20, color=colors[i]))
        legenda = VGroup(*legend_texts).arrange(DOWN, aligned_edge=LEFT)
        legenda.to_edge(RIGHT)
        self.play(Write(legenda))

        # Definir G(s) = 1/(s+1)^3
        s = control.tf('s')
        G = 1/(s+1)**3

        # Tempo de simulação
        t_final = 20
        t = np.linspace(0, t_final, 1000)

        # Criação dos eixos para y(t) e u(t)
        ax_y = Axes(
            x_range=[0, 20, 5],
            y_range=[-1, 2, 1],
            x_length=5,
            y_length=3,
            tips=False,
            axis_config={"include_numbers": True},
        )
        label_y = ax_y.get_axis_labels(x_label="t", y_label="y(t)")
        
        ax_u = Axes(
            x_range=[0, 20, 5],
            y_range=[-2, 3, 1],
            x_length=5,
            y_length=3,
            tips=False,
            axis_config={"include_numbers": True},
        )
        label_u = ax_u.get_axis_labels(x_label="t", y_label="u(t)")

        # Títulos dos gráficos
        titulo_grafico_y = Text("Saída do Processo y(t)", font_size=24)
        titulo_grafico_u = Text("Sinal de Controle u(t)", font_size=24)
        titulo_grafico_y.next_to(ax_y, UP*5)
        titulo_grafico_u.next_to(ax_u, UP*5)
        
        grupo_y = VGroup(titulo_grafico_y, ax_y, label_y)
        grupo_u = VGroup(titulo_grafico_u, ax_u, label_u)
        group_axes = VGroup(grupo_y, grupo_u).arrange(buff=1)
        group_axes.to_edge(DOWN)
        
        self.play(
            Create(ax_y), Create(ax_u),
            Create(label_y), Create(label_u),
            Write(titulo_grafico_y), Write(titulo_grafico_u)
        )

        curve_group = []

        # Loop sobre cada valor de Td
        for i, Td in enumerate(Td_values):
            # Controlador PID real com filtro derivativo e pólo extra:
            # C(s) = K * [ 1 + 1/(Ti*s) + (Td*s)/(1+alpha*Td*s) ] / (1+epsilon*s)
            C = K * (1 + 1/(Ti*s) + (Td*s)/(1 + alpha*Td*s)) / (1 + epsilon*s)
            
            # Malha fechada: [C*G / (1 + C*G)]
            sys_closed = control.feedback(C*G, 1)
            
            # Resposta ao degrau (setpoint = 1)
            t_out, y_out = control.step_response(sys_closed, t)
            
            # Para obter o sinal de controle u(t), simulamos a resposta de C(s) ao erro: e(t)=1-y(t)
            C_sis = control.tf2ss(C)
            e_t = 1 - y_out
            t_u, u_out = control.forced_response(C_sis, t_out, e_t)
            
            # Plotar as curvas
            y_curve = ax_y.plot_line_graph(
                x_values=t_out, y_values=y_out,
                line_color=colors[i], add_vertex_dots=False
            )
            # Se for a curva vermelha (índice 2, Td=4.5), aplica o clipping
            if i == 2:
                clip_rect = Rectangle(
                    width=ax_y.x_length,
                    height=ax_y.y_length,
                    stroke_width=0,
                    fill_opacity=0
                )
                # Posiciona o retângulo no centro dos eixos de y(t)
                clip_rect.move_to(ax_y.get_center())
                # Aplica o clipping à curva
                y_curve.set_clip(clip_rect)
            
            u_curve = ax_u.plot_line_graph(
                x_values=t_out, y_values=u_out,
                line_color=colors[i], add_vertex_dots=False
            )
            
            self.play(Create(y_curve), Create(u_curve))
            # Armazena as curvas para o fadeout
            curve_group.append(y_curve)
            curve_group.append(u_curve)

        self.wait(2)
        fadeout_elements = [titulo_video, legenda, group_axes] + curve_group
        self.play(*[FadeOut(mob) for mob in fadeout_elements], run_time=2)


    def AulaSintonizacaoPID(self):
        # Título da Aula
        title = Text("Projeto e Sintonização do Controlador PID", font_size=36)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # # Introdução ao PID
        # pid_intro = Tex(r"\textbf{PID:} Proporcional, Integral, Derivativo", font_size=32)
        # self.play(Write(pid_intro))
        # self.wait(3)
        # self.play(FadeOut(pid_intro))

        # Seção 1: Cancelamento de Polo-Zero
        pz_title = Text("Técnica de Cancelamento de Polo-Zero", font_size=32, color=BLUE)
        pz_desc = Tex(
            r"""
            \begin{itemize}
                \item \textbf{Objetivo:} Simplificar a dinâmica, eliminando polos ou zeros indesejados.
                \item Requer um modelo matemático preciso do sistema.
                \item Cancelamento imperfeito pode reduzir a robustez.
            \end{itemize}
            """, font_size=28
        )
        pz_group = VGroup(pz_title, pz_desc).arrange(DOWN, buff=0.5)
        self.play(Write(pz_group))
        self.wait(5)
        self.play(FadeOut(pz_group))

        # Seção 2: Alocação de Polos
        ap_title = Text("Técnica de Alocação de Polos", font_size=32, color=GREEN)
        ap_desc = Tex(
            r"""
            \begin{itemize}
                \item \textbf{Objetivo:} Posicionar os polos do sistema em locais específicos.
                \item Baseada em realimentação de estado.
                \item Permite controlar parâmetros como tempo de subida, amortecimento e overshoot.
            \end{itemize}
            """, font_size=28
        )
        ap_group = VGroup(ap_title, ap_desc).arrange(DOWN, buff=0.5)
        self.play(Write(ap_group))
        self.wait(5)
        self.play(FadeOut(ap_group))

        # Seção 3: Método de Ziegler-Nichols
        zn_title = Text("Método de Ziegler-Nichols", font_size=32, color=RED)
        zn_desc = Tex(
            r"""
            \begin{itemize}
                \item Ajusta inicialmente apenas o termo proporcional até ocorrer oscilações contínuas.
                \item Determina o ganho crítico ($K_{cr}$) e o período de oscilação ($P_{cr}$).
                \item Usa fórmulas empíricas para calcular os ganhos $K_p$, $K_i$ e $K_d$.
                \item Pode resultar em overshoot se não for refinado.
            \end{itemize}
            """, font_size=28
        )
        zn_group = VGroup(zn_title, zn_desc).arrange(DOWN, buff=0.5)
        self.play(Write(zn_group))
        self.wait(6)
        self.play(FadeOut(zn_group))

        # Conclusão
        conclusion = Text("A escolha da técnica depende do sistema e\ndos requisitos de desempenho.", font_size=28)
        self.play(Write(conclusion))
        self.wait(4)
        self.play(FadeOut(conclusion))


    def AlocacaoDePolos(self):
        # 1. Título
        title = Text("Técnica de Alocação de Polos", font_size=36, color=YELLOW)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # 2. Introdução
        intro_text = Text(
            "A alocação de polos define os polos desejados do sistema em malha fechada\n"
            "para satisfazer requisitos de desempenho (ζ e ωₙ).",
            font_size=26
        )
        self.play(Write(intro_text))
        self.wait(3)
        self.play(FadeOut(intro_text))

        # 3. Equação de segunda ordem: Y(s)/R(s)
        eq_second_order = MathTex(
            r"\frac{Y(s)}{R(s)} = \frac{\omega_n^2}{s^2 + 2\,\zeta\,\omega_n\,s + \omega_n^2}",
            font_size=36
        )
        eq_second_order.to_edge(UP)
        self.play(Write(eq_second_order))
        self.wait(3)

        # 4. Explicação texto
        text_second_order = Text(
            "Modelo de segunda ordem:\n"
            "Polos em -ζωₙ ± jωₙ√(1-ζ²)",
            font_size=26
        )
        text_second_order.next_to(eq_second_order, DOWN, buff=0.8)
        self.play(FadeIn(text_second_order))
        self.wait(3)

        # 5. Fórmulas para Kp e Ki
        self.play(FadeOut(text_second_order))
        eq_kp = MathTex(
            r"K_p = \frac{2\,\zeta\,\omega_n \;-\; a}{b}",
            font_size=36
        )
        eq_ki = MathTex(
            r"K_i = \frac{\omega_n^2}{b}",
            font_size=36
        )
        group_gains = VGroup(eq_kp, eq_ki).arrange(DOWN, buff=1).next_to(eq_second_order, DOWN, buff=1.5)
        self.play(Write(eq_kp))
        self.wait(1)
        self.play(Write(eq_ki))
        self.wait(2)

        # 6. Explicação final
        conclusion_text = Text(
            "Escolhendo ζ e ωₙ conforme as especificações (tempo de assentamento,\n"
            "percentual de sobressinal, etc.), podemos encontrar Kp e Ki.",
            font_size=26
        )
        conclusion_text.next_to(group_gains, DOWN, buff=1)
        self.play(FadeIn(conclusion_text))
        self.wait(4)

        # Fim
        self.play(*[FadeOut(mob) for mob in self.mobjects])



    def ExemploAlocacaoPolos(self):
        # Título principal
        title = Tex("Exemplo Prático de Alocação de Polos", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 1. Definição do Sistema
        sec1_title = Tex("1. Definição do Sistema", font_size=28)
        sys_eq = MathTex(r"G(s)=\frac{2}{s}").scale(0.8)
        ctrl_eq = MathTex(r"C(s)=K_p+\frac{K_i}{s}").scale(0.8)
        open_loop = MathTex(
            r"G_{OL}(s)=G(s)C(s)=\frac{2}{s}\Bigl(K_p+\frac{K_i}{s}\Bigr)=\frac{2K_p}{s}+\frac{2K_i}{s^2}"
        ).scale(0.8)
        section1 = VGroup(sec1_title, sys_eq, ctrl_eq, open_loop).arrange(DOWN, aligned_edge=LEFT)

        # 2. Polos Desejados (Critério de Desempenho)
        sec2_title = Tex("2. Polos Desejados (Critério de Desempenho)", font_size=28)
        polos = Tex(
            r"Polos desejados: $s=-\zeta\,\omega_n\pm j\,\omega_n\sqrt{1-\zeta^2}$ \\[6pt]"
            r"Equação característica: $s^2+2\zeta\,\omega_n\,s+\omega_n^2=0$"
        ).scale(0.8)
        section2 = VGroup(sec2_title, polos).arrange(DOWN, aligned_edge=LEFT)

        # 3. Equação Característica em Malha Fechada
        sec3_title = Tex("3. Equação Característica em Malha Fechada", font_size=28)
        eq_line1 = MathTex(
            r"1+G_{OL}(s)=0 \quad\Rightarrow\quad 1+\left(\frac{2K_p}{s}+\frac{2K_i}{s^2}\right)=0"
        ).scale(0.8)
        eq_line2 = Tex("Multiplicando por $s^2$:").scale(0.8)
        eq_line3 = MathTex(r"s^2+2K_p\,s+2K_i=0").scale(0.8)
        section3 = VGroup(sec3_title, eq_line1, eq_line2, eq_line3).arrange(DOWN, aligned_edge=LEFT)

        # 4. Igualando ao Polinômio Desejado
        sec4_title = Tex("4. Igualando ao Polinômio Desejado", font_size=28)
        comparacao = Tex(
            r"$s^2+2K_p\,s+2K_i = s^2+2\zeta\,\omega_n\,s+\omega_n^2$ \\[8pt]"
            r"$\Rightarrow \quad 2K_p=2\zeta\,\omega_n \quad\Rightarrow\quad K_p=\zeta\,\omega_n$ \\[8pt]"
            r"$\text{ e } \quad 2K_i=\omega_n^2 \quad\Rightarrow\quad K_i=\frac{\omega_n^2}{2}$"
        ).scale(0.8)
        section4 = VGroup(sec4_title, comparacao).arrange(DOWN, aligned_edge=LEFT)

        # 5. Escolha Numérica de ζ e ωₙ
        sec5_title = Tex(r"5. Escolha Numérica de $\zeta$ e $\omega_n$", font_size=28)
        numerico = Tex(
            r"Exemplo: $\zeta=0.7$, $\omega_n=5\,\text{rad/s}$ \\[8pt]"
            r"$K_p=0.7\times5=3.5$ \\[8pt]"
            r"$K_i=\frac{5^2}{2}=12.5$"
        ).scale(0.8)
        section5 = VGroup(sec5_title, numerico).arrange(DOWN, aligned_edge=LEFT)

        # 6. Verificando o Resultado
        sec6_title = Tex("6. Verificando o Resultado", font_size=28)
        verificacao = Tex(
            r"Controlador PI: $C(s)=3.5+\frac{12.5}{s}$ \\[8pt]"
            r"Equação característica: $s^2+7s+25=0$ \\[8pt]"
            r"Polos: $s=-3.5\pm j\,3.30$"
        ).scale(0.8)
        section6 = VGroup(sec6_title, verificacao).arrange(DOWN, aligned_edge=LEFT)

        # Conclusões
        concl_title = Tex("Conclusões", font_size=28)
        conclusoes = Tex(
            r"1. Alocação de polos por comparação de polinômios. \\[6pt]"
            r"2. Ganhos $K_p$ e $K_i$ obtidos pela igualdade de coeficientes. \\[6pt]"
            r"3. Método válido para sistemas simples; sistemas complexos podem requerer abordagens adicionais. \\[6pt]"
            r"4. Verificar robustez em sistemas reais."
        ).scale(0.8)
        section_concl = VGroup(concl_title, conclusoes).arrange(DOWN, aligned_edge=LEFT)

        # Agrupar todas as seções e organizar verticalmente
        all_sections = VGroup(
            section1, section2, section3, section4, section5, section6, section_concl
        )
        all_sections.arrange(DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)
        all_sections.next_to(title, DOWN, buff=1)

        # Animação de escrita de todas as seções
        self.play(Write(all_sections))
        self.wait(2)
        self.play(
            FadeOut(all_sections),
            FadeOut(title),
        )
