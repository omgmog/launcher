# -*- coding: utf-8 -*- 

import pygame
#import math
import subprocess

#from beeprint import pp
from libs.roundrects import aa_round_rect
#import gobject
#from wicd import misc 
## local UI import
from UI.constants import Width,Height,ICON_TYPES
from UI.page   import Page,PageSelector
from UI.label  import Label
from UI.util_funcs import midRect
from UI.keys_def   import CurKeys, IsKeyMenuOrB
from UI.scroller   import ListScroller
from UI.icon_pool  import MyIconPool
from UI.icon_item  import IconItem
from UI.multilabel import MultiLabel
from UI.lang_manager import MyLangManager
from UI.skin_manager import MySkinManager

from battery import BatteryAbstraction

class InfoPageListItem(object):
    _PosX = 0
    _PosY = 0
    _Width = 0
    _Height = 20

    _Labels = {}
    _Icons  = {}
    _Fonts  = {}

    _LinkObj = None
    
    def __init__(self):
        self._Labels = {}
        self._Icons  = {}
        self._Fonts  = {}

    def SetSmallText(self,text):
        
        l = MultiLabel()
        l.SetCanvasHWND(self._Parent._CanvasHWND)
        l.Init(text,self._Fonts["small"])
        
        self._Labels["Small"] = l

        #if self._Labels["Small"]._Width > self._Width:
        #    self._Width = self._Labels["Small"]._Width
        if self._Labels["Small"]._Height >= self._Height:
            self._Height = self._Labels["Small"]._Height+10
        
    def Init(self,text):

        #self._Fonts["normal"] = fonts["veramono12"]
        
        l = Label()
        l._PosX = 10
        l.SetCanvasHWND(self._Parent._CanvasHWND)

        l.Init(text,self._Fonts["normal"])
        self._Labels["Text"] = l
        
    def Draw(self):
        
        self._Labels["Text"]._PosY = self._PosY
        self._Labels["Text"].Draw()

        if "Small" in self._Labels:
            self._Labels["Small"]._PosX = self._Labels["Text"]._Width + 16 
            self._Labels["Small"]._PosY = self._PosY 
            self._Labels["Small"].Draw()
        
        
    

