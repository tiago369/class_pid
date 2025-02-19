from manim import *
import numpy as np

class PID(Scene):
    def construct(self):
        # self.IntroScene()
        # self.ObjetivosScene()
        # self.Intro_pt1()
        # self.Intro_pt2()
        # self.Intro_pt3()
        # self.DesenvolvimentoScene()
        # self.PIDFeedbackDiagram()
        # self.Proporcional()
        # self.PropIntegral()
        # self.PID()
        # self.ConclusaoScene()
    
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
            "Introdução ao Controle PID",
            "Fundamentos Teóricos do Controlador PID",
            "Projeto e Sintonização do Controlador PID",
            "Exemplos Práticos e Implementação",
            font_size=40
        ).next_to(titulo, DOWN, buff=1.0)

        # Animação de cada item
        for item in objetivos:
            self.play(FadeIn(item, shift=RIGHT))
            self.wait(0.5)

        self.wait(2)
        self.play(FadeOut(titulo), FadeOut(objetivos))
        self.wait()

    def Intro_pt1(self):
        # Título da cena
        title = Text("Introdução ao Controle PID: Controle de Temperatura\ncom Ar Condicionado", font_size=36)
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
        title = Text("Introdução ao Controle PID: Controle de Temperatura\ncom Ar Condicionado", font_size=36)
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
        
        # Tópicos (bullet points)
        bullet_points = BulletedList(
            "Controle proporcional = ganho K aplicado ao erro",
            "Exemplo: Speed controller (Seção 4.1)",
            "Planta de segunda ordem (motor com indutância não desprezível)",
            "Sistema Tipo : K alto reduz erro, mas pode afetar estabilidade",
        ).scale(0.5)
        bullet_points.next_to(title, DOWN, buff=0.5)
        
        self.play(FadeIn(bullet_points, shift=DOWN))
        self.wait(2)
        
        # Equações principais
        eq1 = MathTex(r"U(s) = D(s)\,e(s)").scale(0.8)
        eq2 = MathTex(r"G(s) = \frac{A}{s^2 + a_1 s + a_2}").scale(0.8)
        eq3 = MathTex(
            r"1 + K_p \, G(s) = 0 \quad\Longrightarrow\quad",
            r"s^2 + a_1 s + a_2 + K_p\,A = 0"
        ).scale(0.8)
        
        # Posicionamento das equações
        eq1.next_to(bullet_points, DOWN, buff=1)
        eq2.next_to(eq1, DOWN, buff=0.5)
        eq3.next_to(eq2, DOWN, buff=0.5)
        
        # Animações para as equações
        self.play(Write(eq1))
        self.wait(1)
        self.play(Write(eq2))
        self.wait(1)
        self.play(Write(eq3))
        self.wait(2)
        
        # Encerramento
        self.play(
            FadeOut(title),
            FadeOut(bullet_points),
            FadeOut(eq1),
            FadeOut(eq2),
            FadeOut(eq3)
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

