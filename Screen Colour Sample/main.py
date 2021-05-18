import PySimpleGUI as sg
import tkinter as tkr
from tkinter import Canvas
import PIL
from PIL import ImageGrab, Image
import time
import math
import _thread
from pynput.mouse import Listener

#.exe function
#pyinstaller --onefile -w main.py

running = False

#Application Options
increment = 20
lowerLimit = 90
upperLimit = 245
timer = 0.3
screenResolution = [0, 0, PIL.ImageGrab.grab().size[0], PIL.ImageGrab.grab().size[1]]
R = G = B = 90

loggedFunctionTime = []

def GetScreenColour():
    while running == True:
        time.sleep(timer)

        start = time.time()

        PILImage = PIL.ImageGrab.grab(bbox =(screenResolution[0], screenResolution[1], screenResolution[2], screenResolution[3]))

        screenCap = PILImage.load()

        xRes, yRes = PILImage.size[0], PILImage.size[1]

        i = j = l = _R = _G = _B = 0

        while i < xRes:
            while j < yRes:
                capture = screenCap[i, j]
                if (capture[0] > lowerLimit or capture[1] > lowerLimit or capture[2] > lowerLimit) and (capture[0] < upperLimit or capture[1] < upperLimit or capture[2] < upperLimit):
                    _R += capture[0]
                    _G += capture[1]
                    _B += capture[2]
                    l += 1
                j += increment
            i += increment
            j = 0

        if l > 0:
            #_thread.start_new_thread(updateHex, (math.floor(_R / l), math.floor(_G / l), math.floor(_B / l)))
            updateHex(math.floor(_R / l), math.floor(_G / l), math.floor(_B / l))

        end = time.time()

        #print(end - start)
        window.Element("_LENGTH").Update(round((xRes / increment) * (yRes / increment)))
        window.Element("_LOGGED").Update(l)
        #_thread.start_new_thread(logData, (start, end))
        logData(start, end)


def updateHex(_R, _G, _B):
    global R, G, B
    """
    Rinc = (_R - R) / 5
    Ginc = (_G - G) / 5
    Binc = (_B - B) / 5

    for i in range(5):
        #time.sleep(timer / 5)
        R += Rinc
        G += Ginc
        B += Binc
        window.Element("_RGB").Update(str(round(R)) + "," + str(round(G)) + "," + str(round(B)))
        hexDec = RGBtoHex(R, G, B)
        if len(hexDec) == 7:
            window.Element("_Hex").Update(hexDec, button_color=hexDec)
        else:
            print("Error with Hex: ", hexDec)
    """
    hexDec = RGBtoHex(_R, _G, _B)
    if len(hexDec) == 7:
        window.Element("_Hex").Update(hexDec, button_color=hexDec)
    else:
        print("Error with Hex: ", hexDec)

    window.Element("_RGB").Update(str(_R) + "," + str(_G) + "," + str(_B))

    R, G, B = _R, _G, _B

def RGBtoHex(R, G, B):
    return "#" + format(round(R), 'x') + format(round(G), 'x') + format(round(B), 'x')

#Collapse function to help dynamically change the layout of the window.
def collapse(layout, key, visible):
    return sg.pin(sg.Column(layout, key=key, visible=visible))

def logData(start, end):
    loggedFunctionTime.append(round(end - start, 3))
    if len(loggedFunctionTime) > 100:
        loggedFunctionTime.pop(0)
    runGraphFunctions()
    window.Element("_TIME").Update(round(sum(loggedFunctionTime) / len(loggedFunctionTime), 3))

def runGraphFunctions():
    if values["_PLOTFUNCTIMERADIO"]:
        plotFunctionTime()

def plotFunctionTime():
    graph.Erase()
    generateGraph(0, 0, 100, 0.1)
    for x in range(0, 100):
        if x > len(loggedFunctionTime) - 1:
            break
        y = loggedFunctionTime[x] * 1000
        graph.DrawCircle((x, y), 0.9, fill_color='red')

def generateGraph(xAxis, yAxis, xRange, yRange):
    # X Axis
    graph.DrawLine((0, yAxis), (100, yAxis))
    xText = xInc = round(xRange / 10)
    if(xRange <= 1):
        xText = xInc = round(xRange / 10, 2)
    xText -= xInc * round(10 - (100 - xAxis) / 10) + xInc
    labelPlot = -5
    if(xAxis < 80):
        labelPlot = 5

    for x in range(0, 101, 10):
        graph.DrawLine((x, -2 + yAxis), (x, 2 + yAxis))
        if xAxis - x != 0:
            graph.DrawText(xText, (x, labelPlot + yAxis), color='green')
        xText += xInc
        if(xRange <= 1):
            xText = round(xText, 2)

    # Y Axis
    graph.DrawLine((xAxis, 0), (xAxis, 100))
    yText = yInc = round(yRange / 10)
    if(yRange <= 1):
        yText = yInc = round(yRange / 10, 2)
    yText -= yInc * round(10 - (100 - yAxis) / 10) + yInc
    labelPlot = -5
    if(yAxis < 80):
        labelPlot = 5

    for y in range(0, 101, 10):
        graph.DrawLine((-2 + xAxis, y), (2 + xAxis, y))
        if yAxis - y != 0:
            graph.DrawText(yText, (labelPlot + xAxis, y), color='blue')
        yText += yInc
        if(yRange <= 1):
            yText = round(yText, 2)

