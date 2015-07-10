# -*- coding: utf-8 -*-
"""
    circle_select.py: Load an image file and find the average color in a
    scalable circle area
    
    Copyright (C) 2013  Greg von Winckel

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Last updated: Thu Oct 10 11:35:21 MDT 2013
"""

import numpy as np
import Tkinter,tkFileDialog
from pylab import *

class selector(object):
    """ Movable, resizable, circluar pixel selector """
    def __init__(self,ax,facecolor,edgecolor):
        self.radius = 1
        self.patch = Circle((5,5),radius = self.radius,
                     fc=facecolor,ec=edgecolor)
        self.patch.set_alpha(0.3)
        ax.add_patch(self.patch)

    def update_position(self,x,y):
        """ Move the selector with the mouse """
        self.patch.center = (x,y)          
        draw()

    def increase_size(self):
        """ Make the selection circle larger """
        self.radius += 1
        self.patch.set_radius(self.radius)
        draw()

    def decrease_size(self):
        """ make the selection circle smaller """
        if self.radius > 0:  
            self.radius -= 1
            self.patch.set_radius(self.radius)
            draw()

class index_manager(object):
    def __init__(self,shape):
        x = np.arange(shape[1])
        y = np.arange(shape[0])
        xx,yy = np.meshgrid(x,y)        
        self.xf = xx.flatten("F")
        self.yf = yy.flatten("F")
  
    def get_indices(self,x,y,r):
        """ Find the index of every pixel which lies within
            the circle of radius r, centered at (x,y) """      
        dex = np.where((self.xf-x)**2+(self.yf-y)**2<r**2)[0]
        return dex

class sampler(object):
    def __init__(self,ax,img):

        self.ax = ax

        # Extract the color channels
        self.red = img[:,:,0].flatten("F")
        self.green = img[:,:,1].flatten("F")
        self.blue = img[:,:,2].flatten("F")

        # Convert 0-255 integer to 0-1 float if needed
        if img.dtype == 'uint8':
            self.scale = 1.0/255.0
        else:
            self.scale = 1

        self.dexman = index_manager(img.shape)
               
        # Create a transparent blue circular selector with a 
        # red border
        self.circ = selector(ax,facecolor='b',edgecolor='r')

    def update_pixelcount(self):
        dex = self.dexman.get_indices(self.x,self.y,self.circ.radius)
        npts = str(len(dex))
        
        # Compute average colors for each channel in circlular region
        R = np.mean(self.red[dex])*self.scale
        B = np.mean(self.blue[dex])*self.scale
        G = np.mean(self.green[dex])*self.scale      

        # Tell how many pixels are in the area using text that is
        # the average color for the area
        self.ax.set_title(npts+' pixels selected',fontsize=20,color=((R,G,B)))


    def mouse_move(self,event):
        # Don't do anything if were are not on the image area
        if not event.inaxes: return

        # get pixel coordinates 
        self.x,self.y = map(np.round,(event.xdata,event.ydata))
        self.update_pixelcount() 

        # Move the circle
        self.circ.update_position(self.x,self.y)

    def mouse_scroll(self,event):
        # Change the size of the circle
        if event.button == 'up':
            self.circ.increase_size()
        elif event.button == 'down':
            self.circ.decrease_size()

        self.update_pixelcount() 

    def key_press(self,event):
        # Change the size of the circle
        if event.key == 'up':
            self.circ.increase_size()
        elif event.key == 'down':
            self.circ.decrease_size()


def getfile():
    FILEOPENOPTIONS = dict(defaultextension='.jpg',
                       filetypes=[("Image Files",("*.jpg","*.gif","*.png")), 
                       ('All files','*.*')])
    # Create Dialog to open file
    root = Tkinter.Tk()
    root.withdraw()
    file_path = tkFileDialog.askopenfilename(**FILEOPENOPTIONS)
    root.destroy()
    return file_path



if __name__ == '__main__':

    # Get the name and path of the image file to open
    file_path = getfile()

    # Read in the image
    img = imread(file_path)

    fig = figure(1)
    fig.canvas.set_window_title('Up/Down to change selection size.')
    ax = fig.add_subplot(111)
    ax.imshow(img)
    ax.set_xlim(0,img.shape[1]-1)
    ax.set_ylim(img.shape[0],0)
    ax.set_axis_off()
    circ = sampler(ax,img)
    connect('motion_notify_event',circ.mouse_move)
    connect('scroll_event',circ.mouse_scroll)
    connect('key_press_event',circ.key_press)
    show()

