import pygame
from colors import *
import time
pygame.init()

canvas_width  = 144
canvas_height = 168
canvas_scale  = 2

font = pygame.font.Font("fonts/monogram-extended.ttf",16)
canvas = pygame.Surface((canvas_width,canvas_height))

def get_canvas_mouse_pos():
  mx,my = pygame.mouse.get_pos()
  mx/=canvas_scale
  my/=canvas_scale
  return mx, my

def in_rect(rect):
  if len(rect)==2:
      return False
  x,y,w,h = rect
  mx,my = get_canvas_mouse_pos()
  if mx >= x and mx < x+w and my >= y and my < y+h:
    return True
  return False

class GUIElement():
  def __init__(self,rect) -> None:
      self.rect     = rect
      self.selected = False
      self.value = None
  def draw(self):
    pass
  def edit(self):
    pass
  def select(self,sel):
      self.selected = sel
class WaveEditor(GUIElement):
  def __init__(self, rect) -> None:
      super().__init__(rect)
      self.wave_width  = (128,64,32,16,8,4)[2]
      self.wave_height = (64,32,16,8,4,2)[2]
      self.value = [0]*self.wave_width
      self._none_txt = font.render("(none)",True,COLORS[3])
      self._noise_txt = font.render("(white noise)",True,COLORS[3])
  def draw(self):
      x,y,w,h=self.rect
      pw=w/self.wave_width
      ph=h/self.wave_height
      pygame.draw.rect(canvas,COLORS[1],self.rect)
      if self.value == [0]*self.wave_width:
        canvas.blit(self._none_txt,(x+50,y+10))

      if self.value == [15]*self.wave_width:
        canvas.blit(self._noise_txt,(x+28,y+10))
      for i,sample in enumerate(self.value):
        sh=sample*ph
        pygame.draw.rect(canvas,COLORS[5],(x+i*w/self.wave_width,y+h-sh-ph,pw,ph))
  def edit(self):
    mx,my = get_canvas_mouse_pos()
    if pygame.mouse.get_pressed()[0]:
      wx = int((mx-self.rect[0])/self.rect[2]*self.wave_width)
      wy = self.wave_height-1-int((my-self.rect[1])/self.rect[3]*self.wave_height)
      if wx < 0: 
        wx=0
      if wx>=self.wave_width:
        wx=self.wave_width-1
      if wy < 0: 
        wy=0
      if wy>=self.wave_height:
        wy=self.wave_height-1
      self.value[wx]=wy
  def preset(self,preset):
    presets = [
      [0]*32,
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,15,15,15,15,15,15,15],
      [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0],
      [0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13,14,14,15,15],
      [15,15,14,14,13,13,12,12,11,11,10,10,9,9,8,8,7,7,6,6,5,5,4,4,3,3,2,2,1,1,0,0],
    ]
    self.value=presets[preset]
class Label(GUIElement):
  def __init__(self, rect,text,color) -> None:
      super().__init__(rect)
      self.text  = text
      self.color = color
      self._render_text()
      self._last_text = text
      self._last_color = color
  def _render_text(self):
      self.rendered_text = font.render(self.text,True,COLORS[self.color])
  def draw(self):
      if self._last_text != self.text or self._last_color != self.color:
          self._render_text()
          self._last_text = self.text
          self._last_color = self.color
      canvas.blit(self.rendered_text,(self.rect[0],self.rect[1]))
class NumberEditor(GUIElement):
  def __init__(self, rect,value,min_value=0,max_value=99) -> None:
      super().__init__((rect[0],rect[1],24,16))
      self.value = value
      self.min_value = min_value
      self.max_value = max_value
      self.rendered_arrows = font.render("←  →",True,COLORS[5])
      self._draw_value()

      self.edit_timer = 0
  def _draw_value(self):
    extra = ""
    if self.value < 10:
      extra="0"
    self.rendered_text = font.render(f'{extra}{str(self.value)}',True,COLORS[3])
  def draw(self):
      canvas.blit(self.rendered_arrows,(self.rect[0],self.rect[1]))
      canvas.blit(self.rendered_text,(self.rect[0]+6,self.rect[1]))
  def edit(self):
    if time.time() > self.edit_timer:
      mx,my = get_canvas_mouse_pos()

      if mx > self.rect[0]+self.rect[2]/2:
        self.value+=1
      else:
        self.value-=1
      if self.value < self.min_value:
        self.value = self.min_value
      if self.value > self.max_value:
        self.value = self.max_value
      self._draw_value()
      pressed = pygame.key.get_pressed()
      if pressed[pygame.K_LCTRL]:
        self.edit_timer = time.time() + 0.002
      elif pressed[pygame.K_LSHIFT]:
        self.edit_timer = time.time() + 0.1
      else:
        self.edit_timer = time.time() + 0.02
class RadioButton(GUIElement):
  def __init__(self, rect, options, selected=0) -> None:
      self.width = len(options[0])
      super().__init__((rect[0],rect[1],8*len(options)*self.width,12))
      self.value = selected
      self.options = options
      self.rendered_text = []
      for option in options:
        self.rendered_text.append(font.render(option,True,COLORS[3]))
  def draw(self):
      pygame.draw.rect(canvas,COLORS[1],(self.rect[0]+self.value*8*self.width-1,self.rect[1]+1,7*self.width,11))
      for i,option in enumerate(self.options):
        canvas.blit(self.rendered_text[i],(self.rect[0]+i*8*self.width,self.rect[1]))
  def edit(self):
    mx,_ = get_canvas_mouse_pos()
    sx = int((mx-self.rect[0])/8)
    if sx < 0:
      sx = 0
    if sx >= len(self.options):
      sx = len(self.options)-1
    self.value = sx
class Button(Label):
    def __init__(self, rect, text, color,sel_color,function,args=None) -> None:
        super().__init__(rect, text, color)
        self.function = function
        self.args = args
        self._desel_color = color
        self._sel_color = sel_color
    def select(self, sel):
        super().select(sel)
        if sel:
            self.color = self._sel_color
        else:
            self.color = self._desel_color
        if not sel and in_rect(self.rect):
            if self.args is not None:
                self.function(self.args)
            else:
                self.function()