def showCollectedImg():
    image = PIL.ImageGrab.grab(bbox =(screenResolution[0], screenResolution[1], screenResolution[2], screenResolution[3]))
    screenCap = image.load()
    xRes, yRes = image.size[0], image.size[1]
    i = j = 0

    while i < xRes:
        while j < yRes:
            test = screenCap[i, j]
            if (test[0] > lowerLimit or test[1] > lowerLimit or test[2] > lowerLimit) and (test[0] < upperLimit or test[1] < upperLimit or test[2] < upperLimit):
                screenCap[i, j] = \
                screenCap[i + 1, j] = screenCap[i - 1, j] =\
                screenCap[i + 1, j + 1] = screenCap[i - 1, j - 1] =\
                screenCap[i + 1, j - 1] = screenCap[i - 1, j + 1] =\
                screenCap[i, j + 1] = screenCap[i, j - 1] = (255, 0, 0)
            else:
                screenCap[i, j] = (255, 255, 0)
            j += increment
        i += increment
        j = 0
    image.show()
    _thread.exit()


x1 = x2 = y1 = y2 = None
def newScannedArea():
    overlay = tkr.Tk()
    overlay.attributes("-fullscreen", True, "-alpha", 0.5)
    overlay.geometry(str(PIL.ImageGrab.grab().size[0])+"x"+str(PIL.ImageGrab.grab().size[1]))
    canvas = tkr.Canvas(overlay, width=PIL.ImageGrab.grab().size[0], height=PIL.ImageGrab.grab().size[1])
    selection = canvas.create_rectangle(0, 0, 0, 0, fill="red")
    canvas.pack()

    def on_move(x, y):
        global x1, x2, y1, y2
        if x1 != None and y1 != None:
            canvas.coords(selection, x1, y1, x, y)
            if abs(x - x1) > 100 and abs(y - y1) > 100:
                canvas.itemconfig(selection, fill='green')
            else:
                canvas.itemconfig(selection, fill='red')

    def on_click(x, y, button, pressed):
        global x1, x2, y1, y2
        if pressed:
            x1 = x
            y1 = y
        else:
            x2 = x
            y2 = y

        if not pressed:
            if x1 > x2:
                temp = x2
                x2 = x1
                x1 = temp

            if y1 > y2:
                temp = y2
                y2 = y1
                y1 = temp

            if x2 - x1 > 100 and y2 - y1 > 100:
                screenResolution[0] = x1
                screenResolution[1] = y1
                screenResolution[2] = x2
                screenResolution[3] = y2
                window.Element("_RES").Update(screenResolution)
                x1 = x2 = y1 = y2 = None
                overlay.quit()
                return False
            else:
                x1 = x2 = y1 = y2 = None
                canvas.coords(selection, 0, 0, 0, 0)
    
    with Listener(on_click=on_click, on_move=on_move) as listener:
        overlay.mainloop()
        listener.join()

column1 = 15
column2 = 20

tab1 = [
        #Options
        [sg.Text("Pixel distance on scrape:", size=(column2,1)), sg.Text(increment, key="_INC", size=(3, 1)), sg.Slider(range=(5, 100), size=(20, 20), key="_NEWINC", orientation='h', default_value=increment)],
        [sg.Text("Time between each scrape:", size=(column2,1)), sg.Text(timer, key="_TIMER", size=(3, 1)), sg.Slider(range=(0.1, 1), resolution=.1, size=(20, 20), key="_NEWTIMER", orientation='h', default_value=timer)],
        [sg.Text("Lower colour limit:", size=(column2,1)), sg.Text(lowerLimit, key="_LOWER", size=(3, 1)), sg.Slider(range=(0, 100), size=(20, 20), key="_NEWLOWER", orientation='h', default_value=lowerLimit)],
        [sg.Text("Upper colour limit:", size=(column2,1)), sg.Text(upperLimit, key="_UPPER", size=(3, 1)), sg.Slider(range=(100, 255), size=(20, 20), key="_NEWUPPER", orientation='h', default_value=upperLimit)],
        [sg.Text("Capture Size:"), sg.Text(screenResolution, key="_RES", size=(20, 1)), sg.Button("New Area", key="_NEWRES", tooltip="Click and drag for a new scanned area"),sg.Button("Screen", key="_FULLRES")],
        [sg.Button("Submit"), sg.Button("Default")],
    ]
