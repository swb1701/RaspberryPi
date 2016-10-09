#!/usr/bin/python

import usb.core
import os
import pygame
import pygameui as ui

os.putenv('SDL_FBDEV', '/dev/fb1')

dev=usb.core.find(idVendor=0x16c0,idProduct=0x5dc)

assert dev is not None

print dev

print hex(dev.idVendor)+','+hex(dev.idProduct)

class PiTft(ui.Scene):
    def __init__(self):
        ui.Scene.__init__(self)

        self.add_child(ui.Label(ui.Rect(0,0,320,50),'Raspberry Pi Sound Meter'))

        self.progress_view = ui.ProgressView(ui.Rect(20, 50, 280, 120))
        self.add_child(self.progress_view)

        self.db_value = ui.Label(ui.Rect(110, 170, 100, 30), '00.00 dB')
        self.add_child(self.db_value)

        self.progress = 0
        
    def update(self, dt):
        ui.Scene.update(self, dt)
        ret = dev.ctrl_transfer(0xC0,4,0,0,200)
        dB = (ret[0]+((ret[1]&3)*256))*0.1+30
        self.db_value.text = '%2.2f dB' % dB
        self.progress=(dB/100.0)
        self.progress_view.progress = self.progress
            
if __name__ == '__main__':
    ui.init('SoundMeter UI', (320, 240))
    ui.scene.push(PiTft())
    pygame.mouse.set_visible(False)
    ui.run()
