# Citation Note: The sound algorithms in isid POPs! draw from and build
# upon Pat Virtue's implementation of pitch synthesis & sequencing
# and harmonic generation. Specifically the use of lists for horizontal
# sequencing, the use of loops & sine formulas for tone generation, and the
# technique of adding amplitudes of two tones of a given sample in time for
# harmonic generation (which is exploited generally in POPs! for the effect of
# "layering") are ideas used in this project. All image and sound assets are
# original work.

from cmu_graphics import *
from PIL import Image
import os, pathlib
import string
import random
import wave
import struct
import math
###########################################################
#CLASSES:
#SECTIONS (contains MODULE objects)
class SECTION:
    nextIDindex = 0
    ABC = string.ascii_uppercase
    nextID=ABC[nextIDindex]
    def __init__(self):
        # UNIQUE SECTION IDS
        self.ID = SECTION.nextID
        self.IDnum = SECTION.nextIDindex
        SECTION.nextIDindex+=1
        SECTION.nextIDindex%=26
        ABC = string.ascii_uppercase
        SECTION.nextID=ABC[SECTION.nextIDindex]
        # SECTIONS MODULES LIST
        self.modulesList=[]
        # SECTION TRACK
        self.sectionTrack=None
        self.bars=2
    def __repr__(self):
        return f'{self.ID}'
#MODULES (each corresponds to a respective MENU object)
class MODULE:
    nextID = 0
    def __init__(self, app, type, x, y):
        # UNIQUE MODULE IDS
        self.ID = MODULE.nextID
        MODULE.nextID+=1
        self.type=type
        self.mix=5
        self.x = x
        self.y = y
        self.startDrag=False
        # SAMPLE MODULE GRAPHICS
        if type=='SAMPLE':
            self.image = app.SAMPLEimage
            self.imageWidth = app.SAMPLEimageWidth
            self.imageHeight = app.SAMPLEimageHeight
            self.highlight=app.SAMPLEimageHighlight
        # SYNTH MODULE GRAPHICS
        elif type=='SYNTH':
            self.image = app.SYNTHimage
            self.imageWidth = app.SYNTHimageWidth
            self.imageHeight = app.SYNTHimageHeight
            self.highlight=app.SYNTHimageHighlight
        # SAMPLE MODULE MENU
        if type=='SAMPLE':
            self.menu=MENU(app, 'SAMPLE')
        # SYNTH MODULE MENU
        else:
            self.menu=MENU(app, 'SYNTH')
    def __repr__(self):
        return f'Module: {self.ID}'
#MENUS
class MENU:
    def __init__(self, app, type):
        self.showMenu=False
        self.x=app.width/2
        self.y=app.height/2
        self.startDrag=False
        self.patternRendered=[]
        self.patternTrack=None
        # SAMPLE MENU GRAPHICS
        if type=='SAMPLE':
            self.image = app.SAMPLEMENUimage
            self.imageWidth = app.SAMPLEMENUimageWidth
            self.imageHeight = app.SAMPLEMENUimageHeight
            self.highlightRetrig=app.SAMPLEMENUimageRetrig
            self.highlightFullPlay=app.SAMPLEMENUimageFullPlay
        # SAMPLE MENU SOUNDS
            self.MIDIlist=[] # To hold MIDI objects
            self.sample='samples/.wav'
            self.patternFramework=[[1/8, False, 'trigger'], [1/8, False, 'trigger'],
                                   [1/8, False, 'trigger'], [1/8, False, 'trigger'],
                                   [1/8, False, 'trigger'], [1/8, False, 'trigger'],
                                   [1/8, False, 'trigger'], [1/8, False, 'trigger'],
                                   [1/8, False, 'trigger'], [1/8, False, 'trigger'],
                                   [1/8, False, 'trigger'], [1/8, False, 'trigger'],
                                   [1/8, False, 'trigger'], [1/8, False, 'trigger'],
                                   [1/8, False, 'trigger'], [1/8, False, 'trigger']]
        # SYNTH MENU GRAPHICS
        elif type=='SYNTH':
            self.image = app.SYNTHMENUimage
            self.imageWidth = app.SYNTHMENUimageWidth
            self.imageHeight = app.SYNTHMENUimageHeight
            self.highlightSine=app.SYNTHMENUimageSine
            self.highlightSaw=app.SYNTHMENUimageSaw
            self.highlightSquare=app.SYNTHMENUimageSquare
        # SYNTH MENU SOUNDS
            self.sound='sine'
            #Future iterations of isid POPs! may incorporate other synth sounds
            self.MIDIlist1=[]
            self.MIDIlist2=[]
            self.MIDIlist3=[]
            self.MIDIlist4=[]
            self.MIDIlistList=[self.MIDIlist1, self.MIDIlist2, self.MIDIlist3, self.MIDIlist4]
            # Note: This implementation of multiple pattern frameworks sets the groundwork for the SYNTH module
            # to output up to 4 voices in future iterations of this project
            self.patternFramework1=[[1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None]]
            self.patternFramework2=[[1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None]]
            self.patternFramework3=[[1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None]]
            self.patternFramework4=[[1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None],
                                   [1/8, False, 'trigger', None], [1/8, False, 'trigger', None]]
            self.patternFrameworkList=[self.patternFramework1, self.patternFramework2,
                                       self.patternFramework3, self.patternFramework4]
class MIDI:
    def __init__(self, app, x, y, index, noteType=1/8):
        self.image = app.MIDIimage
        self.selectedImage = app.MIDIselectedImage
        self.x = x
        self.y = y
        self.imageWidth = 48
        self.imageHeight = 48
        self.index = index
        self.noteType=noteType
        #For MIDI reinit
        self.MIDIdefaultX = x
        self.MIDIdefaultY = y
    def __repr__(self):
        return f'{self.x}, {self.y}'
#MISC ICONS
class ICON:
    def __init__(self, image, x, y, width, height, label=False):
        self.image = image
        self.x = x
        self.y = y
        self.imageWidth = width
        self.imageHeight = height
        self.showHighlight=False
        self.highlight=None
        self.label=label
    def __repr__(self):
        return f'{self.x}, {self.y}'
