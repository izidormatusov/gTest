#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# gTest - find out where the network problem is
#
# Author: Izidor Matušov <izidor.matusov@gmail.com>
# License: GNU GPLv2
#
# This program is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by 
# the Free Software Foundation; either version 2 of the License, or 
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License 
# for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program; if not, write to the Free Software Foundation, Inc., 
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import os, sys

try:
	import pygtk
	pygtk.require("2.0")
	import gtk
except:
	sys.stderr.write("Error: PyGTK and GTK 2.xx must be installed to run this application. Exiting\n")
	sys.exit(1)

class Tester:

	UNDEFINED_STATE = "???"

	def __init__(self, accessPoints):
		self.window = gtk.Window()
		self.window.connect("destroy", gtk.main_quit)
		self.window.set_border_width(10)
		self.window.set_icon_name("preferences-desktop-remote-desktop")
		self.window.set_title(u"Testovač pripojenia")

		vbox = gtk.VBox(spacing = 10)

		head = gtk.HBox()

		img = gtk.Image()
		head.pack_start(img)

		label = gtk.Label(u"<b>Testovač pripojenia</b>")
		label.set_use_markup(True)
		head.pack_start(label)

		vbox.pack_start(head)

		table = gtk.Table(rows = len(accessPoints), columns = 2)

		self.points = []
		for line, (name, address) in enumerate(accessPoints):
			nameLabel = gtk.Label(name)
			table.attach(nameLabel, 0, 1, line, line+1)

			stateLabel = gtk.Label(self.UNDEFINED_STATE)
			table.attach(stateLabel, 1, 2, line, line+1)

			self.points.append( {'name': nameLabel, 'state': stateLabel, 'address': address } )

		vbox.pack_start(table)

		self.startButton = gtk.Button(stock= gtk.STOCK_EXECUTE)
		self.startButton.connect("clicked", self.start)
		vbox.pack_start(self.startButton)

		self.progressBar = gtk.ProgressBar()
		vbox.pack_start(self.progressBar)


		self.window.add(vbox)
		self.window.show_all()
		self.progressBar.hide()
	
	def run(self):
		gtk.main()
	
	def start(self, button):
		""" build """

		self.progressBar.show()
		self.progressBar.set_fraction(0.0)
		step = 1.0 / len(self.points)
		fraction = 0.0

		self.startButton.hide()

		while gtk.events_pending():
			gtk.main_iteration()

		map(lambda point: point['state'].set_text(self.UNDEFINED_STATE), self.points)

		for point in self.points:
			name = point['name'].get_text()

			self.progressBar.set_text(u"Testujem bod '%s'"% (name) )
			point['name'].set_text('<i>'+ name + '</i>')
			point['name'].set_use_markup(True)


			while gtk.events_pending():
				gtk.main_iteration()

			returnCode = os.system('ping -c2 "%s"' % point['address'])

			point['name'].set_text(name)
			if returnCode == 0:
				point['state'].set_text("<span color='green'>OK</span>")
				point['state'].set_use_markup(True)
				fraction += step
				self.progressBar.set_fraction(fraction)
			else:
				point['state'].set_text("<span color='red'>Problém</span>")
				point['state'].set_use_markup(True)
				break

		self.progressBar.hide()
		self.startButton.show()
		while gtk.events_pending():
			gtk.main_iteration()



if __name__ == "__main__":
        accessPoints = [('Point A', '1.1.1.1'),
                        ('Point B', '2.2.2.2'),
                        ('Point C', '3.3.3.3'),
                        ('Google DNS', '8.8.8.8')]
	Tester(accessPoints).run()
