#!/usr/bin/python3
import pygame
from pygame.constants import K_LCTRL, MOUSEBUTTONUP, K_e, K_o, K_s
import tkinter as tk
from tkinter import Button, filedialog
import ast
import os

from ui import *
import wave_gen
import sfz_gen
from colors import *

#============================
# I/O Functions
#============================
current_file = None
current_path = None

def export(filename=None,directory=None):
  global current_file
  global current_path

  if filename is None or directory is None:
    filename = current_file
    directory = current_path
  else:
    current_file = filename
    current_path = directory

  if current_file is not None and current_path is not None:
    wave_gen.generate_tables(filename,directory,lgui["wave_editor"].value,lgui["wave_editor"].wave_height,layer)
    sfz_gen.generate_file(filename,directory,layer_gui)   

def load(path):
  global current_file
  global current_path
  if path is not None and os.path.isfile(path):
    current_file = path.split("/")[-1]
    current_path = "/".join(path.split("/")[:-1])
    with open(path) as f:
      raw = f.readlines()[1][2:]
      for item in raw.strip().split(";"):
        if item != "":
          layer,name,value = item.strip().split(":")
          layer_gui[int(layer)][name].value = ast.literal_eval(value)

def save_dialog():
  types = [('SFZ File', '.sfz')]
  path=filedialog.asksaveasfilename(filetypes = types, defaultextension = ".sfz")
  if path != ():
    split = path.split("/")
    filename=split[-1]
    directory=path[:-len(filename)]
    export(filename,directory)

def load_dialog():
  types = [('SFZ File', '.sfz')]
  path=filedialog.askopenfilename(filetypes=types)
  load(path)

#============================
# Defining all UI Elements
#============================
screen = pygame.display.set_mode((canvas_width*canvas_scale,canvas_height*canvas_scale))
pygame.display.set_caption("BitSFZ")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

EDITOR_X,EDITOR_Y = 0,8
gui = {}
layer_gui = []
for i in range(4):
  lgui = {}
  lgui["wave_label"] = Label((0,0+EDITOR_Y),".Wave",4)
  lgui["wave_editor"] = WaveEditor((8,16+EDITOR_Y,128,64))
  lgui["noise_button"] = Button((2,80+EDITOR_Y,18,12),"Nil",3,4,lgui["wave_editor"].preset,0)
  lgui["50%_button"] = Button((2+24,80+EDITOR_Y,18,12),"50%",3,4,lgui["wave_editor"].preset,1)
  lgui["25%_button"] = Button((2+48,80+EDITOR_Y,18,12),"25%",3,4,lgui["wave_editor"].preset,2)
  lgui["triangle_button"] = Button((2+72,80+EDITOR_Y,18,12),"Tri",3,4,lgui["wave_editor"].preset,3)
  lgui["saw_button"] = Button((2+96,80+EDITOR_Y,18,12),"Saw",3,4,lgui["wave_editor"].preset,4)
  lgui["was_button"] = Button((2+120,80+EDITOR_Y,18,12),"Was",3,4,lgui["wave_editor"].preset,5)
  lgui["ampeg_label"] = Label((0,90+EDITOR_Y,0,0),".Amplitude",4)
  lgui["ampeg_delay"] = NumberEditor((0,100+EDITOR_Y,24,16),0)
  lgui["ampeg_attack"] = NumberEditor((24,100+EDITOR_Y,24,16),8)
  lgui["ampeg_hold"] = NumberEditor((48,100+EDITOR_Y,24,16),0)
  lgui["ampeg_decay"] = NumberEditor((48+24,100+EDITOR_Y,24,16),8)
  lgui["ampeg_sustain"] = NumberEditor((48+48,100+EDITOR_Y,24,16),80)
  lgui["ampeg_release"] = NumberEditor((48+48+24,100+EDITOR_Y,24,16),8)
  lgui["ampeg_desc"]=Label((4,110+EDITOR_Y),"Del Atk Hol Dec Sus Rel",2)
  lgui["pitchlfo_label"] = Label((0,120+EDITOR_Y),".Vibrato",4)
  lgui["pitchlfo_delay"]=NumberEditor((0,130+EDITOR_Y),0)
  lgui["pitchlfo_fade"]=NumberEditor((24,130+EDITOR_Y),0)
  lgui["pitchlfo_depth"]=NumberEditor((48,130+EDITOR_Y),0)
  lgui["pitchlfo_freq"]=NumberEditor((72,130+EDITOR_Y),0,max_value=20)
  lgui["other_label"] = Label((90,120+EDITOR_Y),".Other",4)
  lgui["tune"]=NumberEditor((96,130+EDITOR_Y),50)
  lgui["pan"]=NumberEditor((120,130+EDITOR_Y),50)
  lgui["pitchlfo_desc"]=Label((4,140+EDITOR_Y,0,0),"Del Fad Dep Frq Tun Pan",2)
  layer_gui.append(lgui)

gui["layer"] = RadioButton((106,4+EDITOR_Y),["A","B","C","D"],0)
gui["selected_file"] = Label((2,-3),str(current_file),4)
gui["save_button"] = Button((120,-2,24,12),"SAVE",4,5,save_dialog)
gui["load_button"] = Button((90,-2,24,12),"LOAD",4,5,load_dialog)


editor_selected = None
exit = False

root = tk.Tk()
root.withdraw()
  
#============================
# Main Loop
#============================
exit = False
while not exit:
  layer = gui["layer"].value
  lgui = layer_gui[layer]
  #============================
  # Process Input
  #============================
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      exit=True
    elif event.type == pygame.MOUSEBUTTONDOWN:
      for control in gui:
        if in_rect(gui[control].rect):
          gui[control].select(True)
      for control in lgui:
        if in_rect(lgui[control].rect):
          lgui[control].select(True)
    elif event.type == pygame.MOUSEBUTTONUP:
      for control in gui:
        if gui[control].selected:
          gui[control].select(False)
      for control in lgui:
        if lgui[control].selected:
          lgui[control].select(False)            
          export(current_file,current_path)
    elif event.type == pygame.KEYDOWN:
      pressed = pygame.key.get_pressed()
      if pressed[pygame.K_LCTRL]:  
        if event.key==K_s:
          save_dialog()
        if event.key==K_o:
          load_dialog()
  #============================
  # Rendering
  #============================
  canvas.fill(COLORS[0])
  pygame.draw.rect(canvas,COLORS[2],(0,0,canvas_width,10))
  
  gui["selected_file"].text = current_file

  for control in gui:
    gui[control].draw()
    if gui[control].selected:
      gui[control].edit()
  for control in layer_gui[gui["layer"].value]:
    layer_gui[gui["layer"].value][control].draw()
    if layer_gui[gui["layer"].value][control].selected:
      layer_gui[gui["layer"].value][control].edit()

  # Scaling
  #------
  scaled = pygame.transform.scale(canvas, (canvas_width*2,canvas_height*2))
  screen.blit(scaled,(0,0))
  pygame.display.flip()

pygame.display.quit()
pygame.quit()
