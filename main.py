#!/usr/bin/python3
import sys
import tkinter
import pygame
from pygame.constants import K_LCTRL, MOUSEBUTTONUP, K_e, K_o, K_s
import tkinter as tk
from tkinter import filedialog
from colors import *
import random
import wave_gen
import sfz_gen
import math
import time

def get_canvas_mouse_pos():
  mx,my = pygame.mouse.get_pos()
  mx/=2
  my/=2
  return mx, my

def in_rect(rect):
  x,y,w,h = rect
  mx,my = get_canvas_mouse_pos()
  if mx >= x and mx < x+w and my >= y and my < y+h:
    return True
  return False

class GUIElement():
  def __init__(self,rect) -> None:
      self.rect     = rect
      self.selected = False
  def draw(self):
    pass
  def edit(self):
    pass
class WaveEditor(GUIElement):
  def __init__(self, rect) -> None:
      super().__init__(rect)
      self.wave_width  = (128,64,32,16,8,4)[2]
      self.wave_height = (64,32,16,8,4,2)[2]
      self.wave_data = [0]*self.wave_width
      self._none_txt = font.render("(none)",True,COLORS[3])
      self._noise_txt = font.render("(white noise)",True,COLORS[3])
  def draw(self):
      x,y,w,h=self.rect
      pw=w/self.wave_width
      ph=h/self.wave_height
      pygame.draw.rect(canvas,COLORS[1],self.rect)
      if self.wave_data == [0]*self.wave_width:
        canvas.blit(self._none_txt,(x+50,y+10))

      if self.wave_data == [15]*self.wave_width:
        canvas.blit(self._noise_txt,(x+28,y+10))
      for i,sample in enumerate(self.wave_data):
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
      self.wave_data[wx]=wy
  def preset(self,preset):
    presets = [
      [15]*32,
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,15,15,15,15,15,15,15],
      [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0],
      [0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13,14,14,15,15],
      [15,15,14,14,13,13,12,12,11,11,10,10,9,9,8,8,7,7,6,6,5,5,4,4,3,3,2,2,1,1,0,0],
    ]
    self.wave_data=presets[preset]
class Label(GUIElement):
  def __init__(self, rect,text,color) -> None:
      super().__init__(rect)
      self.rendered_text = font.render(text,True,COLORS[color])
  def draw(self):
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

pygame.init()

canvas_width  = 144
canvas_height = 160

screen = pygame.display.set_mode((canvas_width*2,canvas_height*2))
canvas = pygame.Surface((canvas_width,canvas_height))
pygame.display.set_caption("BitSFZ")

exit = False

FILE = "live.sfz"

font = pygame.font.Font("fonts/monogram-extended.ttf",16)
gui = {}
layer_gui = []
for i in range(4):
  lgui = {}
  lgui["wave_editor"] = WaveEditor((8,16,128,64))
  lgui["wave_preset"] = Label((2,80,144,16),"Noi 50% 25% Tri Saw Was",3)
  lgui["ampeg_label"] = Label((0,90,0,0),".Amplitude",4)
  lgui["ampeg_delay"] = NumberEditor((0,100,24,16),0)
  lgui["ampeg_attack"] = NumberEditor((24,100,24,16),50)
  lgui["ampeg_hold"] = NumberEditor((48,100,24,16),0)
  lgui["ampeg_decay"] = NumberEditor((48+24,100,24,16),50)
  lgui["ampeg_sustain"] = NumberEditor((48+48,100,24,16),90)
  lgui["ampeg_release"] = NumberEditor((48+48+24,100,24,16),50)
  lgui["ampeg_desc"]=Label((4,110,0,0),"Del Atk Hol Dec Sus Rel",2)
  lgui["pitchlfo_label"] = Label((0,120,0,0),".Vibrato",4)
  lgui["pitchlfo_delay"]=NumberEditor((0,130),0)
  lgui["pitchlfo_fade"]=NumberEditor((24,130),0)
  lgui["pitchlfo_depth"]=NumberEditor((48,130),0)
  lgui["pitchlfo_freq"]=NumberEditor((72,130),0,max_value=20)
  lgui["other_label"] = Label((90,120,0,0),".Other",4)
  lgui["tune"]=NumberEditor((96,130),50)
  lgui["pan"]=NumberEditor((120,130),50)
  lgui["pitchlfo_desc"]=Label((4,140,0,0),"Del Fad Dep Frq Tun Pan",2)
  layer_gui.append(lgui)

gui["wave_label"] = Label((0,0,0,0),f".Wave({FILE})",4)
gui["layer"] = RadioButton((106,4),["A","B","C","D"],0)

editor_selected = None
exit = False

root = tk.Tk()
root.withdraw()

def export(filename,directory):
  wave_gen.generate_tables(filename,directory,lgui["wave_editor"].wave_data,lgui["wave_editor"].wave_height,layer)
  sfz_gen.generate_file(filename,directory,layer_gui)

while not exit:
  layer = gui["layer"].value
  lgui = layer_gui[layer]
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      exit=True
    elif event.type == pygame.MOUSEBUTTONDOWN:
      for control in gui:
        if in_rect(gui[control].rect):
          gui[control].selected = True
      for control in lgui:
        if in_rect(lgui[control].rect):
          lgui[control].selected = True
    elif event.type == pygame.MOUSEBUTTONUP:
      for control in gui:
        if gui[control].selected:
          gui[control].selected = False
      for control in lgui:
        if lgui[control].selected:
          lgui[control].selected = False
          if control == "wave_preset":
            mx,my = get_canvas_mouse_pos()
            lgui["wave_editor"].preset(int(mx/24))
            
          export("live.sfz","out")
    elif event.type == pygame.KEYDOWN:
      pressed = pygame.key.get_pressed()
      if pressed[pygame.K_LCTRL]:  
        if event.key==K_e:
          types = [('SFZ File', '.sfz')]
          path=filedialog.asksaveasfilename(filetypes = types, defaultextension = ".sfz")
          if path != ():
            split = path.split("/")
            filename=split[-1]
            directory=path[:-len(filename)]
            export(filename,directory)

  # Drawing
  canvas.fill(COLORS[0])
  for control in gui:
    gui[control].draw()
    if gui[control].selected:
      gui[control].edit()
  for control in layer_gui[gui["layer"].value]:
    layer_gui[gui["layer"].value][control].draw()
    if layer_gui[gui["layer"].value][control].selected:
      layer_gui[gui["layer"].value][control].edit()

  scaled = pygame.transform.scale(canvas, (canvas_width*2,canvas_height*2))
  screen.blit(scaled,(0,0))
  pygame.display.flip()

pygame.display.quit()
pygame.quit()
