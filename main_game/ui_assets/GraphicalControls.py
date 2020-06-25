import pygame
from Control import *


#
# UI Assets
# By Tommy Hu
#
# Inherited from Control class
class Label(Control):

    def __init__(self):
        Control.__init__(self)
        self.text = ""


# Basic ProgressBar class
class ProgressBar(Control):

    def __init__(self, maximum=100.0, current=0.0):
        Control.__init__(self)
        self.maximum = maximum
        self.current = current
        self.back_color = pygame.Color("DARKGRAY")
        self.fore_color = pygame.Color("DARKGREEN")
        self.font_color = pygame.Color("BLACK")
        self.font = pygame.font.SysFont("arial", 50)
        self.finish_event_list = []
        self.caption = ""
        self.display_caption = False

    def refresh(self):
        if self.Enabled:
            Control.refresh(self)

            if self.current > self.maximum:
                self.current = self.maximum

            if self.current == self.maximum:
                for func in self.finish_event_list:
                    func()

            draw.rect(self.surface, self.back_color, self.Rect)
            client_rect = Rect(self.Rect.x + 5, self.Rect.y + 5, self.Rect.width - 10, self.Rect.height - 10)
            unit = client_rect.width / float(self.maximum)
            actual_width = self.current * unit

            actual_rect = Rect(client_rect.x, client_rect.y, actual_width, client_rect.height)
            draw.rect(self.surface, self.fore_color, actual_rect)
            if self.display_caption:
                text_surface = self.font.render(self.caption + str(self.current) + "/" + str(self.maximum), True,
                                                self.font_color)
                t_rect = text_surface.get_rect()
                text_rect = Rect(client_rect.x + client_rect.width / 2 - (t_rect.width / 2),
                                 client_rect.y + client_rect.height / 2 - (t_rect.height / 2),
                                 t_rect.width, t_rect.height)
                self.surface.blit(text_surface, text_rect)

    def subscribe_finish_event(self, func):
        self.finish_event_list.append(func)

    def unsubscribe_finish_event(self, func):
        self.finish_event_list.remove(func)


# Basic Button class
class Button(Control):
    def __init__(self, caption="Click me!"):
        Control.__init__(self)
        self.on_click_list = []
        self.on_mouse_over_list = []
        self.on_mouse_leave_list = []
        self.rim_color = pygame.Color("GRAY")
        self.normal_color = pygame.Color("LIGHTGRAY")
        self.pressed_color = pygame.Color("GRAY")
        self.rim_thickness = 3
        self.caption = caption
        self.font_color = pygame.Color("BLACK")
        self.font = pygame.font.SysFont("arial", 20)
        self.pressed = False

        self.last_mouse_over = False
        self.rect_inflation_amount = 20

    def refresh(self):
        if self.Enabled:
            Control.refresh(self)
            self.check_click()

    def redraw(self, pressed=False):
        pygame.draw.rect(self.surface, self.rim_color, self.Rect)
        inner_rect = pygame.Rect(self.Rect.x + self.rim_thickness, self.Rect.y + self.rim_thickness,
                                 self.Rect.width - 2 * self.rim_thickness,
                                 self.Rect.height - 2 * self.rim_thickness)
        if pressed:
            pygame.draw.rect(self.surface, self.pressed_color, inner_rect)
        else:
            pygame.draw.rect(self.surface, self.normal_color, inner_rect)
        text_surface = self.font.render(self.caption, True, self.font_color)
        t_rect = text_surface.get_rect()
        text_rect = pygame.Rect(inner_rect.x + inner_rect.width / 2 - t_rect.width / 2,
                                inner_rect.y + inner_rect.height / 2 - t_rect.height / 2, t_rect.width, t_rect.height)
        self.surface.blit(text_surface, text_rect)

    def check_click(self):
        pos = pygame.mouse.get_pos()
        if self.Rect.collidepoint(pos):
            if not self.last_mouse_over:
                self.last_mouse_over = True
                self.Rect = self.Rect.inflate(self.rect_inflation_amount, self.rect_inflation_amount)
                for func in self.on_mouse_over_list:
                    func()
        else:
            if self.last_mouse_over:
                self.last_mouse_over = False
                self.Rect = self.Rect.inflate(-self.rect_inflation_amount, -self.rect_inflation_amount)
                for func in self.on_mouse_leave_list:
                    func()

        if pygame.mouse.get_pressed()[0]:  # left mouse button pressed down
            if self.Rect.collidepoint(pos):
                self.pressed = True
                self.redraw(True)
            else:
                self.redraw(False)
                self.pressed = False
        else:
            self.redraw(False)
            if self.pressed:
                # last frame, the mouse was pressed!
                self.pressed = False
                # fire the on click events subscribed!
                for func in self.on_click_list:
                    func()

    def subscribe_on_click(self, func):
        self.on_click_list.append(func)

    def unsubscribe_on_click(self, func):
        self.on_click_list.remove(func)

    def subscribe_on_mouse_over(self, func):
        self.on_mouse_over_list.append(func)

    def unsubscribe_on_mouse_over(self, func):
        self.on_mouse_over_list.remove(func)

    def subscribe_on_mouse_leave(self, func):
        self.on_mouse_leave_list.append(func)

    def unsubscribe_on_mouse_leave(self, func):
        self.on_mouse_leave_list.remove(func)


