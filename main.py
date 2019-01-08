# -*- coding: utf-8 -*-
import pyglet
import random
from pyglet.sprite import Sprite
from pyglet.gl import *  #for particials
import pickle
import threading
import socketserver
from socketserver import StreamRequestHandler as SRH

HOST = ''
PORT = 9999
addr = (HOST, PORT)
signal = '99|0'

display = pyglet.window.get_platform().get_default_display().get_screens()[-1]
WIDTH = display.width
HEIGHT = display.height
# WIDTH = 1600
# HEIGHT = 900


class Servers(SRH):
    def handle(self):
        global signal
        signal1 = self.request.recv(1024).decode('utf-8').strip()
        if signal1:
            signal = signal1


class PartialBatch(pyglet.graphics.Batch):
    def __init__(self, win):
        super(PartialBatch, self).__init__()
        self.win = win
        self.particles = []
        self.gravity = -100

    def add_particles(self):
        particle = self.add(1, GL_POINTS, None,
                             ('v2f/stream', [self.win['w'] / 2, 0]))
        particle.dx = (random.random() - .5) * self.win['w'] / 4
        particle.dy = self.win['h'] * (.5 + random.random() * .2)
        particle.dead = False
        self.particles.append(particle)

    def update_particles(self, dt):
        for particle in self.particles:
            particle.dy += self.gravity * dt
            vertices = particle.vertices
            vertices[0] += particle.dx * dt
            vertices[1] += particle.dy * dt
            if vertices[1] <= 0:
                particle.delete()
                particle.dead = True
        self.particles = [p for p in self.particles if not p.dead]

    def loop(self, dt):
        self.update_particles(dt)
        for i in range(min(100, 2000 - len(self.particles))):
            self.add_particles()


class Pic(pyglet.sprite.Sprite):
    def __init__(self, img, x, y, win, lucky=0, batch=None):
        super(Pic, self).__init__(img)
        self.img = img
        self.x = x
        self.y = y
        self.batch = batch
        self.scale_x = 0.4 * win[0]*(2+lucky)/((1+lucky)*(6+lucky)) / self.img.width
        self.scale_y = 0.4 * win[0]*(2+lucky)/((1+lucky)*(6+lucky)) *4/(3 * self.img.height)


