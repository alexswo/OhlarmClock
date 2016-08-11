#!/usr/bin/env python
import pygame
import subprocess
musicPlaying = False
volume = 1
class musicPlayer:
    def soundAlarm(self):
        global musicPlaying 
        pygame.mixer.init()
        if(pygame.mixer.music.get_busy()): 
            musicPlaying = True
            return
        else: musicPlaying = False
	pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.load("Music/ripndip.wav")
        pygame.mixer.music.play()
#if a button is pressed, then call pygame.mixer.quit()
    def exitAlarm(self):
        global musicPlaying
        if musicPlaying == False: return
        pygame.mixer.quit()
        pygame.mixer.init()
        musicPlaying = False
    def adjustVolume(self, volume_code):
        global volume
        if (volume_code == 1):
            if (volume + .05) <= 1:
                volume = volume + .05
                #print "Volume Incremented. Vol is: ", volume   
        else:
            if (volume - .05) >= 0:
                volume = volume - .05
                #print "Volume Decremented. Vol is: ", volume
    def getVolume(self):
	return volume