class AboutPage(Page):
    _FootMsg =  ["Nav.","","","Back",""]
    _MyList = []
    _ListFontObj = MyLangManager.TrFont("varela13")
    
    _AList = {}

    _Scrolled = 0
    
    _BGwidth = 480
    _BGheight = 272

    _DrawOnce = False
    _Scroller = None
    
    def __init__(self):
        Page.__init__(self)
        self._Icons = {}

    def Uname(self):
        
        out = {}
        out["key"]="uname"
        out["label"]= "Kernel:"
        st = subprocess.check_output(["uname","-srmo"])
        st = st.strip("\n")
        st = st.strip("\t")
        out["value"] = st
        self._AList["uname"] = out

        return
    
    def CpuMhz(self):

        try:
            with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq") as f:
                content = f.readlines()
            content = [x.strip() for x in content]
            
        except:
            print("open %s failed" % "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
            content = ["0"]
        
        mhz = int(content[0]) / 1000.0

        cpuscalemhz = {}
        cpuscalemhz["key"] = "cpuscalemhz"
        cpuscalemhz["label"] = "CPU Mhz:"
        cpuscalemhz["value"] = str(mhz)
        self._AList["cpuscalemhz"] = cpuscalemhz
        
        return 
    
    def CpuInfo(self):
        last_processor = 0
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("processor"):
                    parts = line.split(":")
                    cur_processor_number = int( parts[1].strip())
                    if cur_processor_number > last_processor:
                        last_processor = cur_processor_number
                    
                if line.startswith("model name"):
                    parts = line.split(":")
#                    print( parts[1].strip() )
                    processor = {}
                    processor["key"]="processor"
                    processor["label"] = "Processor:"
                    processor["value"] = parts[1].strip()
                    
                    self._AList["processor"] = processor
                    
                if line.startswith("cpu MHz"):
                    parts = line.split(":")
#                    print(parts[1].strip() )
                    cpumhz = {}
                    cpumhz["key"] = "cpumhz"
                    cpumhz["label"] = "CPU MHz:"
                    cpumhz["value"] = parts[1].strip()

                    self._AList["cpumhz"] = cpumhz
                if line.startswith("cpu cores"):
                    parts = line.split(":")
#                    print(parts[1].strip() )
                    cpucores = {}
                    cpucores["key"] = "cpucores"
                    cpucores["label"] = "CPU cores:"
                    cpucores["value"] = parts[1].strip()
                    self._AList["cpucores"] = cpucores
                if line.startswith("Features"):
                    parts = line.split(":")
#                    print(parts[1].strip() )
                    f_ = {}
                    f_["key"] = "features"
                    f_["label"] = "Features:"
                    f_["value"] = parts[1].strip()
                    self._AList["features"] = f_
                    
                if line.startswith("flags"):
                    parts = line.split(":")
#                    print(parts[1].strip() )
                    flags = {}
                    flags["key"] = "flags"
                    flags["label"] = "Flags:"
                    flags["value"] = parts[1].strip()
                    self._AList["flags"] = flags
                    

        if last_processor > 0:
            arm_cores = {}
            arm_cores["key"]= "armcores"
            arm_cores["label"] = "CPU cores:"
            arm_cores["value"] = str(last_processor + 1)
            self._AList["armcores"] = arm_cores
        
    def MemInfo(self):

        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal"):
                    parts = line.split(":")
                    parts[1] = parts[1].replace("kB","")
                    print(   parts[1].strip() )

                    memory = {}
                    memory["key"] = "memory"
                    memory["label"] = "Memory:"
                    memory["value"] = str( int(parts[1].strip())/1000.0) +" MB"
                    self._AList["memory"] = memory                    
                    break
    def BatteryInfo(self):
        batteryinfo = {}
        batteryinfo["key"] = "batteryinfo"
        batteryinfo["label"] = "Battery:"
        charging_string = "Discharging"
        if BatteryAbstraction.IsCharging():
            charging_string = "Charging"

        batteryinfo["value"] = "{}/{} mAh, {}%, {}".format(
            BatteryAbstraction.CurrentVoltage(),
            BatteryAbstraction.MaxVoltage(),
            BatteryAbstraction.AsPercentage(),
            charging_string
        )
        self._AList["batteryinfo"] = batteryinfo




    def PortInfo1(self):
        portinfo = {}
        portinfo["key"] = "portinfo1"
        portinfo["label"] = "Originally created for ClockworkPi Gameshell."
        portinfo["value"] = ""
        self._AList["portinfo1"] = portinfo

    def PortInfo2(self):
        portinfo = {}
        portinfo["key"] = "portinfo2"
        portinfo["label"] = "Ported to Pocket CHIP by omgmog."
        portinfo["value"] = ""
        self._AList["portinfo2"] = portinfo


    def ThanksTimTam(self):
        thanks = {}
        thanks["key"] = "thankstimtam"
        thanks["label"] = "PocketCHIP Graphic created by TimTam"
        thanks["value"] = ""
        self._AList["thankstimtam"] = thanks


        

    def GenList(self):
        
        self._MyList = []
        
        start_x  = 0
        start_y  = 10
        last_height = 0

        for i,u in enumerate( ["cpuscalemhz","memory","uname", "batteryinfo", "portinfo1","portinfo2","thankstimtam"] ):
            if u not in self._AList:
                continue
            
            v = self._AList[u]
            
            li = InfoPageListItem()
            li._Parent = self
            li._PosX   = start_x
            li._PosY   = start_y + last_height
            li._Width  = Width
            li._Fonts["normal"] = self._ListFontObj
            li._Fonts["small"] = MySkinManager.GiveFont("varela12")
            
            if self._AList[u]["label"] != "":
                li.Init(  self._AList[u]["label"] )
            else:
                # li.Init( self._AList[u]["key"] )
                li.Init("")

            li._Flag = self._AList[u]["key"]

            if self._AList[u]["value"] != "":
                li.SetSmallText( self._AList[u]["value"] )
            else:
                li.SetSmallText("")
            
            last_height += li._Height
            
            self._MyList.append(li)
            
    def Init(self):
        if self._Screen != None:
            if self._Screen._CanvasHWND != None and self._CanvasHWND == None:
                self._HWND = self._Screen._CanvasHWND
                self._CanvasHWND = pygame.Surface( (self._Screen._Width,self._BGheight) )

        self._PosX = self._Index*self._Screen._Width 
        self._Width = self._Screen._Width ## equal to screen width
        self._Height = self._Screen._Height

        bgpng = IconItem()
        bgpng._ImgSurf = MyIconPool._Icons["about_bg"]
        bgpng._MyType = ICON_TYPES["STAT"]
        bgpng._Parent = self
        bgpng.Adjust(0,0,self._BGwidth,self._BGheight,0)

        self._Icons["bg"] = bgpng
        
        self.CpuInfo()
        self.MemInfo()
        self.CpuMhz()
        self.Uname()
        self.BatteryInfo()
        self.PortInfo1()
        self.PortInfo2()
        self.ThanksTimTam()
        
        self.GenList()

        self._Scroller = ListScroller()
        self._Scroller._Parent = self
        self._Scroller._PosX = self._Width - 10
        self._Scroller._PosY = 2
        self._Scroller.Init()
        self._Scroller.SetCanvasHWND(self._HWND)
        
    def ScrollDown(self):
        dis = 10
        if abs(self._Scrolled) <  (self._BGheight - self._Height)/2 + 50:
            self._PosY -= dis
            self._Scrolled -= dis
        
    def ScrollUp(self):
        dis = 10
        if self._PosY < 0:
            self._PosY += dis
            self._Scrolled += dis

        
    def OnLoadCb(self):
        self._Scrolled = 0
        self._PosY = 0
        self._DrawOnce = False

    def OnReturnBackCb(self):
        self.ReturnToUpLevelPage()
        self._Screen.Draw()
        self._Screen.SwapAndShow()
        
    def KeyDown(self,event):
        if IsKeyMenuOrB(event.key):
            self.ReturnToUpLevelPage()
            self._Screen.Draw()
            self._Screen.SwapAndShow()

        # We don't need this page to be scrolly   

        # if event.key == CurKeys["Up"]:
        #     self.ScrollUp()
        #     self._Screen.Draw()
        #     self._Screen.SwapAndShow()
        # if event.key == CurKeys["Down"]:
        #     self.ScrollDown()
        #     self._Screen.Draw()
        #     self._Screen.SwapAndShow()
        
                                
    def Draw(self):

        if self._DrawOnce == False:
            self.ClearCanvas()
            #self._Ps.Draw()
        
            self._Icons["bg"].NewCoord(self._Width/2,self._Height/2 + (self._BGheight - Height)/2 + self._Screen._TitleBar._Height)
            self._Icons["bg"].Draw()

            for i in self._MyList:
                i.Draw()
                
            self._DrawOnce = True
            
        if self._HWND != None:
            # self._HWND.fill((255,255,255))
            
            self._HWND.blit(self._CanvasHWND,(self._PosX,self._PosY,self._Width, self._Height ) )
            
            # self._Scroller.UpdateSize(self._BGheight,abs(self._Scrolled)*3)
            # self._Scroller.Draw()
        
        


class APIOBJ(object):

    _Page = None
    def __init__(self):
        pass
    def Init(self,main_screen):
        self._Page = AboutPage()
        self._Page._Screen = main_screen
        self._Page._Name ="About"
        self._Page.Init()
        
    def API(self,main_screen):
        if main_screen !=None:
            main_screen.PushPage(self._Page)
            main_screen.Draw()
            main_screen.SwapAndShow()

OBJ = APIOBJ()
def Init(main_screen):    
    OBJ.Init(main_screen)
def API(main_screen):
    OBJ.API(main_screen)
    
        