###########################################################
#INITIALIZING:
def onAppStart(app):
    #GENERAL DIMENSIONS:
    app.width=960
    app.height=720
    app.savedWidth=960
    app.savedHeight=720
    app.makeupX=None
    app.makeupY=None
    #SOUND PLAYING:
    app.playing=False
    #STEP COUNTERS:
    app.clickCounter=0
    app.mixCounter=0
    app.generalCounter=0
    #FULL TRACK VARIABLES:
    app.BPM=120
    app.BPMchange=False
    app.BPMinput=''
    app.keyInput="' '"
    app.keyEnter=False
    # KEY SIGNATURES
    app.CMaj={6: 'C3', 5: 'D3', 4: 'E3', 3: 'F3', 2: 'G3', 1: 'A3', 0: 'B3'}
    app.GMaj={3: 'C4', 2: 'D4', 1: 'E4', 0: 'F#4', 6: 'G3', 5: 'A3', 4: 'B3'}
    app.DMaj={0: 'C#4', 6: 'D3', 5: 'E3', 4: 'F#3', 3: 'G3', 2: 'A3', 1: 'B3'}
    app.AMaj={4: 'C#4', 3: 'D4', 2: 'E4', 1: 'F#4', 0: 'G#4', 6: 'A3', 5: 'B3'}
    app.EMaj={1: 'C#4', 0: 'D#4', 6: 'E3', 5: 'F#3', 4: 'G#3', 3: 'A3', 2: 'B3'}
    app.BMaj={5: 'C#4', 4: 'D#4', 3: 'E4', 2: 'F#4', 1: 'G#4', 0: 'A#4', 6: 'B3'}
    app.FMaj={2: 'C4', 1: 'D4', 0: 'E4', 6: 'F3', 5: 'G3', 4: 'A3', 3: 'Bb3'}
    app.BbMaj={5: 'C4', 4: 'D4', 3: 'Eb4', 2: 'F4', 1: 'G4', 0: 'A4', 6: 'Bb3'}
    app.EbMaj={1: 'C4', 0: 'D4', 6: 'Eb3', 5: 'F3', 4: 'G3', 3: 'Ab3', 2: 'Bb3'}
    app.AbMaj={4: 'C4', 3: 'Db4', 2: 'Eb4', 1: 'F4', 0: 'G4', 6: 'Ab3', 5: 'Bb3'}
    app.DbMaj={0: 'C4', 6: 'Db3', 5: 'Eb3', 4: 'F3', 3: 'Gb3', 2: 'Ab3', 1: 'Bb3'}
    app.GbMaj={3: 'C4', 2: 'Db4', 1: 'Eb4', 0: 'F4', 6: 'Gb3', 5: 'Ab3', 4: 'Bb3'}
    app.keysDict={'C': app.CMaj, 'G': app.GMaj, 'D': app.DMaj, 'A': app.AMaj,
                 'B': app.BMaj, 'F': app.FMaj, 'Bb': app.BbMaj, 'Eb': app.EbMaj,
                 'Ab': app.AbMaj, 'Db': app.DbMaj, 'Gb': app.GbMaj, 'A#': app.BbMaj,
                 'D#': app.EbMaj, 'G#': app.AbMaj, 'C#': app.DbMaj, 'F#': app.GbMaj}
    app.meter='4/4'
    app.sampleRate=44100.0
    #BACKGROUND:
    app.POPSbkg = Image.open('image assets/isid POPs! BACKGROUND.png')
    app.POPSbkg = CMUImage(app.POPSbkg)
    #LOGO FRAME:
    app.POPSlogo = Image.open('image assets/isid POPs! LOGO frame.png')
    app.POPSlogo = CMUImage(app.POPSlogo)
    #SECTIONS:
    A = SECTION()
    B = SECTION()
    C = SECTION()
    D = SECTION()
    app.sectionList = [A, B, C, B, C, D]
    app.sectionNextIDindex=4
    app.currSection=0
    app.sectionDeleteCheck=False
    app.sectionDeleteCheckList=[]
    app.sectionDeleteSuccess=False
    app.deleteCounter=0
    app.startSectDrag=False
    app.draggedSection=app.currSection
    #ICONS:
        #(Note: SECTION ADD is built into logo frame)
    # MODULE ADD
    moduleAddImage = Image.open('image assets/isid POPs! ADD MODULE.png')
    app.MODULEadd = ICON(CMUImage(moduleAddImage), 900, 250, 59, 103)
    # PLAY/STOP
    playStopImage = Image.open('image assets/isid POPs! PLAY STOP.png')
    app.PLAYstop = ICON(CMUImage(playStopImage), 243, 557, 289/2, 68/2)
    app.PLAYstopHighlightImage = Image.open('image assets/isid POPs! PLAY STOP highlight.png')
    app.PLAYstop.highlight = CMUImage(app.PLAYstopHighlightImage)
    # BOUNCE
    bounceImage = Image.open('image assets/isid POPs! BOUNCE.png')
    app.BOUNCE = ICON(CMUImage(bounceImage), 80, 557, 220/2, 61/2)
    app.BOUNCEhighlightImage = Image.open('image assets/isid POPs! BOUNCE highlight.png')
    app.BOUNCE.highlight = CMUImage(app.BOUNCEhighlightImage)
    # BPM + SECTION BARS
    barsbpmImage = Image.open('image assets/isid POPs! BARS BPM.png')
    app.BARSBPM = ICON(CMUImage(barsbpmImage), 874, 610, 228/2, 273/2, True)
    # ICON LIST
    app.iconList=[app.MODULEadd, app.PLAYstop, app.BOUNCE, app.BARSBPM]
    #MODULES:
    app.showModID=True
    app.selectedModule=None
    app.showingMix=False
    app.menuPullCheck=False
    app.menuPullCheckList=[]
    app.lastClickedMod=None
    # SAMPLE
    sampleImage = Image.open('image assets/isid POPs! SAMPLE.png')
    app.SAMPLEimage = CMUImage(sampleImage)
    sampleImageHighlight = Image.open('image assets/isid POPs! SAMPLE highlight.png')
    app.SAMPLEimageHighlight = CMUImage(sampleImageHighlight)
    app.SAMPLEimageWidth=340/2
    app.SAMPLEimageHeight=244/2
    # SYNTH
    synthImage = Image.open('image assets/isid POPs! SYNTH.png')
    app.SYNTHimage = CMUImage(synthImage)
    synthImageHighlight = Image.open('image assets/isid POPs! SYNTH highlight.png')
    app.SYNTHimageHighlight = CMUImage(synthImageHighlight)
    app.SYNTHimageWidth=340/2
    app.SYNTHimageHeight=244/2
    #MENUS:
    app.fileInput=''
    app.showingMenu=False
    # MIDI (actually an ICON object but used for in Menus)
    midiImage = Image.open('image assets/isid POPs! MIDI.png')
    app.MIDIimage =CMUImage(midiImage)
    midiSelectedImage = Image.open('image assets/isid POPs! MIDI selected.png')
    app.MIDIselectedImage =CMUImage(midiSelectedImage)
    app.selectedMIDI=None
    # SAMPLE
    sampleMenuImage = Image.open('image assets/isid POPs! SAMPLE menu default.png')
    app.SAMPLEMENUimage = CMUImage(sampleMenuImage)
    sampleMenuFullPlayImage=Image.open('image assets/isid POPs! SAMPLE menu fullplay.png')
    app.SAMPLEMENUimageFullPlay = CMUImage(sampleMenuFullPlayImage)
    sampleMenuRetriggerImage=Image.open('image assets/isid POPs! SAMPLE menu retrigger.png')
    app.SAMPLEMENUimageRetrig=CMUImage(sampleMenuRetriggerImage)
    app.SAMPLEMENUimageWidth = 1920/2
    app.SAMPLEMENUimageHeight = 1008/2
    # SYNTH
    synthMenuImage = Image.open('image assets/isid POPs! SYNTH menu default.png')
    app.SYNTHMENUimage = CMUImage(synthMenuImage)
    synthMenuSineImage=Image.open('image assets/isid POPs! SYNTH menu sine.png')
    app.SYNTHMENUimageSine = CMUImage(synthMenuSineImage)
    synthMenuSawImage=Image.open('image assets/isid POPs! SYNTH menu saw.png')
    app.SYNTHMENUimageSaw = CMUImage(synthMenuSawImage)
    synthMenuSquareImage=Image.open('image assets/isid POPs! SYNTH menu square.png')
    app.SYNTHMENUimageSquare = CMUImage(synthMenuSquareImage)
    app.SYNTHMENUimageWidth = 1920/2
    app.SYNTHMENUimageHeight = 1440/2
    app.notesSemitones={'C': -9, 'C#': -8, 'Db': -8, 'D': -7, 'D#': -6,
                  'Eb': -6, 'E': -5, 'F': -4,'F#': -3, 'Gb': -3,
                  'G': -2, 'G#': -1, 'Ab': -1, 'A': 0, 'A#': 1,
                  'Bb': 1, 'B': 2}
    # Note: Defaulting C Major
    app.notes={6: 'C3', 5: 'D3', 4: 'E3', 3: 'F3', 2: 'G3', 1: 'A3', 0: 'B3'}