tab1_layout =  [
        [collapse(tab1, '_TAB1', True)]
    ]

tab2 = [
        #Graph Canvas
        [sg.Graph(canvas_size=(400, 400), graph_bottom_left=(-5,-5), graph_top_right=(105,105), background_color='white', key='_GRAPH')],
        [sg.Radio('Pause', enable_events=True, key='_NONE', group_id="RadioGraph", default=True), sg.Radio('Function Time', enable_events=True, key='_PLOTFUNCTIMERADIO', group_id="RadioGraph")]
    ]
tab2_layout = [
        [collapse(tab2, '_TAB2', False)],
    ]

layout = [
        [sg.Text("Average Colour", font=("Helvetica", 25)), sg.Text("Stopped", size=(7,1), key="_RUNNING")],
        #Colour Data
        [sg.Frame(layout=[      
            [sg.Text("Current Hex:", size=(column1,1)), sg.Button("#000000", size=(20,2), key="_Hex", button_color="#000000", tooltip="Click to see scrape sample.")],
            [sg.Text("Current RGB:", size=(column1,1)), sg.Text("0", key="_RGB", size=(11,1))],
            [sg.Text("# Pixels Checked:", size=(column1,1)), sg.Text("0",size=(7,1), key="_LENGTH")],
            [sg.Text("# Pixels Logged:", size=(column1,1)), sg.Text("0",size=(7,1), key="_LOGGED")],
            [sg.Text("Time Avg.(s):", size=(column1,1)), sg.Text("0",size=(7,1), key="_TIME")]
        ],title='Colour Data', relief=sg.RELIEF_SUNKEN)],

        #Tabs
        [sg.TabGroup([[sg.Tab('Options', tab1_layout), sg.Tab("Graph Data", tab2_layout)]], key="_TABS", enable_events=True)],

        #Control Buttons
        [sg.Text('_'  * 58)],
        [sg.Button("Start", button_color="green", focus=True), sg.Button("Stop", button_color="red")],
        [sg.Button("Close")]
    ]

window = sg.Window("Average Screen Colour", layout, finalize=True)
graph = window['_GRAPH']

while True:
    event, values = window.read()

    if event == "Start" and running == False:
        running = True
        _thread.start_new_thread(GetScreenColour, ())

    if event == "Stop":
        running = False

    if event == "Close" or event == sg.WIN_CLOSED:
        break

    if event == "_Hex":
        _thread.start_new_thread(showCollectedImg, ())

    if event == "_NEWRES":
        running = False
        _thread.start_new_thread(newScannedArea, ())

    if event == "_TABS":
        if values["_TABS"] == "Options":
            window['_TAB1'].update(visible=True)
        else:
            window['_TAB1'].update(visible=False)

        if values["_TABS"] == "Graph Data":
            window['_TAB2'].update(visible=True)
        else:
            window['_TAB2'].update(visible=False)

    #Input Sanitization
    #if event == '_INC' and values['_INC'] and values['_INC'][-1] not in ('0123456789'):
    #    window['_INC'].update(values['_INC'][:-1])

    if event == "Submit":
        increment = int(values['_NEWINC'])
        window.Element("_INC").Update(int(values['_NEWINC']))

        timer = values['_NEWTIMER']
        window.Element("_TIMER").Update(values['_NEWTIMER'])

        lowerLimit = int(values['_NEWLOWER'])
        window.Element("_LOWER").Update(int(values['_NEWLOWER']))

        upperLimit = int(values['_NEWUPPER'])
        window.Element("_UPPER").Update(int(values['_NEWUPPER']))

    if event == "Default":
        increment = 20
        window.Element("_NEWINC").Update(value=20)
        window.Element("_INC").Update(value=20)

        timer = 0.3
        window.Element("_NEWTIMER").Update(value=0.3)
        window.Element("_TIMER").Update(value=0.3)

        lowerLimit = 90
        window.Element("_NEWLOWER").Update(value=90)
        window.Element("_LOWER").Update(value=90)

        upperLimit = 245
        window.Element("_NEWUPPER").Update(value=245)
        window.Element("_UPPER").Update(value=245)

    if event == "_FULLRES":
        screenResolution = [0, 0, PIL.ImageGrab.grab().size[0], PIL.ImageGrab.grab().size[1]]
        window.Element("_RES").Update(screenResolution)

    if running:
        window.Element("_RUNNING").Update("Running", text_color="#00ff00")
    else:
        window.Element("_RUNNING").Update("Stopped", text_color="red")

window.close()
