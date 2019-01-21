#ilerm
#17/01/2019
from tkinter import *
import time

root = Tk()
root.title("Pixel Splines")
root.geometry('700x601')#1320

cellsize = 10
canvas = Canvas(root,height=603,width=700,bg="white",borderwidth=-3)
canvas.place(x=0,y=0)
points = []
pixelPath = []

#textbox
txt = Text(root,height = 30, width=10)
txt.insert(END, """0,0
25,9
32,32
39,52
60,60""")
txt.place(x=601,y=26)

#draw grid
for i in range(61):
	canvas.create_line(i*cellsize,0,i*cellsize,600,tags="grid")
	canvas.create_line(0,i*cellsize,600,i*cellsize,tags="grid")
	
def DrawTile(x, y, c):
	canvas.create_rectangle(x*cellsize,y*cellsize,x*cellsize+cellsize,y*cellsize+cellsize,fill=c,tags="tile")
	
def SplinePoint(t): #thanks @Javidx9
	p1 = int(t) + 1
	p2 = p1 + 1
	p3 = p1 + 2
	p0 = p1 - 1
	
	t = t - int(t)
	tt = t * t
	ttt = tt * t
	
	q1 = -ttt + 2*tt - t
	q2 = 3*ttt - 5*tt + 2
	q3 = -3*ttt + 4*tt + t
	q4 = ttt - tt
	
	tx = 0.5 * (points[p0][0] * q1 + points[p1][0] * q2 + points[p2][0] * q3 + points[p3][0] * q4)
	ty = 0.5 * (points[p0][1] * q1 + points[p1][1] * q2 + points[p2][1] * q3 + points[p3][1] * q4)
	return (int(tx),int(ty))

def UpdatePoints():
	global points
	str = txt.get(1.0, END)
	strlist = str.split("\n")
	points.clear()
	
	for e in strlist:
		if e is not "":
			points.append(eval(e))
			
	#duplicate start and end points
	points.insert(0,points[0])
	points.append(points[len(points)-1])
	
def CalculatePath():
	time = 0
	end = len(points) - 3
	jump = 0.002
	pixelPath.clear()
	while time <= end:
		tile = SplinePoint(time)
		if tile not in pixelPath:
			pixelPath.append(tile)
		
		time += jump

def DrawPixelPath():
	for p in pixelPath:
		DrawTile(p[0],p[1],"black")

def DrawPoints():
	for p in points:
		DrawTile(int(p[0]),int(p[1]),"blue")

def OnApply():	
	UpdatePoints()
	canvas.delete("tile")
	CalculatePath()
	DrawPixelPath()
	DrawPoints()

#button
btn_apply = Button(root, text="Apply", command=OnApply)
btn_apply.place(x=601,y=0)

OnApply()
root.mainloop()