###########################################################
#DRAWING GRAPHICS:
def redrawAll(app):
    #BACKGROUND
    drawImage(app.POPSbkg, app.width/2, app.height/2, align='center',
              width=app.width, height=app.height)
    #SECTION BARS
    sectionNum=len(app.sectionList)
    barWidth = (app.width-(app.width*(48/960)))/sectionNum
    for bar in range(sectionNum):
        if bar == app.currSection:
            if app.sectionDeleteSuccess:
            # DELETED SECTION TURNS RED
                color='red'
            else:
            # CURRENT SECTION IS PINK
                color='pink'
        elif app.draggedSection != app.currSection and bar==app.draggedSection:
            # DRAGGED SECTION IS LIGHT BLUE
            color=rgb(0, 255, 255)
        else:
            # 'ODD' SECTIONS ARE GREEN
            # 'EVEN' SECTION ARE ORANGE
            section = app.sectionList[bar]
            color=rgb(4, 202, 74) if section.IDnum%2==0 else 'orange'
        drawRect(0+barWidth*bar, 0, barWidth, app.height*(48/720),
                 fill=color,border='brown')
        # SHOWING SECTION IDs
        barCenter = 0+barWidth*bar + (barWidth/2)
        drawLabel(f'{app.sectionList[bar]}', barCenter, app.height*(24/720),
                  size=int(18*(app.width/960)), border=rgb(180,95,6), borderWidth=0.5,
                    fill=rgb(180,95,6), italic=True, align='center', font='montserrat')
    #LOGO
    drawImage(app.POPSlogo, app.width/2, app.height/2, align='center',
              width=app.width, height=app.height)
    #KEY SIGNATURE ENTER
    if app.keyEnter==True:
        drawLabel(f'{app.keyInput}', app.width/2, app.height/2,
                  size=int(50*(app.width/960)), border=rgb(180,95,6), borderWidth=2,
                    fill=rgb(255, 213, 0), bold=True, align='center', font='montserrat')
    #ICONS/MISC BUTTONS
    for icon in app.iconList:
        drawImage(icon.image, app.width/(960/icon.x), app.height/(720/icon.y),
                  align='center', width=app.width/(960/icon.imageWidth),
                  height=app.height/(720/icon.imageHeight))
        if icon.showHighlight:
            drawImage(icon.highlight, app.width/(960/icon.x), app.height/(720/icon.y),
                    align='center', width=app.width/(960/icon.imageWidth),
                    height=app.height/(720/icon.imageHeight))
        #only Labels for BARS/BPM right now
        if icon.label==True:
            currSection=app.sectionList[app.currSection]
            #BARS LABEL
            bars=currSection.bars
            labelX=app.width/(960/icon.x) - app.width/(960/34)
            labelY=app.height/(720/icon.y) - app.height/(720/33.5)
            drawLabel(f'{bars}', labelX, labelY,
                  size=int(20*(app.width/960)), border=rgb(14,255,88), borderWidth=0.5,
                    fill=rgb(14,255,88), bold=True, align='left', font='montserrat')
            #BPM LABEL
            labelX=app.width/(960/icon.x) - app.width/(960/19)
            labelY=app.height/(720/icon.y) + app.height/(720/20)
            if app.BPMinput!='':
                bpm=app.BPMinput
            else: bpm = app.BPM
            drawLabel(f'{bpm}', labelX, labelY,
                  size=int(21*(app.width/960)), border=rgb(255,196,225), borderWidth=0.5,
                    fill=rgb(255,196,225), bold=True, align='left', font='montserrat')
    #MODULES:
    currSection=app.sectionList[app.currSection]
    #DRAWING MODULES
    for module in currSection.modulesList:
        drawImage(module.image, app.width/(960/module.x), app.height/(720/module.y),
                  align='center', width=app.width/(960/module.imageWidth),
                  height=app.height/(720/module.imageHeight))
        if app.selectedModule==module:
            drawImage(module.highlight, app.width/(960/module.x), app.height/(720/module.y),
                    align='center', width=app.width/(960/module.imageWidth),
                    height=app.height/(720/module.imageHeight))
        # SHOWING MODULE IDs
        labelX=(module.x)-(module.imageWidth)/3
        labelY=(module.y)-(module.imageHeight)/3.7
        if module==app.selectedModule and app.showingMix==True:
            labelColor=rgb(255, 213, 0) #yellow
            drawLabel(f'{module.mix}',
                      labelX, labelY, size=int(18*(app.width/960)),
                      border=labelColor, borderWidth=0.5, fill=labelColor, bold=True,
                      align='center', font='montserrat')
        elif app.showModID==True:
            if app.selectedModule == module:
                labelColor=rgb(0, 255, 0) #green
            elif module.type=="SAMPLE":
                labelColor=rgb(0, 255, 255) #cyan
            else:
                labelColor=rgb(255, 171, 0) #orange
            drawLabel(f'{module.ID}',
                      labelX, labelY, size=int(18*(app.width/960)),
                      border=labelColor, borderWidth=0.5, fill=labelColor, bold=True,
                      align='center', font='montserrat')
        #DRAWING MENU
        if module.menu.showMenu==True:
            drawImage(module.menu.image, app.width/(960/module.menu.x), app.height/(720/module.menu.y),
                    align='center', width=app.width/(1280/module.menu.imageWidth),
                    height=app.height/(960/module.menu.imageHeight))
            # SHOWING MENU IDs
            labelX=(module.menu.x)-(app.width/(1280/module.menu.imageWidth))/3
            labelY=(module.menu.y)- (app.height/(960/module.menu.imageHeight))/2.3
            drawLabel(f'Module: {module.ID}', labelX, labelY, size=int(18*(app.width/960)),
                      border='white', borderWidth=0.5, fill='white', bold=True,
                      align='center', font='montserrat')
            # SHOWING SAMPLE FILE
            if module.type=='SAMPLE':
                sampleLabelX=(module.menu.x)+(app.width/(1280/module.menu.imageWidth))/3
                sampleLabelY=(module.menu.y)+(app.height/(960/module.menu.imageHeight))/3
                drawLabel(f'{app.fileInput} {module.menu.sample}', sampleLabelX,
                        sampleLabelY, size=int(18*(app.width/960)),
                        border='white', borderWidth=0.5, fill='white', bold=True,
                        align='center', font='montserrat')
            # SHOWING SYNTH NOTES
            if module.type=='SYNTH':
                menu=module.menu
                menuWidth = app.width/(1280/menu.imageWidth)
                menuHeight = app.height/(960/menu.imageHeight)
                topBound = math.ceil(app.height/(720/menu.y) + menuHeight*(48/1440))
                botBound = math.ceil(app.height/(720/menu.y) + menuHeight/2)
                rowHeight=int(menu.imageHeight/(960/48))
                labelX = app.width/(960/menu.x) - menuWidth*(672/1920)
                color=rgb(255, 171, 0) #yellowish
                noteIndex=-1
                for rowTop in range(topBound, botBound, rowHeight):
                    noteIndex+=1
                    labelY = rowTop + rowHeight/2
                    note=app.notes[noteIndex]
                    drawLabel(f'{note}', labelX, labelY, size=int(18*(app.width/960)),
                      border=color, borderWidth=0.5, fill=color, bold=True,
                      align='center', font='montserrat')
            # DRAWING MIDI
            if module.type=='SAMPLE':
                for midi in module.menu.MIDIlist:
                    if midi.index==app.selectedMIDI:
                        color=midi.selectedImage
                    else: color=midi.image
                    MIDIwidth=module.menu.imageWidth/(1280/midi.imageWidth)
                    MIDIheight=module.menu.imageHeight/(720/midi.imageHeight)
                    MIDIwidth *= midi.noteType * 8
                    drawImage(color, app.width/(960/midi.x), app.height/(720/midi.y),
                        align='left-top', width=MIDIwidth, height=MIDIheight)
            elif module.type=='SYNTH':
                for midiList in module.menu.MIDIlistList:
                    for midi in midiList:
                        if midi.index==app.selectedMIDI:
                            color=midi.selectedImage
                        else: color=midi.image
                        MIDIwidth=module.menu.imageWidth/(1280/midi.imageWidth)
                        MIDIheight=module.menu.imageHeight/(960/midi.imageHeight)
                        MIDIwidth *= midi.noteType * 8
                        drawImage(color, app.width/(960/midi.x), app.height/(720/midi.y),
                            align='left-top', width=MIDIwidth, height=MIDIheight)