# Basic InputField class
class InputField(Control):

    def __init__(self, text=""):
        Control.__init__(self)
        self.back_color = pygame.Color("WHITESMOKE")
        self.rim_color = pygame.Color("DARKGRAY")
        self.pressed_rim_color = pygame.Color("DODGERBLUE")
        self.rim_thickness = 2
        self.font_color = pygame.Color("BLACK")
        self.font = pygame.font.SysFont("arial", 20)
        self.cursor_color = pygame.Color("Black")
        self.text = text
        self._editing = False
        self.pressed = False
        self.default_width = 200
        self.default_height = 30

    def set_rect(self, rect):
        Control.set_rect(self, rect)
        self.default_width = rect.width
        self.default_height = rect.height

    def get_rect(self):
        return Control.get_rect(self)

    def refresh(self, events=None):
        if self.Enabled:
            self.check_click()
            if self._editing:
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            self.text = self.text[:-1]
                        elif event.key == pygame.K_RETURN:
                            self.text += "\n"
                        else:
                            cap = event.mod & pygame.KMOD_CAPS
                            shift = event.mod & pygame.KMOD_SHIFT
                            if (cap or shift) and not (cap and shift):
                                self.text += event.unicode.upper()
                                print "Shift!"
                            else:
                                self.text += event.unicode

            Control.refresh(self)
            if self._editing:
                pygame.draw.rect(self.surface, self.pressed_rim_color, self.Rect)
            else:
                pygame.draw.rect(self.surface, self.rim_color, self.Rect)

            inner_rect = Rect(self.Rect.x + self.rim_thickness, self.Rect.y + self.rim_thickness,
                              self.Rect.width - 2 * self.rim_thickness, self.Rect.height - 2 * self.rim_thickness)
            pygame.draw.rect(self.surface, self.back_color, inner_rect)
            text_surface = self.font.render(self.text, True, self.font_color)
            t_rect = text_surface.get_rect()
            text_rect = Rect(inner_rect.x + inner_rect.width / 2 - t_rect.width / 2,
                             inner_rect.y + inner_rect.height / 2 - t_rect.height / 2, t_rect.width, t_rect.height)
            self.Rect.width = max(self.default_width, t_rect.width + 2 * self.rim_thickness)
            self.Rect.height = max(self.default_height, t_rect.height + 2 * self.rim_thickness)
            self.surface.blit(text_surface, text_rect)

    def check_click(self):
        if pygame.mouse.get_pressed()[0]:  # left mouse button pressed down
            pos = pygame.mouse.get_pos()
            if self.Rect.collidepoint(pos):
                self.pressed = True
            else:
                self.pressed = False
                self._editing = False
        else:
            if self.pressed:
                # last frame, the mouse was pressed!
                self.pressed = False
                # basically, the text field was clicked!
                self._editing = True

    Rect = property(get_rect, set_rect)
