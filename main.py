from math import ceil, floor, isfinite, log10

from kivy.app import App
from kivy.core.text import Label as CoreLabel
from kivy.graphics import Color, Line, Rectangle, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex


NAVY = get_color_from_hex("#172554")
BLUE = get_color_from_hex("#2563EB")
TEAL = get_color_from_hex("#0F9D8A")
INK = get_color_from_hex("#172033")
MUTED = get_color_from_hex("#667085")
GRID = get_color_from_hex("#E8EDF5")
PAPER = get_color_from_hex("#F5F7FB")
WHITE = get_color_from_hex("#FFFFFF")


class GraphWidget(Widget):
    """Desenha eixos, grade e a curva sem depender de bibliotecas externas."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mode = "linear"
        self.coefficients = (1.0, 0.0, 0.0)
        self.x_min, self.x_max = -10.0, 10.0
        self.bind(pos=self.redraw, size=self.redraw)
        self.redraw()

    def set_function(self, mode, coefficients, x_min, x_max):
        self.mode = mode
        self.coefficients = coefficients
        self.x_min, self.x_max = x_min, x_max
        self.redraw()

    @staticmethod
    def _text(text, x, y, font_size=sp(10), color=MUTED):
        label = CoreLabel(text=text, font_size=font_size, color=color)
        label.refresh()
        texture = label.texture
        Rectangle(texture=texture, pos=(x, y), size=texture.size)

    @staticmethod
    def _tick_step(span):
        raw = span / 8.0
        magnitude = 10 ** floor(log10(raw))
        fraction = raw / magnitude
        nice = 1 if fraction <= 1 else 2 if fraction <= 2 else 5 if fraction <= 5 else 10
        return nice * magnitude

    @staticmethod
    def _format_tick(value):
        if abs(value) < 1e-9:
            value = 0
        return f"{value:g}"

    def redraw(self, *_):
        self.canvas.clear()
        with self.canvas:
            Color(*WHITE)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(16)])
            if self.width < dp(100) or self.height < dp(100):
                return

            left = self.x + dp(48)
            right = self.right - dp(14)
            bottom = self.y + dp(34)
            top = self.top - dp(16)
            plot_w, plot_h = right - left, top - bottom
            x0, x1 = self.x_min, self.x_max
            a, b, c = self.coefficients

            def fn(x):
                return a * x + b if self.mode == "linear" else a * x * x + b * x + c

            sample_count = 301
            ys = [fn(x0 + (x1 - x0) * i / (sample_count - 1)) for i in range(sample_count)]
            ys = [y for y in ys if isfinite(y)]
            if not ys:
                return
            y_low, y_high = min(ys), max(ys)
            if abs(y_high - y_low) < 1e-9:
                pad = max(1.0, abs(y_high) * 0.12)
            else:
                pad = (y_high - y_low) * 0.12
            y0, y1 = y_low - pad, y_high + pad
            if y0 == y1:
                y0, y1 = -1, 1

            def px(x):
                return left + (x - x0) / (x1 - x0) * plot_w

            def py(y):
                return bottom + (y - y0) / (y1 - y0) * plot_h

            sx, sy = self._tick_step(x1 - x0), self._tick_step(y1 - y0)
            Color(*GRID)
            tick = ceil(x0 / sx) * sx
            while tick <= x1 + sx * 1e-8:
                x = px(tick)
                Line(points=[x, bottom, x, top], width=1)
                self._text(self._format_tick(tick), x - dp(9), self.y + dp(8), sp(9))
                tick += sx
            tick = ceil(y0 / sy) * sy
            while tick <= y1 + sy * 1e-8:
                y = py(tick)
                Line(points=[left, y, right, y], width=1)
                if bottom - dp(4) <= y <= top - dp(8):
                    self._text(self._format_tick(tick), self.x + dp(4), y - dp(6), sp(9))
                tick += sy

            Color(*MUTED)
            if x0 <= 0 <= x1:
                Line(points=[px(0), bottom, px(0), top], width=1.25)
            if y0 <= 0 <= y1:
                Line(points=[left, py(0), right, py(0)], width=1.25)

            points = []
            for i in range(sample_count):
                x = x0 + (x1 - x0) * i / (sample_count - 1)
                y = fn(x)
                if isfinite(y):
                    points.extend((px(x), py(max(y0, min(y1, y)))))
            Color(*(BLUE if self.mode == "linear" else TEAL))
            if len(points) >= 4:
                Line(points=points, width=dp(2.8), cap="round", joint="round")

            Color(*MUTED)
            self._text("x", right - dp(7), bottom - dp(3), sp(10))
            self._text("y", left - dp(5), top - dp(2), sp(10))


class FunctionGraphApp(App):
    title = "Gráfico de Funções"

    def build(self):
        self.mode = "linear"
        self.root_layout = BoxLayout(orientation="vertical", padding=[dp(14), dp(10)], spacing=dp(10))
        self.root_layout.bind(size=self._set_background, pos=self._set_background)
        with self.root_layout.canvas.before:
            Color(*PAPER)
            self.background = Rectangle(pos=self.root_layout.pos, size=self.root_layout.size)

        scroll = __import__("kivy.uix.scrollview", fromlist=["ScrollView"]).ScrollView(
            do_scroll_x=False, bar_width=dp(3), scroll_type=["bars", "content"]
        )
        content = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(12), padding=[0, 0, 0, dp(12)])
        content.bind(minimum_height=content.setter("height"))
        scroll.add_widget(content)
        self.root_layout.add_widget(scroll)

        header = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(70), spacing=dp(3))
        header.add_widget(Label(text="Gráfico de Funções", font_size=sp(24), bold=True, color=NAVY,
                                halign="left", valign="middle", size_hint_y=None, height=dp(38),
                                text_size=(None, None)))
        header.add_widget(Label(text="Explore funções do 1º e 2º grau", font_size=sp(14), color=MUTED,
                                halign="left", valign="middle", size_hint_y=None, height=dp(24)))
        content.add_widget(header)

        card = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(77), padding=dp(10), spacing=dp(7))
        self._add_card_background(card)
        card.add_widget(self._caption("TIPO DE FUNÇÃO"))
        mode_row = BoxLayout(spacing=dp(8))
        self.linear_button = self._mode_button("1º grau · y = ax + b", "linear")
        self.quadratic_button = self._mode_button("2º grau · y = ax² + bx + c", "quadratic")
        mode_row.add_widget(self.linear_button)
        mode_row.add_widget(self.quadratic_button)
        card.add_widget(mode_row)
        content.add_widget(card)

        self.coefficient_card = BoxLayout(orientation="vertical", size_hint_y=None, padding=dp(12), spacing=dp(8))
        self.coefficient_grid = GridLayout(cols=3, size_hint_y=None, height=dp(62), spacing=dp(8))
        self.coefficient_card.add_widget(self._caption("COEFICIENTES"))
        self.coefficient_card.add_widget(self.coefficient_grid)
        content.add_widget(self.coefficient_card)
        self.coefficient_card.bind(pos=self._card_canvas, size=self._card_canvas)
        self._card_canvas(self.coefficient_card)
        self._make_coefficient_inputs()

        range_card = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(92), padding=dp(12), spacing=dp(7))
        range_card.add_widget(self._caption("INTERVALO DO EIXO X"))
        range_row = BoxLayout(spacing=dp(8))
        self.x_min_input = self._input("De", "-10")
        self.x_max_input = self._input("Até", "10")
        range_row.add_widget(self._field("De", self.x_min_input))
        range_row.add_widget(self._field("Até", self.x_max_input))
        range_card.add_widget(range_row)
        self._add_card_background(range_card)
        content.add_widget(range_card)

        draw = Button(text="Atualizar gráfico", size_hint_y=None, height=dp(48), background_normal="",
                      background_color=BLUE, color=WHITE, font_size=sp(16), bold=True)
        draw.bind(on_release=self.plot)
        content.add_widget(draw)

        graph_card = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(330), padding=dp(12), spacing=dp(6))
        graph_card.add_widget(self._caption("VISUALIZAÇÃO"))
        self.graph = GraphWidget()
        graph_card.add_widget(self.graph)
        self._add_card_background(graph_card)
        content.add_widget(graph_card)

        self.result = Label(text="Insira os coeficientes e toque em Atualizar gráfico.", color=INK,
                            font_size=sp(14), halign="left", valign="middle", size_hint_y=None,
                            height=dp(55), text_size=(None, None))
        content.add_widget(self.result)
        self.status = Label(text="Use ponto ou vírgula para casas decimais.", color=MUTED, font_size=sp(12),
                            size_hint_y=None, height=dp(24), halign="left")
        content.add_widget(self.status)
        self.select_mode("linear")
        self.plot()
        return self.root_layout

    def _set_background(self, *_):
        self.background.pos = self.root_layout.pos
        self.background.size = self.root_layout.size

    @staticmethod
    def _caption(text):
        return Label(text=text, color=MUTED, font_size=sp(10), bold=True, halign="left",
                     valign="middle", size_hint_y=None, height=dp(17))

    def _add_card_background(self, widget):
        with widget.canvas.before:
            Color(*WHITE)
            widget._card_rect = RoundedRectangle(pos=widget.pos, size=widget.size, radius=[dp(14)])
        widget.bind(pos=lambda w, v: setattr(w._card_rect, "pos", v),
                    size=lambda w, v: setattr(w._card_rect, "size", v))

    def _card_canvas(self, widget, *_):
        if not hasattr(widget, "_card_rect"):
            with widget.canvas.before:
                Color(*WHITE)
                widget._card_rect = RoundedRectangle(pos=widget.pos, size=widget.size, radius=[dp(14)])
        else:
            widget._card_rect.pos = widget.pos
            widget._card_rect.size = widget.size

    def _mode_button(self, text, mode):
        button = Button(text=text, background_normal="", background_color=BLUE if mode == "linear" else PAPER,
                        color=WHITE if mode == "linear" else INK, font_size=sp(12), bold=True)
        button.bind(on_release=lambda *_: self.select_mode(mode))
        return button

    def select_mode(self, mode):
        self.mode = mode
        self.linear_button.background_color = BLUE if mode == "linear" else PAPER
        self.linear_button.color = WHITE if mode == "linear" else INK
        self.quadratic_button.background_color = BLUE if mode == "quadratic" else PAPER
        self.quadratic_button.color = WHITE if mode == "quadratic" else INK
        self._make_coefficient_inputs()
        self.plot()

    @staticmethod
    def _input(hint, value):
        return TextInput(text=value, hint_text=hint, multiline=False, input_filter="float",
                         background_normal="", background_active="", background_color=PAPER,
                         foreground_color=INK, cursor_color=BLUE, font_size=sp(16), padding=[dp(9), dp(10)])

    def _field(self, title, field):
        box = BoxLayout(orientation="vertical", spacing=dp(3))
        box.add_widget(Label(text=title, color=MUTED, font_size=sp(11), halign="left",
                             size_hint_y=None, height=dp(16)))
        box.add_widget(field)
        return box

    def _make_coefficient_inputs(self):
        if not hasattr(self, "coefficient_grid"):
            return
        self.coefficient_grid.clear_widgets()
        self.inputs = {}
        names = [("a", "1"), ("b", "0")] if self.mode == "linear" else [("a", "1"), ("b", "0"), ("c", "0")]
        self.coefficient_grid.cols = len(names)
        for name, value in names:
            field = self._input(name, value)
            self.inputs[name] = field
            self.coefficient_grid.add_widget(self._field(name, field))
        self.coefficient_grid.height = dp(62)

    @staticmethod
    def _number(field, name):
        raw = field.text.strip().replace(",", ".")
        if not raw:
            raise ValueError(f"Preencha o coeficiente {name}.")
        value = float(raw)
        if not isfinite(value):
            raise ValueError(f"O valor de {name} precisa ser finito.")
        return value

    def plot(self, *_):
        try:
            a = self._number(self.inputs["a"], "a")
            b = self._number(self.inputs["b"], "b")
            c = self._number(self.inputs["c"], "c") if self.mode == "quadratic" else 0.0
            x_min = self._number(self.x_min_input, "início do intervalo")
            x_max = self._number(self.x_max_input, "fim do intervalo")
            if x_min >= x_max:
                raise ValueError("O início do intervalo deve ser menor que o fim.")
            if abs(x_min) > 1e6 or abs(x_max) > 1e6:
                raise ValueError("Use um intervalo entre −1.000.000 e 1.000.000.")
            if self.mode == "quadratic" and a == 0:
                raise ValueError("Na função do 2º grau, o coeficiente a não pode ser zero.")

            self.graph.set_function(self.mode, (a, b, c), x_min, x_max)
            if self.mode == "linear":
                equation = f"f(x) = {a:g}x {'+' if b >= 0 else '−'} {abs(b):g}"
                detail = f"Inclinação: {a:g}   ·   Intercepto em y: {b:g}"
            else:
                equation = f"f(x) = {a:g}x² {'+' if b >= 0 else '−'} {abs(b):g}x {'+' if c >= 0 else '−'} {abs(c):g}"
                delta = b * b - 4 * a * c
                xv = -b / (2 * a)
                yv = a * xv * xv + b * xv + c
                roots = "duas raízes reais" if delta > 0 else "uma raiz real" if delta == 0 else "sem raízes reais"
                detail = f"Vértice: ({xv:.3g}, {yv:.3g})   ·   Δ = {delta:.3g} ({roots})"
            self.result.text = equation + "\n" + detail
            self.status.text = "Gráfico atualizado."
            self.status.color = TEAL
        except (ValueError, OverflowError) as exc:
            self.status.text = str(exc)
            self.status.color = get_color_from_hex("#C0392B")


if __name__ == "__main__":
    FunctionGraphApp().run()
