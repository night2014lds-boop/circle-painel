import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import cairo as Cairo
import math
import os

class RevolverPanel(Gtk.Window):
    def __init__(self):
        super().__init__(title="Painel Revolver")
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)
        self.set_app_paintable(True)
        self.set_keep_above(True)
        
        self.home_dir = os.path.expanduser("~")
        
        # Variáveis de customização
        self.esconder_inteligente = False
        self.painel_visivel = True
        self.cor_r, self.cor_g, self.cor_b = 0.1, 0.1, 0.1
        self.alfa = 0.6
        self.caminho_imagem = ""

        # Configurações de física e posição
        self.raio = 140
        self.centro_x = 200
        self.centro_y = 200
        self.resize(400, 400)
        
        self.pos_x_visivel = Gdk.Screen.width() - 200
        self.pos_x_escondido = Gdk.Screen.width() - 15
        self.pos_x_atual = self.pos_x_visivel
        self.pos_y = 300
        self.move(self.pos_x_atual, self.pos_y)

        self.animacao_id = 0
        self.pos_x_alvo = self.pos_x_visivel

        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual:
            self.set_visual(visual)

        # LISTA UNIVERSAL (Apenas apps que todo usuário XFCE possui)
        self.apps = [
            ("Apps Finder", "xfce4-appfinder", "edit-find"),
            ("Terminal", "xfce4-terminal", "utilities-terminal"),
            ("Web Browser", "x-www-browser", "browser"),
            ("Files", "thunar", "system-file-manager"),
            ("Settings", "xfce4-settings-manager", "preferences-system"),
            ("Text Editor", "mousepad", "text-editor")
        ]
        self.angulo_atual = 0.0

        self.fixed = Gtk.Fixed()
        self.add(self.fixed)

        self.botoes = []
        for nome, comando, icone_nome in self.apps:
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            try:
                img = Gtk.Image.new_from_icon_name(icone_nome, Gtk.IconSize.LARGE_TOOLBAR)
                box.pack_start(img, True, True, 0)
            except:
                pass
            lbl = Gtk.Label(label=nome)
            box.pack_start(lbl, True, True, 0)
            
            btn = Gtk.Button()
            btn.add(box)
            btn.connect("clicked", self.executar_app, comando)
            self.fixed.put(btn, 0, 0)
            self.botoes.append(btn)

        self.connect("draw", self.draw_circle)
        self.add_events(Gdk.EventMask.SCROLL_MASK | Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.ENTER_NOTIFY_MASK)
        self.connect("scroll-event", self.ao_girar_mouse)
        self.connect("button-press-event", self.ao_clicar_mouse)
        self.connect("enter-notify-event", self.mouse_entrou_na_beirada)

        self.atualizar_posicao_apps()
        self.show_all()

    def draw_circle(self, widget, cr):
        cr.set_source_rgba(0, 0, 0, 0)
        cr.set_operator(Cairo.Operator.CLEAR)
        cr.paint()
        cr.set_operator(Cairo.Operator.OVER)
        
        if self.caminho_imagem and os.path.exists(self.caminho_imagem):
            try:
                cr.save()
                cr.arc(self.centro_x, self.centro_y, 200, 0, 2 * math.pi)
                cr.clip()
                surface = Cairo.ImageSurface.create_from_png(self.caminho_imagem)
                cr.scale(400 / surface.get_width(), 400 / surface.get_height())
                cr.set_source_surface(surface, 0, 0)
                cr.paint_with_alpha(self.alfa)
                cr.restore()
                return
            except:
                pass
        
        cr.set_source_rgba(self.cor_r, self.cor_g, self.cor_b, self.alfa)
        cr.arc(self.centro_x, self.centro_y, 200, 0, 2 * math.pi)
        cr.fill()

    def atualizar_posicao_apps(self):
        num_apps = len(self.apps)
        for i, btn in enumerate(self.botoes):
            fatia = (2 * math.pi) / num_apps
            angulo_app = self.angulo_atual + (i * fatia)
            x = self.centro_x + int(self.raio * math.cos(angulo_app)) - 45
            y = self.centro_y + int(self.raio * math.sin(angulo_app)) - 25
            self.fixed.move(btn, x, y)

    def ao_girar_mouse(self, widget, event):
        if event.direction == Gdk.ScrollDirection.UP:
            self.angulo_atual -= 0.25
        elif event.direction == Gdk.ScrollDirection.DOWN:
            self.angulo_atual += 0.25
        self.atualizar_posicao_apps()
        return True

    def ao_clicar_mouse(self, widget, event):
        if event.button == 3:
            self.criar_menu_contexto(event)
            return True
        elif event.button == 1 and self.esconder_inteligente and self.painel_visivel:
            self.recolher_painel()
            return True
        return False

    def iniciar_animacao(self, x_alvo):
        self.pos_x_alvo = x_alvo
        if self.animacao_id == 0:
            self.animacao_id = GLib.timeout_add(16, self.passo_animacao)

    def passo_animacao(self):
        distancia = self.pos_x_alvo - self.pos_x_atual
        if abs(distancia) < 2:
            self.pos_x_atual = self.pos_x_alvo
            self.move(self.pos_x_atual, self.pos_y)
            self.animacao_id = 0
            return False
        
        self.pos_x_atual += int(distancia * 0.25)
        self.move(self.pos_x_atual, self.pos_y)
        return True

    def mouse_entrou_na_beirada(self, widget, event):
        if self.esconder_inteligente and not self.painel_visivel:
            self.painel_visivel = True
            self.iniciar_animacao(self.pos_x_visivel)

    def recolher_painel(self):
        if self.esconder_inteligente:
            self.painel_visivel = False
            self.iniciar_animacao(self.pos_x_escondido)

    def criar_menu_contexto(self, event):
        menu = Gtk.Menu()

        txt_esconder = "Desativar Ocultação" if self.esconder_inteligente else "Ativar Ocultação Inteligente"
        item_esconder = Gtk.MenuItem(label=txt_esconder)
        item_esconder.connect("activate", self.menu_alternar_esconder)
        menu.append(item_esconder)

        item_transp = Gtk.MenuItem(label="Ajustar Transparência")
        sub_transp = Gtk.Menu()
        niveis = [("10%", 0.1), ("20%", 0.2), ("30%", 0.3), ("40%", 0.4), ("50%", 0.5), 
                  ("60%", 0.6), ("70%", 0.7), ("80%", 0.8), ("90%", 0.9), ("100% (Opaco)", 1.0)]
        for rotulo, valor in niveis:
            item_nv = Gtk.MenuItem(label=rotulo)
            item_nv.connect("activate", self.menu_definir_transparencia, valor)
            sub_transp.append(item_nv)
        item_transp.set_submenu(sub_transp)
        menu.append(item_transp)

        item_cores = Gtk.MenuItem(label="Mudar Cor do Fundo")
        sub_cores = Gtk.Menu()
        cores = [("Escuro", 0.1, 0.1, 0.1), ("Vermelho Neon", 0.8, 0.1, 0.1), ("Azul Cyber", 0.1, 0.5, 0.8), ("Verde Terminal", 0.1, 0.7, 0.2)]
        for nome_cor, r, g, b in cores:
            item_cor = Gtk.MenuItem(label=nome_cor)
            item_cor.connect("activate", self.menu_definir_cor, r, g, b)
            sub_cores.append(item_cor)
        item_cores.set_submenu(sub_cores)
        menu.append(item_cores)

        item_img = Gtk.MenuItem(label="Aplicar Imagem HTM.png")
        item_img.connect("activate", self.menu_aplicar_imagem)
        menu.append(item_img)

        item_sair = Gtk.MenuItem(label="Fechar Lançador")
        item_sair.connect("activate", lambda w: Gtk.main_quit())
        menu.append(item_sair)

        menu.show_all()
        menu.popup_at_pointer(event)

    def menu_alternar_esconder(self, widget):
        self.esconder_inteligente = not self.esconder_inteligente
        if not self.esconder_inteligente:
            self.painel_visivel = True
            self.iniciar_animacao(self.pos_x_visivel)
        else:
            self.recolher_painel()

    def menu_definir_transparencia(self, widget, valor):
        self.alfa = valor
        self.queue_draw()

    def menu_definir_cor(self, widget, r, g, b):
        self.caminho_imagem = ""
        self.cor_r, self.cor_g, self.cor_b = r, g, b
        self.queue_draw()

    def menu_aplicar_imagem(self, widget):
        self.caminho_imagem = f"{self.home_dir}/Imagens/HTM.png"
        self.queue_draw()

    def executar_app(self, botao, comando):
        os.system(f"{comando} &")
        self.recolher_painel()

if __name__ == "__main__":
    win = RevolverPanel()
    Gtk.main()