#######################################################
#SECTION HELPERS:
#BOUND CHECK (for ICONS, MODULES, and MENUS)
def inBounds(app, icon, x, y):
    if isinstance(icon, ICON) or isinstance(icon, MODULE):
        scaleWidth=960
        scaleHeight=720
    elif isinstance(icon, MENU):
        scaleWidth=1280
        scaleHeight=960
    else: return False
    imageWidth = app.width/(scaleWidth/icon.imageWidth)
    imageHeight = app.height/(scaleHeight/icon.imageHeight)
    rightBound = app.width/(960/icon.x) + imageWidth/2
    leftBound = app.width/(960/icon.x) - imageWidth/2
    topBound = app.height/(720/icon.y) - imageHeight/2
    botBound = app.height/(720/icon.y) + imageHeight/2
    return (x <= rightBound) and (x >= leftBound) and\
        (y >= topBound) and (y <= botBound)
#CREATING SECTIONS
def createSection(app):
    app.sectionList.append(SECTION()) 
#CHANGING CURRENT SECTION
def changeSections(app, mouseX):
    sectionNum=len(app.sectionList)
    barWidth = (app.width-(app.width*(48/960)))/sectionNum
    # BOUND CHECKING MOUSEX POSITION TO CHANGE SECTIONS ACCORDINGLY
    for bar in range(sectionNum):
        barBoundLeft=0+barWidth*bar
        barBoundRight=barBoundLeft+barWidth
        if mouseX >= barBoundLeft and mouseX <= barBoundRight:
            app.currSection = bar
#DELETING SECTIONS
def deleteSection(app):
    sectionsNum = len(app.sectionList)
    # If Current Section is not the last section, pop without reassigning new
    # Current Section.
    if sectionsNum-1 > app.currSection:
        app.draggedSection=app.currSection
        app.sectionList.pop(app.currSection)
    else:
        # If Current Section is the last, reassign Current Section to the
        # section before and pop the new Current Section's index + 1.
        app.currSection-=1
        app.draggedSection=app.currSection
        app.sectionList.pop(app.currSection+1)
    # REINITIALIZING DELETE TOOLS
    app.sectionDeleteCheck==False
    app.sectionDeleteCheckList=[]
    app.clickCounter=0
#ASSIGNING DRAGGED SECTION (so it turns blue)
def setSwitchColor(app, mouseX):
    # BOUND CHECKING MOUSEX AND REASSIGNING DRAGGED SECTION ACCORDINGLY
    sectionNum=len(app.sectionList)
    barWidth = (app.width-(app.width*(48/960)))/sectionNum
    for bar in range(sectionNum):
        barBoundLeft=0+barWidth*bar
        barBoundRight=barBoundLeft+barWidth
        if mouseX >= barBoundLeft and mouseX <= barBoundRight:
            app.draggedSection = bar
#MOVING SECTION POSITION
def moveSection(app):
    currentSection = app.sectionList.pop(app.currSection)
    app.sectionList.insert(app.draggedSection, currentSection)
    app.currSection=app.draggedSection
#DUPLICATING ALIASED SECTIONS
def duplicateSection(app):
    dupSection=app.sectionList[app.currSection]
    app.sectionList.insert(app.currSection+1, dupSection)