class Lucky(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Lucky, self).__init__(width=WIDTH, height=HEIGHT, screen=display, fullscreen=True)

        self.prepare = 99
        self.lucky = 0  # 1, 2, 3, 5

        self.player1 = pyglet.media.Player()
        music1 = pyglet.resource.media('1.mp3')
        looper = pyglet.media.SourceGroup(music1.audio_format, None)
        looper.loop = True
        looper.queue(music1)
        self.player1.queue(looper)
        self.player1.play()

        self.player2 = pyglet.media.Player()
        self.music2 = pyglet.resource.media('2.mp3')
        self.player2.queue(self.music2)
        self.player2.push_handlers(self.on_eos)

        self.player3 = pyglet.media.Player()
        music3 = pyglet.resource.media('3.mp3')
        looper3 = pyglet.media.SourceGroup(music3.audio_format, None)
        looper3.loop = True
        looper3.queue(music3)
        self.player3.queue(looper3)

        self.ground = pyglet.image.load('bk.jpg')
        self.starBatch = pyglet.graphics.Batch()
        self.stars = []
        starImg = pyglet.resource.image('star.png')
        starImg.anchor_x = starImg.width / 2
        starImg.anchor_y = starImg.height / 2
        for i in range(50):
            star = Sprite(img=starImg, batch=self.starBatch, x=random.randint(1, self.width),
                          y=random.randint(1, self.height))
            star.scale = random.random()
            self.stars.append(star)
        #particials
        self.particials = PartialBatch({'w': self.width, 'h': self.height})

        #load lucky population
        self.total = pickle.load(open('total','rb'))
        self.picBatch = pyglet.graphics.Batch()
        self.picDict = {}
        for i in self.total:
            spt = pyglet.text.Label(str(i).zfill(3),
                                       font_size=70, x=-1000, y=-1000,
                                       anchor_x= 'center', anchor_y='center', batch=self.picBatch)
            self.picDict[spt] = i

        self.title = pyglet.text.Label('Fiskars Ningbo 2019 Annual Dinner',
                                       font_size=35, x=self.width/2, y=self.height *6/7,
                                       anchor_x= 'center', anchor_y='center')

        self.luckyTitle = pyglet.text.Label('',
                                       font_size=80, x=self.width / 2, y=self.height * 5 / 7,
                                       anchor_x='center', anchor_y='center')

        self.samples = []

        pyglet.clock.schedule(self.update)

    def update(self, dt):
        global signal
        self.particials.loop(dt)

        if self.lucky == 0:
            self.luckyTitle.text = ''
        #stars
        for star in self.stars:
            star.scale = random.random()
            star.rotation += 360 * dt
            if star.rotation >= 360:
                self.rotation = 0

        if self.prepare == 0:
            self.player3.play()

            for pic in self.picDict.keys():
                pic.x = -1000
                pic.y = -1000

            for sample in self.samples:
                sample.x = -1000
                sample.y = -1000

            if self.lucky == 1:
                self.luckyTitle.text = '一等奖'
                self.samples = random.sample(self.picDict.keys(), 1)
                for sample in self.samples:
                    sample.font_size = 160
                    sample.x = self.width / 2
                    sample.y = self.height / 2
            elif self.lucky == 2:
                self.luckyTitle.text = '二等奖'
                self.samples = random.sample(self.picDict.keys(), 1)
                for sample in self.samples:
                    sample.font_size = 160
                    sample.x = self.width / 2
                    sample.y = self.height / 2
            elif self.lucky == 3:
                self.luckyTitle.text = '三等奖'
                self.samples = random.sample(self.picDict.keys(), 1)
                for sample in self.samples:
                    sample.font_size = 160
                    sample.x = self.width / 2
                    sample.y = self.height / 2
            elif self.lucky == 5:
                self.luckyTitle.text = '阳光普照奖'
                self.samples = random.sample(self.picDict.keys(), 10)
                for i in range(10):
                    if i < 5:
                        self.samples[i].x = self.width * (i+1) / (1 + self.lucky)
                        self.samples[i].y = self.height * 5 / 10
                    else:
                        self.samples[i].x = self.width * (i-5+1) / (1 + self.lucky)
                        self.samples[i].y = self.height * 2 / 10
                    self.samples[i].font_size = 70
            elif self.lucky == 100:
                self.luckyTitle.text = ''
                self.samples = random.sample(self.picDict.keys(), 1)
                for sample in self.samples:
                    sample.font_size = 120
                    sample.x = self.width / 2
                    sample.y = self.height / 2
        elif self.prepare == 1:
            self.player3.pause()
            self.player2.play()

            s = []
            for sample in self.samples:
                s.append(self.picDict[sample])  #record the sample id
                self.picDict.pop(sample)  #remove from total dict

            #write to total
            totalfile = open('total','wb')
            pickle.dump(list(self.picDict.values()), totalfile)
            totalfile.close()
            #write to prize file
            self.picklefile(self.lucky, s)

            signal = '99|' + str(self.lucky)

        self.prepare = int(signal.split('|')[0])
        self.lucky = int(signal.split('|')[1])

    def on_eos(self):
        self.player2 = None
        self.player2 = pyglet.media.Player()
        self.player2.queue(pyglet.resource.media('2.mp3'))
        self.player2.push_handlers(self.on_eos)

    def picklefile(self, lucky, list):
        if lucky == 1:
            try:
                s = pickle.load(open('prize1','rb'))
            except Exception as e:
                s = []
            s = s + list
            f = open('prize1','wb')
            pickle.dump(s, f)
            f.close()
        elif lucky == 2:
            try:
                s = pickle.load(open('prize2', 'rb'))
            except Exception as e:
                s = []
            s = s + list
            f = open('prize2', 'wb')
            pickle.dump(s, f)
            f.close()
        elif lucky == 3:
            try:
                s = pickle.load(open('prize3', 'rb'))
            except Exception as e:
                s = []
            s = s + list
            f = open('prize3', 'wb')
            pickle.dump(s, f)
            f.close()
        elif lucky == 5:
            try:
                s = pickle.load(open('prize5', 'rb'))
            except Exception as e:
                s = []
            s = s + list
            f = open('prize5', 'wb')
            pickle.dump(s, f)
            f.close()
        elif lucky == 100:
            try:
                s = pickle.load(open('prize100', 'rb'))
            except Exception as e:
                s = []
            s = s + list
            f = open('prize100', 'wb')
            pickle.dump(s, f)
            f.close()

    def on_draw(self):
        self.clear()
        self.ground.blit(0,0)
        self.title.draw()
        self.luckyTitle.draw()
        self.starBatch.draw()
        self.particials.draw()
        self.picBatch.draw()


if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(addr, Servers)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()

    Lucky()
    pyglet.app.run()
