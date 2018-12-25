#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from time import sleep
import os
from luma.core.render import canvas
from demo_opts import get_device
from PIL import ImageFont
from PIL import Image
font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                            'fonts', 'PIXEARG_.TTF')) #C&C Red Alert [INET].ttf'))
font = ImageFont.truetype(font_path, 8)
chars = {'ö':chr(246),'ä':chr(228),'ü':chr(252),'ß':chr(223),'Ä':chr(196),'Ü':chr(220),'Ö':chr(214),'%20':' ',' 1/4':chr(252),'%C3%9C':chr(220),'%C3%BC':chr(252),'%C3%84':chr(196),'%C3%A4':chr(228),'%C3%96':chr(214),'%C3%B6':chr(246),'%C3%9F':chr(223)}

def SetCharacters(text):
    for char in chars:
       text = text.replace(char,chars[char])
    return text

def GetMPC(command):
    from subprocess import check_output
    process = check_output(command.split())
    for char in chars:
       process = process.replace(char,chars[char])
    return process

def ShowImage():
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'images', 'notes.png'))
    logo = Image.open(img_path).convert("RGBA")
    fff = Image.new(logo.mode, logo.size, (255,) * 4)
    background = Image.new("RGBA", device.size, "black")
    posn = ((device.width - logo.width) // 2, 0)
    img = Image.composite(logo, fff, logo)
    background.paste(img, posn)
    device.display(background.convert(device.mode))
    sleep(0.2)

def main(num_iterations=sys.maxsize):
#    device = get_device()
    while num_iterations > 0:
        try:
          num_iterations = 1
          sleep(0.4)
          mpcstatus = GetMPC("mpc status")
          playing = mpcstatus.split("\n")[1].split(" ")[0] #Split to see if mpc is playing at the moment
          file = GetMPC("mpc -f %file% current") # Get the current title
          if (playing == "[playing]") or (playing == "[paused]"): # If it is currently playing
            if file.startswith("http"): # if it is a http stream!
              name = GetMPC("mpc -f %name% current")
              titel = GetMPC("mpc -f %title% current")
              with canvas(device) as draw:
                draw.text((0, 12),titel,font=font, fill="cyan")
            else: # if it is not a stream
              album = GetMPC("mpc -f %album% current"  )
              titel = GetMPC("mpc -f %title% current")
              track = GetMPC("mpc -f %track% current")
              timer = GetMPC("mpc -f %time% current")
              artist = GetMPC("mpc -f %artist% current")
              #playlist = GetMPC("mpc -f %file% playlist")
              elapsed = mpcstatus.split("\n")[1].split(" ")[4]
              #track = "Track: "+track+"   "+elapsed
              if playing == "[paused]":
                plpause = "PAUSE"
              else:
                plpause = ""
              with canvas(device) as draw:
                draw.text((0, 0),artist, font=font, fill="white")
                draw.text((0, 12),titel,font=font, fill="white")
                if track == "\n":
                  draw.text((0, 24),elapsed,font=font, fill="white")
                  draw.text((0, 24),plpause,font=font, fill="white")
                else:
                  draw.text((0, 24),"Track "+track,font=font, fill="white")
                  draw.text((55, 24),elapsed,font=font, fill="white")
                  draw.text((55, 24),plpause,font=font, fill="white")
                draw.text((0, 36),album,font=font, fill="white")
                laenge="-"+artist+"-"
                if artist == "\n":
                  filename = GetMPC("mpc -f %file% current")
                  filename = filename.split(":")[2]
                  filename = SetCharacters(filename)
                  file = filename.split("/")
                  draw.text((0, 0),file[1], font=font, fill="white")
                  draw.text((0, 36),file[0], font=font, fill="white")
          else:
#            with canvas(device) as draw:
#              draw.text((0, 0),"Karte auflegen...", font=font, fill="white")
             ShowImage()
        except:
          ShowImage()
          #with canvas(device) as draw:
            #draw.text((0, 0),"Houston, wir haben ein", font=font, fill="white")
            #draw.text((0, 10),"Problem", font=font, fill="white")
            #draw.text((0, 20),"Ruf den Papa :-)", font=font, fill="white") 

if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