###########################################################
#MODULE HELPERS:
#CREATING MODULES
def addModule(app, mouseY):
    # RANDOM MODULE PLACEMENT
    x = random.randint(app.width//6, 4*(app.width//6))
    y = random.randint((app.height//6), 4*(app.height//6))
    # BOUND CHECKING MOUSEY FOR SAMPLE OR SYNTH MODULE ADDING
    if mouseY < app.MODULEadd.y:
        currSection=app.sectionList[app.currSection]
        currSection.modulesList.append(MODULE(app, 'SAMPLE', x, y))
    else:
        currSection=app.sectionList[app.currSection]
        currSection.modulesList.append(MODULE(app, 'SYNTH', x, y))
#REORDERING MODULES (for bringing Selected Module to front)
def reorderModules(currSection, module):
    currSection.modulesList.remove(module)
    currSection.modulesList.append(module)
#DELETING MODULES
def deleteModule(app):
    currSection=app.sectionList[app.currSection]
    modList=currSection.modulesList
    modList.remove(app.selectedModule)
    app.selectedModule=None
###########################################################
#MENU HELPERS:
#BOUND CHECK FOR MENU DRAGGING OR CLOSE
def inMenuTopBar(app, menu, mouseX, mouseY):
    imageWidth = app.width/(1280/menu.imageWidth)
    imageHeight = app.height/(960/menu.imageHeight)
    rightBound = app.width/(960/menu.x) + imageWidth/2
    leftBound = app.width/(960/menu.x) - imageWidth/2
    topBound = app.height/(720/menu.y) - imageHeight/2
    botBound = app.height/(720/menu.y) - imageHeight*(576/1440)
    # CLOSE COMMAND (if in top left corner)
    if (mouseX >= leftBound) and (mouseX<=leftBound+(imageWidth*(144/1440)))and\
        (mouseY >= topBound) and (mouseY <= botBound):
        return 'close'
    # DRAG COMMAND
    else:
        return (mouseX <= rightBound) and (mouseX >= leftBound) and\
            (mouseY >= topBound) and (mouseY <= botBound)
#SEQUENCER BOUNDS CHECK
def inBoundsSequencer(app, menu, mouseX, mouseY):
    imageWidth = app.width/(1280/menu.imageWidth)
    imageHeight = app.height/(960/menu.imageHeight)
    # SAMPLE SEQUENCER
    if app.selectedModule.type=='SAMPLE':
        rightBound = app.width/(960/menu.x) + imageWidth*(768/1920)
        leftBound = app.width/(960/menu.x) - imageWidth*(768/1920)
        topBound = app.height/(720/menu.y) + imageHeight*(24/1008)
        botBound = app.height/(720/menu.y) + imageHeight*(120/1008)
        return (mouseX <= rightBound) and (mouseX >= leftBound) and\
            (mouseY >= topBound) and (mouseY <= botBound)
    # SYNTH SEQUENCER
    elif app.selectedModule.type=='SYNTH':
        rightBound = app.width/(960/menu.x) + imageWidth/2
        leftBound = app.width/(960/menu.x) - imageWidth*(576/1920)
        topBound = app.height/(720/menu.y) + imageHeight*(48/1440)
        botBound = app.height/(720/menu.y) + imageHeight/2
        return (mouseX <= rightBound) and (mouseX >= leftBound) and\
            (mouseY >= topBound) and (mouseY <= botBound)
#SYNTH CHANGING OCTAVES
def inBoundsOctaveChangeCheck(app, menu, mouseX, mouseY):
    imageWidth = app.width/(1280/menu.imageWidth)
    imageHeight = app.height/(960/menu.imageHeight)
    rightBound = app.width/(960/menu.x) - imageWidth*(768/1920)
    leftBound = app.width/(960/menu.x) - imageWidth*(864/1920)
    topBound = app.height/(720/menu.y) + imageHeight*(48/1440)
    middle = app.height/(720/menu.y) + imageHeight*(144/1440)
    botBound = app.height/(720/menu.y) + imageHeight*(240/1440)
    #BOUNDS CHECK
    if (mouseX <= rightBound) and (mouseX >= leftBound):
        #OCTAVE CHANGE UP
        if (mouseY >= topBound) and (mouseY <= middle):
            for noteKey in app.notes:
                note = app.notes[noteKey]
                octave=int(note[-1])
                octave=str(octave+1)
                note = note[0:-1]+octave
                app.notes[noteKey]=note
        #OCTAVE CHANGE DOWN
        elif (mouseY >= middle) and (mouseY <= botBound):
            for noteKey in app.notes:
                note = app.notes[noteKey]
                octave=int(note[-1])
                if octave!=0:
                    octave=str(octave-1)
                    note = note[0:-1]+octave
                    app.notes[noteKey]=note
#SEQUENCER BOUNDS CHECK --> SAMPLE PATTERN WRITING & MIDI SELECT
def writePatternSequence(app, menu, mouseX):
    imageWidth = app.width/(1280/menu.imageWidth)
    imageHeight = app.height/(960/menu.imageHeight)
    rightBound = int(app.width/(960/menu.x) + imageWidth*(768/1920))
    leftBound = int(app.width/(960/menu.x) - imageWidth*(768/1920))
    topBound = app.height/(720/menu.y) + imageHeight*(24/1008)
    tickDistance=int(menu.imageWidth/(1280/48))
    # WRITE N0TE TO PATTERN FRAMEWORK
    index=0
    for tickL in range(leftBound, rightBound, tickDistance):
        tickR=tickL+tickDistance
        if mouseX>=tickL and mouseX<=tickR:
            patternFrame=menu.patternFramework
            # Map trigger point
            if patternFrame[index][1] == False:
                # Defaulting 1/4 note
                if index+1 < len(patternFrame) and\
                    patternFrame[index+1][1]==False:
                        patternFrame[index]=[1/8, True, 'trigger']
                        patternFrame[index+1]=[1/8, True, 'sustain']
                        menu.MIDIlist.append(MIDI(app, tickL, topBound+2, index, 1/4))
                        if menu.sample!='' and menu.sample!='samples/.wav':
                            playSound(app, menu.sample)
                else:
                    # Else 1/8 note
                    patternFrame[index]=[1/8, True, 'trigger']
                    menu.MIDIlist.append(MIDI(app, tickL, topBound+2, index, 1/8))
                    if menu.sample!='' and menu.sample!='samples/.wav':
                            playSound(app, menu.sample)
            else:
    # MIDI SELECT
                app.selectedMIDI=index
        index+=1
    menu.patternRendered = renderPattern(menu.patternFramework)
#RENDERING PATTERN FROM FRAMEWORK
# Note: The pattern framework indicates triggers and sustains at every 1/8
# note subdivision. Rendering combines the triggers and sustains accordingly.
# (i.e. [[1/8, True, trigger],[1/8, True, sustain]] --> [1/4, True])
def renderPattern(patternFrame):
    inSustain=None
    sustainDuration=None
    patternRendered=[]
    for tickIndex in range(len(patternFrame)):
        tick=patternFrame[tickIndex]
        if tick[1]==True and not inSustain:
                inSustain=True
                sustainDuration=1/8
        elif tick[1]==True and inSustain:
            if tick[2]=='trigger':
                patternRendered.append([sustainDuration, True])
                sustainDuration=1/8
            else:
                sustainDuration+=1/8
        else:
            if inSustain:
                patternRendered.append([sustainDuration, True])
                inSustain=False
                sustainDuration=None
                patternRendered.append([1/8, False])
            else:
                patternRendered.append([1/8, False])
        if tickIndex+1==len(patternFrame) and inSustain:
            patternRendered.append([sustainDuration, True])
            inSustain=False
            sustainDuration=None
    return patternRendered
#PITCHED PATTERN WRITE & MIDI SELECT
def writePitchedSequence(app, menu, mouseX, mouseY):
    imageWidth = app.width/(1280/menu.imageWidth)
    imageHeight = app.height/(960/menu.imageHeight)
    rightBound = int(app.width/(960/menu.x) + imageWidth/2)
    leftBound = int(app.width/(960/menu.x) - imageWidth*(576/1920))
    topBound = int(app.height/(720/menu.y) + imageHeight*(48/1440))
    botBound = int(app.height/(720/menu.y) + imageHeight/2)
    tickDistanceH=int(menu.imageWidth/(1280/48))
    tickDistanceV=int(menu.imageHeight/(960/48))
    timeIndex=-1
    noteIndex=-1
    # Note: For the first edition of isid POPs!, SYNTH is single voice, so
    # just patternFramework1 will be used.
    patternFrame=menu.patternFramework1
    #RHYTHM
    for tickL in range(leftBound, rightBound, tickDistanceH):
        tickR=tickL+tickDistanceH
        timeIndex+=1
        noteIndex=-1
    #PITCH
        for tickT in range(topBound, botBound, tickDistanceV):
            tickB=tickT+tickDistanceV
            noteIndex+=1
            #BOUND CHECK
            if mouseX>=tickL and mouseX<=tickR and\
                  mouseY>=tickT and mouseY<=tickB:
        # WRITE N0TE TO FRAMEWORK
                # Map trigger if empty
                if patternFrame[timeIndex][1] == False:
                    # GET PITCH
                    note=app.notes[noteIndex]
                    # DEFAULT A QUARTER N0TE
                    if timeIndex+1 < len(patternFrame) and\
                        patternFrame[timeIndex+1][1]==False:
                            patternFrame[timeIndex]=[1/8, True, 'trigger', note]
                            patternFrame[timeIndex+1]=[1/8, True, 'sustain', note]
                            menu.MIDIlist1.append(MIDI(app, tickL, tickT+2, timeIndex, 1/4))
                    else:
                        patternFrame[timeIndex]=[1/8, True, 'trigger', note]
                        menu.MIDIlist1.append(MIDI(app, tickL, tickT+2, timeIndex, 1/8))
        # MIDI SELECT
                else:
                    app.selectedMIDI=timeIndex
    menu.patternRendered = renderPitchPattern(menu.patternFramework1)
#RENDERING PITCH PATTERN FROM FRAMEWORK
# Note: See pattern render note
def renderPitchPattern(patternFrame):
    inSustain=None
    sustainDuration=None
    sustainedNote=None
    patternRendered=[]
    for tickIndex in range(len(patternFrame)):
        tick=patternFrame[tickIndex]
        if tick[1]==True and not inSustain:
                inSustain=True
                sustainDuration=1/8
                sustainedNote=tick[3]
        elif tick[1]==True and inSustain:
            if tick[2]=='trigger':
                patternRendered.append([sustainDuration, True, sustainedNote])
                sustainedNote = tick[3]
                sustainDuration=1/8
            else:
                sustainDuration+=1/8
        else:
            if inSustain:
                patternRendered.append([sustainDuration, True, sustainedNote])
                inSustain=False
                sustainDuration=None
                sustainedNote=None
                patternRendered.append([1/8, False, None])
            else:
                patternRendered.append([1/8, False, None])
        if tickIndex+1==len(patternFrame) and inSustain:
            patternRendered.append([sustainDuration, True, sustainedNote])
            inSustain=False
            sustainDuration=None
            sustainedNote=None
    return patternRendered
###########################################################
#EVENTS:
# MOUSE PRESS EVENTS:
def onMousePress(app, mouseX, mouseY):
    #BPM CHANGE
    if inBounds(app, app.BARSBPM, mouseX, mouseY):
        middle = app.height/(720/app.BARSBPM.y)
        if mouseY >= middle:
            app.BPMchange=True
    #MODULE ADD
    if inBounds(app, app.MODULEadd, mouseX, mouseY):
        addModule(app, mouseY)
    #MODULE SELECT
    currSection=app.sectionList[app.currSection]
    for module in currSection.modulesList:
        # MODULE BOUND CHECK
        if not app.showingMenu:
            if inBounds(app, module, mouseX, mouseY):
                if app.showingMix==True:
                    app.mixCounter=0
                    app.showingMix=False
                app.selectedModule = module
                # BRING MODULE TO FRONT
                reorderModules(currSection, module)
                # START DRAG
                module.startDrag = True
                app.makeupX = module.x - mouseX
                app.makeupY = module.y - mouseY
            else:
                app.selectedModule=None
        elif inBounds(app, module, mouseX, mouseY):
            if not inBounds(app, app.selectedModule.menu, mouseX, mouseY):
                app.selectedModule = module
                # BRING MODULE TO FRONT
                reorderModules(currSection, module)
                # START DRAG
                module.startDrag = True
                app.makeupX = module.x - mouseX
                app.makeupY = module.y - mouseY
    #MENU FEATURES
    if app.showingMenu:
        currMenu=app.selectedModule.menu
        # MENU REGIONS BOUND CHECKS
        topBarConsensus=inMenuTopBar(app, currMenu, mouseX, mouseY)
        # MENU CLOSE
        if topBarConsensus=='close':
            currMenu.showMenu=False
            app.showingMenu=False
        # MENU DRAG
        elif topBarConsensus==True:
            currMenu.startDrag=True
            app.makeupX = currMenu.x - mouseX
            app.makeupY = currMenu.y - mouseY
            if app.selectedModule.type=='SAMPLE':
                for midi in currMenu.MIDIlist:
                    midi.makeupX=midi.x-mouseX
                    midi.makeupY=midi.y-mouseY
            elif app.selectedModule.type=='SYNTH':
                for midiList in currMenu.MIDIlistList:
                    for midi in midiList:
                        midi.makeupX=midi.x-mouseX
                        midi.makeupY=midi.y-mouseY
        # MENU PATTERN WRITING
        if inBoundsSequencer(app, currMenu, mouseX, mouseY):
            if app.selectedModule.type=='SAMPLE':
                writePatternSequence(app, currMenu, mouseX)
            elif app.selectedModule.type=='SYNTH':
                writePitchedSequence(app, currMenu, mouseX, mouseY)
        # SYNTH MENU OCTAVE CHANGE
        if app.selectedModule.type=='SYNTH':
            inBoundsOctaveChangeCheck(app, currMenu, mouseX, mouseY)
    #SECTION ADD
    addSectLeft=app.width/(960/(960-48))
    addSectBot=app.height/(720/48)
    if (mouseX <= app.width) and (mouseX >= addSectLeft) and\
       (mouseY >= 0) and (mouseY <= addSectBot):
        createSection(app)
    #SECTIONS CHANGE
    elif (mouseY >= 0) and (mouseY <= 48): #in section bar
        changeSections(app, mouseX)
        app.startSectDrag=True
        app.draggedSection=app.currSection
        # TRIPLE-CLICK CHECK
        app.sectionDeleteCheck=True
        app.sectionDeleteCheckList.append(True)
    #PLAY/STOP SECTION TRACK
    if inBounds(app, app.PLAYstop, mouseX, mouseY) and not app.showingMenu:
        app.PLAYstop.showHighlight=True
        currSection=app.sectionList[app.currSection]
        modList = currSection.modulesList
        patternTracksAndMix={}
        patternTracksForSection=[]
        if app.meter=='4/4':
            bpm=app.BPM/4
        for module in modList:
            if module.menu.patternTrack!=None:
                patternTracksAndMix[module.menu.patternTrack] = module.mix
        #COMBINE PATTERN TRACKS
        if patternTracksAndMix!={}:
            currSection.sectionTrack = wave.open(f'sectionTrack{currSection.ID}.wav', 'w')
            sectionTrackFile = currSection.sectionTrack
            sectionTrackFile.setnchannels(2)
            sectionTrackFile.setsampwidth(2)
            sectionTrackFile.setframerate(app.sampleRate)
            for track in patternTracksAndMix:
                layer = getTrackLayer(track, patternTracksAndMix)
                patternTracksForSection.append(layer)
            duration=60*currSection.bars / bpm
            #test volume
            sectionAmps = genSectionAmps(patternTracksForSection, duration)
            #maxing volume
            ceiling = findCeiling(sectionAmps)
            scale = 1 + (32767-ceiling)/ceiling
            sectionAdjustedList = genDefaultAmpList(sectionAmps, scale)
            #generate track
            genSectionTrack(sectionTrackFile, sectionAdjustedList, duration)
            sectionTrackFile.close()
            playSound(app, f'sectionTrack{currSection.ID}.wav')
    #FULL TRACK BOUNCE
    if inBounds(app, app.BOUNCE, mouseX, mouseY):
        app.BOUNCE.showHighlight=True
        sectionTracksList=[]
        sectionTracksAmps=[]
        for section in app.sectionList:
            if section.sectionTrack!=None:
                sectionTracksList.append(f'sectionTrack{section.ID}.wav')
        if sectionTracksList!=[]:
            fullTrackFile = wave.open('My isid POPs! Track.wav', 'w')
            fullTrackFile.setnchannels(2)
            fullTrackFile.setsampwidth(2)
            fullTrackFile.setframerate(app.sampleRate)
            for track in sectionTracksList:
                appendAmps(sectionTracksAmps, track)
            genStitchedTrack(fullTrackFile, sectionTracksAmps)
            fullTrackFile.close()
            playSound(app,'My isid POPs! Track.wav')
#MOUSE DRAG EVENTS:
def onMouseDrag(app, mouseX, mouseY):
    #SECTION DRAG
    if app.startSectDrag:
        setSwitchColor(app, mouseX)
    currSection=app.sectionList[app.currSection]
    for module in currSection.modulesList:
    #MENU DRAG
        if module.menu.startDrag==True:
            module.menu.x = (mouseX + app.makeupX)
            module.menu.y = (mouseY + app.makeupY)
            if module.type=="SAMPLE":
                for midi in module.menu.MIDIlist:
                    midi.x = (mouseX + midi.makeupX)
                    midi.y = (mouseY + midi.makeupY)
            elif module.type=='SYNTH':
                for midiList in module.menu.MIDIlistList:
                    for midi in midiList:
                        midi.x = (mouseX + midi.makeupX)
                        midi.y = (mouseY + midi.makeupY)
    #MODULE DRAG
        elif module.startDrag == True:
            module.x = (mouseX + app.makeupX)
            module.y = (mouseY + app.makeupY)
#MOUSE RELEASE EVENTS:
def onMouseRelease(app, mouseX, mouseY):
    #SECTION DRAG END AND REORDERING
    if app.draggedSection != app.currSection:
        moveSection(app)
    app.draggedSection=app.currSection
    app.startSectDrag=False
    #TURNING OFF HIGHLIGHTS FOR MISC ICONS
    for icon in app.iconList:
        if icon.showHighlight==True:
            icon.showHighlight=False
    #MODULE/MENU DRAG END & MENU CLOSE
    currSection=app.sectionList[app.currSection]
    for module in currSection.modulesList:
        # MODULE
        if module.startDrag == True:
            module.startDrag = False
        # MENU DRAG
        if module.menu.startDrag==True:
            module.menu.startDrag = False
        # MENU CLOSE
        if module.menu.showMenu==True and module != app.selectedModule:
            module.menu.showMenu=False
            app.selectedModule.menu.showMenu=True
    app.makeupX=None
    app.makeupY=None
#KEY PRESS EVENTS:
def onKeyPress(app, key):
    #KEY SIGNATURE ENTER
    validKeys=string.ascii_letters + 'enter' + 'backspace' + '#'
    if key in validKeys and app.selectedModule==None and app.keyEnter==True:
        if key=='backspace' and len(app.keyInput)>0:
            app.keyInput=app.keyInput[0:-1]
        elif key=='backspace' and len(app.keyInput)<=0:
            pass
        elif key=='enter':
            if app.keyInput in app.keysDict:
                app.notes=app.keysDict[app.keyInput]
                app.keyInput="' '"
                app.keyEnter=False
            else:
                app.keyInput="' '"
                app.keyEnter=False
        else:
            if app.keyInput=="' '":
                app.keyInput=''
            app.keyInput+=key
    elif key=='k' and app.selectedModule==None:
        app.keyEnter=True
    #BPM CHANGE
    digits=string.digits + 'enter' + 'backspace'
    if key in digits and key!='space' and app.BPMchange==True:
        if key=='backspace' and len(app.BPMinput)>0:
                app.BPMinput=app.BPMinput[0:-1]
        elif key=='backspace' and len(app.BPMinput)<=0:
            pass
        elif key=='enter':
            if app.BPMinput!='':
                app.BPM=int(app.BPMinput)
                app.BPMinput=''
            app.BPMchange=False
        else:
            app.BPMinput+=key
    #SECTION DUPLICATE
    if key=='d' and app.selectedModule == None and app.keyEnter==False:
        duplicateSection(app)
    #MODULE DELETE
    elif key=='backspace' and app.selectedModule != None and\
        not app.selectedModule.menu.showMenu:
            deleteModule(app)
    #MENU SHOW
    elif key=='enter' and app.selectedModule != None:
        app.selectedModule.menu.showMenu=True
        app.showingMenu=True
        app.selectedModule.menu.x=app.width/2
        app.selectedModule.menu.y=app.height/2
        if app.selectedModule.type=='SAMPLE':
            midiList=app.selectedModule.menu.MIDIlist
            for midi in midiList:
                midi.x = midi.MIDIdefaultX
                midi.y = midi.MIDIdefaultY
        elif app.selectedModule.type=='SYNTH':
            midiListList=app.selectedModule.menu.MIDIlistList
            for midiList in midiListList:
                for midi in midiList:
                    midi.x = midi.MIDIdefaultX
                    midi.y = midi.MIDIdefaultY
    #MODULE/MENU SAMPLE INPUT
    validKeys=string.printable + 'enter' + 'backspace' + 'space'
    if key in validKeys and app.showingMenu and app.selectedModule.type=='SAMPLE':
        currMenu=app.selectedModule.menu
        # SAMPLE INPUT
        if app.selectedModule.type=='SAMPLE' and currMenu.sample=='samples/.wav':
            if key=='backspace' and len(app.fileInput)>0:
                app.fileInput=app.fileInput[0:-1]
            elif key=='backspace' and len(app.fileInput)<=0:
                pass
            elif key=='enter':
                filestring = app.fileInput
                currMenu.sample='samples/'+filestring+'.wav'
                app.fileInput=''
            elif key=='space':
                app.fileInput+=' '
            else:
                app.fileInput+=key
# SAMPLE PLAYBACK
        else:
            if key=='1':
                if app.selectedModule.type=='SAMPLE' and app.selectedModule!=None:
                    sample=currMenu.sample
                    playSound(app, sample)
# SAMPLE PATTERN PLAYBACK
            if key=='space':
                if app.meter == '4/4':
                    bpm = app.BPM/4
                currMenu.patternTrack = f'pattern{app.selectedModule.ID}.wav'
                patternFile=currMenu.patternTrack
                patternSequence=currMenu.patternRendered
                sampleFile=currMenu.sample
                patternTrackFile = wave.open(patternFile, 'w')
                patternTrackFile.setnchannels(2)
                patternTrackFile.setsampwidth(2)
                patternTrackFile.setframerate(app.sampleRate)
                ampList = getAmpList(sampleFile)
                for note in patternSequence:
                    noteType=note[0]
                    trigger=note[1]
                    duration = noteType*60/bpm #relating beats to seconds
                    if trigger:
                            genBeatNote(patternTrackFile, ampList, duration)
                    else:
                        genRest(patternTrackFile, duration)
                patternTrackFile.close()
                patternTrack = currMenu.patternTrack
                playSound(app, patternTrack)
# SYNTH PATTERN PLAYBACK
    if key=='space' and app.showingMenu and app.selectedModule.type=='SYNTH':
        currMenu=app.selectedModule.menu
        if app.meter == '4/4':
            bpm = app.BPM/4
        currMenu.patternTrack = f'pattern{app.selectedModule.ID}.wav'
        patternFile=currMenu.patternTrack
        patternSequence=currMenu.patternRendered
        patternTrackFile = wave.open(patternFile, 'w')
        patternTrackFile.setnchannels(2)
        patternTrackFile.setsampwidth(2)
        patternTrackFile.setframerate(app.sampleRate)
        for note in patternSequence:
            noteType=note[0]
            trigger=note[1]
            pitch=note[2]
            duration = noteType*60/bpm
            if trigger:
                    genPitchedNote(app, patternTrackFile, pitch, duration)
            else:
                genRest(patternTrackFile, duration)
        patternTrackFile.close()
        patternTrack = currMenu.patternTrack
        playSound(app, patternTrack)
    if key=='up' and app.selectedModule!=None and not app.selectedModule.menu.showMenu:
        app.selectedModule.mix+=1
        app.mixCounter=0
        app.showingMix=True
    elif key=='down' and app.selectedModule!=None and not app.selectedModule.menu.showMenu:
        if app.selectedModule.mix != 0:
            app.selectedModule.mix-=1
            app.mixCounter=0
            app.showingMix=True
    # MIDI/N0TE LENGTHEN
    elif (key=='right' or key=='up') and app.selectedMIDI != None:
        # SAMPLE MIDI
        if app.selectedModule.type=="SAMPLE":
            midiList = app.selectedModule.menu.MIDIlist
            patternFrame=app.selectedModule.menu.patternFramework
            for midi in midiList:
                if midi.index==app.selectedMIDI:
                    trigger=app.selectedMIDI
                    duration=0
                    # Getting index of the next note or rest
                    while trigger+1 < len(patternFrame) and patternFrame[trigger+1][2] == 'sustain':
                        duration += 1
                        trigger+=1
                    #CHECKING IF N0TE IS ON EDGE
                    if app.selectedMIDI+duration+1 < len(patternFrame):
                        nextNote = patternFrame[app.selectedMIDI+duration+1][1]
                        if app.selectedMIDI+1 < len(patternFrame) and nextNote!=True:
                            midi.noteType+=1/8
                            patternFrame[app.selectedMIDI+duration+1][1]=True
                            patternFrame[app.selectedMIDI+duration+1][2]='sustain'
            app.selectedModule.menu.patternRendered = renderPattern(patternFrame)
        # SYNTH MIDI
        elif app.selectedModule.type=="SYNTH":
            midiListList = app.selectedModule.menu.MIDIlistList
            patternFrameList=app.selectedModule.menu.patternFrameworkList
            for i in range(len(midiListList)):
                midiList=midiListList[i]
                patternFrame=patternFrameList[i]
                for midi in midiList:
                    if midi.index==app.selectedMIDI:
                        trigger=app.selectedMIDI
                        duration=0
                        # Getting index of the next note or rest
                        while trigger+1 < len(patternFrame) and patternFrame[trigger+1][2] == 'sustain':
                            duration += 1
                            trigger+=1
                        #CHECKING IF N0TE IS ON EDGE
                        if app.selectedMIDI+duration+1 < len(patternFrame):
                            nextNote = patternFrame[app.selectedMIDI+duration+1][1]
                            if app.selectedMIDI+1 < len(patternFrame) and nextNote!=True:
                                midi.noteType+=1/8
                                note = patternFrame[trigger][3]
                                patternFrame[app.selectedMIDI+duration+1][1]=True
                                patternFrame[app.selectedMIDI+duration+1][2]='sustain'
                                patternFrame[app.selectedMIDI+duration+1][3]=note
            #JUST ONE VOICE RIGHT NOW
            patternFrame1=app.selectedModule.menu.patternFramework1
            app.selectedModule.menu.patternRendered = renderPitchPattern(patternFrame1)
    # MIDI SHORTEN
    elif (key=='left' or key=='down') and app.selectedMIDI != None:
        # SAMPLE MIDI
        if app.selectedModule.type=="SAMPLE":
            midiList = app.selectedModule.menu.MIDIlist
            patternFrame=app.selectedModule.menu.patternFramework
            for midi in midiList:
                if midi.index==app.selectedMIDI:
                    trigger=app.selectedMIDI
                    duration=0
                    # Getting index of the next note or rest
                    while trigger+1 < len(patternFrame) and patternFrame[trigger+1][2]=='sustain':
                        duration += 1
                        trigger+=1
                    if midi.noteType!=1/8:
                        midi.noteType-=1/8
                        patternFrame[app.selectedMIDI+duration][1]=False
                        patternFrame[app.selectedMIDI+duration][2]='trigger'
                    else:
                        midiList.remove(midi)
                        patternFrame[trigger][1]=False
                        patternFrame[trigger][2]='trigger'
                        app.selectedMIDI=None
            app.selectedModule.menu.patternRendered = renderPattern(patternFrame)
        # SYNTH MIDI
        elif app.selectedModule.type=="SYNTH":
            midiListList = app.selectedModule.menu.MIDIlistList
            patternFrameList=app.selectedModule.menu.patternFrameworkList
            for i in range(len(midiListList)):
                midiList=midiListList[i]
                patternFrame=patternFrameList[i]
                for midi in midiList:
                    if midi.index==app.selectedMIDI:
                        trigger=app.selectedMIDI
                        duration=0
                        # Getting index of the next note or rest
                        while trigger+1 < len(patternFrame) and patternFrame[trigger+1][2]=='sustain':
                            duration += 1
                            trigger+=1
                        if midi.noteType!=1/8:
                            midi.noteType-=1/8
                            patternFrame[app.selectedMIDI+duration][1]=False
                            patternFrame[app.selectedMIDI+duration][2]='trigger'
                        else:
                            midiList.remove(midi)
                            patternFrame[trigger][1]=False
                            patternFrame[trigger][2]='trigger'
                            app.selectedMIDI=None
            #JUST ONE VOICE RIGHT NOW
            patternFrame1=app.selectedModule.menu.patternFramework1
            app.selectedModule.menu.patternRendered = renderPitchPattern(patternFrame1)
#######################################################
def onStep(app):
    app.generalCounter+=1
    #SECTION DELETE (TRIPLE CLICK CHECK) # (Note: change to Click+Hold?)
    if app.sectionDeleteCheck==True:
        app.clickCounter+=1
        if app.clickCounter==16:
            if len(app.sectionDeleteCheckList)>=3:
                sectionsNum = len(app.sectionList)
                if sectionsNum > 1:
                    app.sectionDeleteSuccess=True
            else: 
                app.sectionDeleteCheck==False
                app.sectionDeleteCheckList=[]
                app.clickCounter=0
    #SECTION DELETE (DELETING, RED COLOR, AND BUFFER)
    if app.sectionDeleteSuccess==True:
        app.deleteCounter+=1
        if app.deleteCounter==7:
            deleteSection(app)
            app.deleteCounter=0
            app.sectionDeleteSuccess=False
    #MODULE MIX VALUES TURNING OFF
    if app.showingMix==True:
        if app.mixCounter==0:
            app.mixCounter=app.generalCounter
        if app.generalCounter-app.mixCounter==20:
            app.showingMix=False
            app.mixCounter=0
            
#######################################################
#SOUND HELPERS:
#AMP LIST GENERATORS
def getAmpList(sample): #amp list is in bytes
   lst=[]
   sampleObj = wave.open(sample, 'r')
   numFrames = sampleObj.getnframes()
   while sampleObj.tell() < numFrames:
      frame = sampleObj.readframes(1)
      lst.append(frame)
   sampleObj.close()
   return lst
def getAmpListDecoded(sample): #amp list is in integers
   lst=[]
   sampleObj = wave.open(sample, 'r')
   numFrames = sampleObj.getnframes()
   while sampleObj.tell() < numFrames:
      frame = sampleObj.readframes(1)
      frame = struct.unpack('<hh', frame)
      lst.append(frame)
   sampleObj.close()
   return lst
#GAIN ADJUSTMENT FUNCS
def findCeiling(ampList):
   greatest=0
   for i in range(len(ampList)):
      right, left = ampList[i]
      if abs(right) > greatest:
         greatest=abs(right)
      if abs(left) > greatest:
         greatest=abs(left)
   return greatest
def genDefaultAmpList(ampList, scale):
   newAmps=[]
   for i in range(len(ampList)):
      right, left = ampList[i]
      right *= scale
      left *= scale
      newAmps.append((int(right), int(left)))
   return newAmps
def changeGain(ampList, scale):
   newAmps=[]
   for i in range(len(ampList)):
      right, left = ampList[i]
      right *= scale
      left *= scale
      newAmps.append((int(right), int(left)))
   return newAmps
#GENERATING BEAT PATTERN TRACKS
def genBeatNote(patternFile, sampleAmps, duration): #takes sampleAmps as bytes 
    for i in range(int(duration*44100.0)):
        data = sampleAmps[i]
        patternFile.writeframesraw(data)
def genRest(patternFile, duration):
    for i in range(int(duration*44100.0)*2):
        data = struct.pack('<h', 0)
        patternFile.writeframesraw(data)
#GENERATING PITCH PATTERN TRACKS
def getFreq(app, pitch):
    interval=app.notesSemitones[pitch[:len(pitch)-1]]
    octave=int(pitch[len(pitch)-1])
    semitonesfromA4 = (octave-4)*12 + (interval)
    return 440*(2**(semitonesfromA4/12)) #formula for equal temp tuning based around A4 i.e. 440Hz
def genPitchedNote(app, chordProgFile, pitch, duration):
    maxAmp=32767
    freq=getFreq(app, pitch)
    for i in range(int(duration*44100.0)*2):
        data = math.sin(math.pi*freq*i/44100.0) #sine wave sound
        #data = (freq*i/44100.0)%1  #for sawtooth sound
        #decay formula adjusted from Mike's
        decay = 5 * (10**-5) #first num decay adjust. exponent is sensivity
        data *= (1 - decay)**(i/duration)
        data = int(maxAmp*data)
        data = struct.pack('<h', data)
        chordProgFile.writeframesraw(data)
#GENERATING SECTION TRACKS
def getTrackLayer(track, patternTracksAndMix):
    trackAmpList=getAmpListDecoded(track)
    #finding gain scaling
    ceiling = findCeiling(trackAmpList)
    scale = 1 + (32767-ceiling)/ceiling
    defaultAmpList = genDefaultAmpList(trackAmpList, scale)
    #adjusting gain
    trackMix=patternTracksAndMix[track]
    trackAdjustedGain = changeGain(defaultAmpList, trackMix)
    return trackAdjustedGain
def genSectionTrack(sectionFile, sectionAmps, duration): #takes sectionAmps as tups of ints
    for i in range(int(duration*44100.0)):
        right, left = sectionAmps[i]
        dataR = struct.pack('<h', right)
        dataL = struct.pack('<h', left)
        sectionFile.writeframesraw(dataR)
        sectionFile.writeframesraw(dataL)
def genSectionAmps(patternTracksList, duration): #writes amp list as tups of ints
    amps=[]
    for i in range(int(duration*44100.0)):
        dataR=0
        dataL=0
        for inst in patternTracksList:
            if i < len(inst):
                right, left = inst[i]
                dataR += right
                dataL += left
        amps.append((dataR, dataL))
    return amps
#GENERATING FULL/STITCHED TRACKS
def appendAmps(lst, sample):
   sampleObj = wave.open(sample, 'r')
   numFrames = sampleObj.getnframes()
   while sampleObj.tell() < numFrames:
      frame = sampleObj.readframes(1)
      lst.append(frame)
   sampleObj.close()
def genStitchedTrack(patternFile, sampleAmps): # takes sampleAmps in bytes
    for i in range(len(sampleAmps)):
         data = sampleAmps[i]
         patternFile.writeframesraw(data)
#SOUND LOAD
def loadSound(relativePath):
    absolutePath = os.path.abspath(relativePath)
    url = pathlib.Path(absolutePath).as_uri()
    return Sound(url)
#SOUND PLAY
def playSound(app, file):
    app.sound = loadSound(file)
    app.sound.play(restart = True)
def main():
    runApp()
if __name__ == '__main__':
    main()