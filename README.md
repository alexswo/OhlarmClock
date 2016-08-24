# OhlarmClock
####DIY alarm clock built on a Raspberry Pi 2 Model B
<br />
<br />

#THIS IS STILL IN ALPHA

<p align="center">
<a href="http://imgur.com/FB51WWR"><img src="http://i.imgur.com/FB51WWRl.jpg" title="source: imgur.com" /></a>
</p>
<br />
<br />
###Introduction
  The purpose of this homemade alarm clock was to experiment with the Raspberry Pi 2 Model B and to provide a gift to my parents. The house that my parents reside in rarely has any blackouts; however, when they do occur, all of the digital clocks in the house need to be manually set. With the OhlarmClock, it will continue to perform regularly after a blackout by fetching time from the internet. In the future, I hope to make the OhlarmClock capable of drawing power from a constantly charging battery so that it will be able to run through a blackout. I also hope to utilize the OhlarmClock as the next "home controlling" siri by implementing machine learning. 
<br />
###Hardware Used:

[1.2″ 4-Digit 7-Segment display](https://www.adafruit.com/products/1268)<br />
[Blue OLED 16x2](https://www.adafruit.com/products/823)<br />
[Metal Push Button](https://www.adafruit.com/products/481)<br />
[Rotary Encoder](https://www.adafruit.com/products/377)<br />
[Metal Knob for Rotary Encoder](https://www.adafruit.com/products/2056)<br />
(2) [3" - 8 Ohm 1 Watt Speakers](https://www.adafruit.com/products/1313)<br />
[2.1W Class D Audio Amplifier ](https://www.adafruit.com/products/1552)<br />
[3.5mm Plug/Plug Cable](https://www.adafruit.com/products/876)<br />
[USB Audio Adapter](https://www.adafruit.com/products/1475)<br />

Everything is connected internally with a breadboard that was provided in the Vilros Raspberry Pi kit. Also, a usb wifi dongle was used to access the interwebs. <br />
To assemble the shell/frame of the clock, I purchased a 12" x 30" Baltic Birch Plywood with 1/4" thickness. Then using Adobe Illustrator, I created a CAD file so that my local laser cutting shop could cut out the wood to my specifications. <br />

###Current Features:
####Weather
By using Wunderground's API, the OhlarmClock updates every 15 minutes the high and low temperatures for that day. The OhlarmClock will also raise a signal whenever there is a high chance of rain.
####Internet Radio


