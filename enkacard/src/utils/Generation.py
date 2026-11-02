# Copyright 2022 DEViantUa <t.me/deviant_ua>
# All rights reserved.
from PIL import Image, ImageChops,ImageFilter
from . import openFile
from .options import *
from .gradient import userAdaptGrandient, colorBg
import os
path = os.path.dirname(__file__).replace("utils","assets")

try:
    from enkacard.namecard_ctx import get_namecard_bg as _get_nc_bg, nc_cover as _nc_cover
except ImportError:
    def _get_nc_bg(): return None
    def _nc_cover(nc, w, h): return nc.resize((w, h), __import__("PIL.Image", fromlist=["Image"]).Image.LANCZOS).convert("RGBA")

_img_cache = {}

_ELEMENT_BG = {
    "Fire": "PYRO", "Grass": "DENDRO", "Electric": "ELECTRO",
    "Water": "GYDRO", "Wind": "ANEMO", "Rock": "GEO", "Ice": "CRYO",
}

_ICON_PATH = {
    "FIGHT_PROP_MAX_HP": "HP.png", "FIGHT_PROP_HP": "HP.png",
    "FIGHT_PROP_CUR_ATTACK": "ATTACK.png", "FIGHT_PROP_ATTACK": "ATTACK.png",
    "FIGHT_PROP_CUR_DEFENSE": "DEFENSE.png", "FIGHT_PROP_DEFENSE": "DEFENSE.png",
    "FIGHT_PROP_ELEMENT_MASTERY": "MASTERY.png",
    "FIGHT_PROP_CRITICAL": "CRITICAL_HURT.png",
    "FIGHT_PROP_CRITICAL_HURT": "CRITICAL.png",
    "FIGHT_PROP_CHARGE_EFFICIENCY": "CHARGE_EFFICIENCY.png",
    "FIGHT_PROP_DEFENSE_PERCENT": "DEFENSE_PERCENT.png",
    "FIGHT_PROP_ATTACK_PERCENT": "ATTACK_PERCENT.png",
    "FIGHT_PROP_HP_PERCENT": "HP_PERCENT.png",
    "FIGHT_PROP_HEAL_ADD": "HEALED_ADD.png",
    "FIGHT_PROP_HEAL": "HEAL.png",
    "FIGHT_PROP_PHYSICAL_ADD_HURT": "PHYSICAL_ADD_HURT.png",
}

_ELEMENT_ICON = {
    "FIGHT_PROP_ELEC_ADD_HURT":  ("ELECTRO.png",  "ELECTRO_UP.png"),
    "FIGHT_PROP_WATER_ADD_HURT": ("HYDRO.png",    "HYDRO_UP.png"),
    "FIGHT_PROP_WIND_ADD_HURT":  ("ANEMO.png",    "ANEMO_UP.png"),
    "FIGHT_PROP_ICE_ADD_HURT":   ("CRYO.png",     "CRYO_UP.png"),
    "FIGHT_PROP_ROCK_ADD_HURT":  ("GEO.png",      "GEO_UP.png"),
    "FIGHT_PROP_FIRE_ADD_HURT":  ("PYRO.png",     "PYRO_UP.png"),
    "FIGHT_PROP_GRASS_ADD_HURT": ("DENDRO.png",   "DENDRO_UP.png"),
}

def _open(file_path, convert=None):
    key = (file_path, convert)
    if key not in _img_cache:
        img = Image.open(file_path)
        if convert:
            img = img.convert(convert)
        img.load()
        _img_cache[key] = img
    return _img_cache[key].copy()

def centryImage(userImages, teample = 1):
    if teample == 6:
        x,y = userImages.size
        if max(x, y) / min(x, y) < 1.1:
            baseheight = 1615
            hpercent = (baseheight / float (y)) 
            wsize = int ((float (x) * float (hpercent)))
            userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
            return userImages, -235
            # квадратное 
        elif x > y:
            baseheight = 1615
            hpercent = (baseheight / float (y)) 
            wsize = int ((float (x) * float (hpercent)))
            userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
            return userImages, int(515 -userImages.size[0]/2)
        else:
            basewidth = 1066
            wpercent = (basewidth / float(userImages.size[0]))
            hsize = int((float(userImages.size[1]) * float(wpercent)))
            if hsize < 1615:
                baseheight = 1615
                hpercent = (baseheight / float (y)) 
                wsize = int ((float (x) * float (hpercent)))
                userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
                return userImages, int(515 -userImages.size[0]/2)
            userImages = userImages.resize((basewidth, hsize), Image.LANCZOS)

            return userImages, 0
        
    elif teample == 1:
        x,y = userImages.size
        if max(x, y) / min(x, y) < 1.1:
            baseheight = 787
            hpercent = (baseheight / float (y)) 
            wsize = int ((float (x) * float (hpercent)))
            userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
            return userImages, -58
            # квадратное 
            pass
        elif x > y:
            baseheight = 787
            hpercent = (baseheight / float (y)) 
            wsize = int ((float (x) * float (hpercent)))
            userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
            return userImages, int(271 -userImages.size[0]/2)
        else:
            basewidth = 575
            wpercent = (basewidth / float(userImages.size[0]))
            hsize = int((float(userImages.size[1]) * float(wpercent)))
            if hsize < 787:
                baseheight = 787
                hpercent = (baseheight / float (y)) 
                wsize = int ((float (x) * float (hpercent)))
                userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
                return userImages, int(271 -userImages.size[0]/2)
            userImages = userImages.resize((basewidth, hsize), Image.LANCZOS)
            return userImages, 0
            # вертикальное
        
    elif teample == 2:
        x,y = userImages.size
        if max(x, y) / min(x, y) < 1.1:
            baseheight = 1047
            hpercent = (baseheight / float (y)) 
            wsize = int ((float (x) * float (hpercent)))
            userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
            return userImages, 537, 0
            # квадратное 
            pass
        elif x > y:

            baseheight = 1047
            hpercent = (baseheight / float (y)) 
            wsize = int ((float (x) * float (hpercent)))
            userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
            return userImages, int(972 -userImages.size[0]/2), 1
        else:
            basewidth = 1029
            wpercent = (basewidth / float(userImages.size[0]))
            hsize = int((float(userImages.size[1]) * float(wpercent)))
            userImages = userImages.resize((basewidth, hsize), Image.LANCZOS)
            return userImages, 509,2
            # вертикальное
    elif teample == 4:
        x,y = userImages.size
        if max(x, y) / min(x, y) < 1.1:
            basewidth = 647
            wpercent = (basewidth / float(userImages.size[0]))
            hsize = int((float(userImages.size[1]) * float(wpercent)))
            userImages = userImages.resize((basewidth, hsize), Image.LANCZOS)
            return userImages, int(194-userImages.size[0]/2)
            # квадратное 
            pass
        elif x > y:
            baseheight = 621
            hpercent = (baseheight / float (y)) 
            wsize = int ((float (x) * float (hpercent)))
            userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
            return userImages, int(194 -userImages.size[0]/2)
        else:
            basewidth = 388
            wpercent = (basewidth / float(userImages.size[0]))
            hsize = int((float(userImages.size[1]) * float(wpercent)))
            if hsize < 618:
                baseheight = 621
                hpercent = (baseheight / float (y)) 
                wsize = int ((float (x) * float (hpercent)))
                userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
                return userImages, int(194 -userImages.size[0]/2)
            userImages = userImages.resize((basewidth, hsize), Image.LANCZOS)
            return userImages, 0
            # вертикальное
    else:
        x,y = userImages.size
        if max(x, y) / min(x, y) < 1.1:
            baseheight = 802
            hpercent = (baseheight / float (y)) 
            wsize = int ((float (x) * float (hpercent)))
            userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
            return userImages, (0,0), 1
            # квадратное '''
        elif x > y:
            baseheight = 802
            hpercent = (baseheight / float (y)) 
            wsize = int ((float (x) * float (hpercent)))
            userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
            return userImages, (int(300  -userImages.size[0]/2),0), 1
        else:
            basewidth = 645
            wpercent = (basewidth / float(userImages.size[0]))
            hsize = int((float(userImages.size[1]) * float(wpercent)))
            userImages = userImages.resize((basewidth, hsize), Image.LANCZOS)
            if hsize < 802:
                baseheight = 802
                hpercent = (baseheight / float (y)) 
                wsize = int ((float (x) * float (hpercent)))
                userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
                return userImages, (int(300  -userImages.size[0]/2),0), 2
            return userImages, (0,0), 2


def openImageElement(element, teample=1):
    folder = {1: "teapmleOne", 2: "teapmleTwo"}.get(teample, "teapmleTree")
    name = _ELEMENT_BG.get(element, "ERROR")
    base = _open(f'{path}/{folder}/background/{name}.png', "RGBA")
    nc = _get_nc_bg()
    if nc is not None:
        return _nc_cover(nc, *base.size)
    return base

def openImageElementConstant(element, teampt=1):
    name = _ELEMENT_BG.get(element, "ERROR")
    if teampt in [1, 2]:
        return _open(f'{path}/constant/{name}.png')
    else:
        return (
            _open(f'{path}/teapmleTree/constant/open/OPEN_CONST_{name}.png'),
            _open(f'{path}/teapmleTree/constant/closed/CLOSE_CONST_{name}.png'),
        )


def maskaAdd(element,charter, teample = 1):
    charter = charter.convert("RGBA")
    if teample == 1:
        bg = openImageElement(element)
        bgUP = bg.copy()
        bg.alpha_composite(charter,(-734,-134))
        im = Image.composite(bg, bgUP, openFile.MaskaBgTeampleOne.convert('L'))
        bg.alpha_composite(im,(0,0))
    elif teample == 2:
        bg = openImageElement(element, teample = 2)
        bgUP = bg.copy()
        bg.alpha_composite(charter,(0,0))
        im = Image.composite(bg, bgUP, openFile.MaskaSplas.convert('L').resize(bg.size))
        bg.alpha_composite(im,(0,0))
        bg.alpha_composite(openFile.MasskaEffectDown,(0,0))
    else:
        bg = openImageElement(element, teample = 3)
        bgUP = bg.copy()
        bg.alpha_composite(charter,(-810,-115))
        im = Image.composite(bg, bgUP, openFile.UserBgTeampleTree.convert('L'))
        bg.alpha_composite(im,(0,0))
        bg.alpha_composite(openFile.EffectBgTeampleTree,(0,0))
    return bg


def userImage(img,element = None, adaptation = False):
    userImagess,pozitionX = centryImage(img)
    if adaptation:
        grandient = userAdaptGrandient(userImagess.convert("RGB").copy())
        grandient = grandient.resize((1502,787))
        Effect = openFile.UserEffectTeampleOne.copy().convert('RGBA')
        grandient = ImageChops.soft_light(grandient,Effect)
        
        Effect.alpha_composite(userImagess,(pozitionX,0))
        im = Image.composite(Effect, grandient, openFile.MaskaUserBg2TeampleOne.convert("L"))
        return im
    else:
        try:
            bg = openImageElement(element)
            effect = bg.copy()
        except Exception as e:
            print(e)

        bg.alpha_composite(userImagess,(pozitionX,0))
        im = Image.composite(bg, effect, openFile.MaskaUserBg2TeampleOne.convert("L"))
        bg.alpha_composite(im,(0,0))
        return bg

def userImageTree(img,element = None, adaptation = False):
    userImagess,pozitionX,types = centryImage(img, teample = 3)
    if adaptation:
        grandient = userAdaptGrandient(userImagess.convert("RGB").copy(), size =(2,802))
        grandient = grandient.resize((1924,802))
        Effect = openFile.EffectBgTree.copy().convert("RGBA")
        grandient = ImageChops.soft_light(grandient,Effect)
        Effect.alpha_composite(userImagess,pozitionX)
        if types == 2:
            im = Image.composite(Effect, grandient, openFile.USER_BG_IMG_VERT.convert("L"))
        else:
            im = Image.composite(Effect, grandient, openFile.UserBgTeampleImgTree.convert("L"))
        
        im.alpha_composite(openFile.EffectBgTeampleTree,(0,0))
        return im
    else:
        bg = openImageElement(element, teample = 3)
        effect = bg.copy()
        bg.alpha_composite(userImagess,pozitionX)
        im = Image.composite(bg, effect, openFile.UserBgTeampleImgTree.convert("L"))
        bg.alpha_composite(im,(0,0))
        bg.alpha_composite(openFile.EffectBgTeampleTree.convert("RGBA"),(0,0))
        return bg


def userImageTwo(img,element = None, adaptation = False):
    userImagess,pozitionX,types = centryImage(img, teample = 2)
    if adaptation:
        bg = openImageElement("error", teample = 2)
        grandientLeft = userAdaptGrandient(userImagess.convert("RGB").copy(), size = (2, 1048),left = True)
        grandientLeft = grandientLeft.resize((1038,1048))
        grandientRight = userAdaptGrandient(userImagess.convert("RGB").copy(), size = (2, 1048))
        grandientRight = grandientRight.resize((937,1048))
        bg.alpha_composite(grandientLeft,(0,0))
        bg.alpha_composite(grandientRight,(grandientLeft.size[0],0))
        Effect = openFile.UserEffectTeampleTwo.copy().convert("RGBA")
        grandient = ImageChops.soft_light(bg,Effect)
        Effect.alpha_composite(userImagess,(pozitionX,0))
        if types == 0:
            im = Image.composite(Effect, grandient, openFile.UserBgTeampleTwo.convert("L"))
        elif types == 1:
            im = Image.composite(Effect, grandient, openFile.MaskaArt_TWO_TREE.convert("L"))
        else:
            im = Image.composite(Effect, grandient, openFile.MaskaArt_TWO.convert("L"))
        return im
    else:
        bg = openImageElement(element, teample = 2)
        effect = bg.copy()
        bg.alpha_composite(userImagess,(pozitionX,0))
        im = Image.composite(bg, effect, openFile.UserBgTeampleTwo.convert("L"))
        bg.alpha_composite(im,(0,0))
        return bg

def star(x):
    return _open(f'{path}/stars/Star{x}.png')


def elementIconPanel(element):
    name = _ELEMENT_BG.get(element, "PYRO")
    return _open(f'{path}/teapmleTwo/charter_element/{name}.png')

def getIconAdd(x, icon=False, size=None, element=False):
    if not icon and x not in IconAddTrue:
        return False
    if x in _ICON_PATH:
        icons = _open(f'{path}/icon/{_ICON_PATH[x]}', "RGBA")
    elif x in _ELEMENT_ICON:
        normal, up = _ELEMENT_ICON[x]
        icons = _open(f'{path}/icon/{up if element else normal}', "RGBA")
    else:
        return False
    if size:
        icons.thumbnail(size)
    return icons


def centrFive(userImages):
    x,y = userImages.size
    if max(x, y) / min(x, y) < 1.1:
        baseheight = 997
        hpercent = (baseheight / float (y)) 
        wsize = int ((float (x) * float (hpercent)))
        userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
        return userImages, (818,0), 1
        # квадратное 
        pass
    elif x > y:
        basewidth = 2605
        wpercent = (basewidth / float(userImages.size[0]))
        hsize = int((float(userImages.size[1]) * float(wpercent)))
        if hsize > 1690:
            baseheight = 997
            hpercent = (baseheight / float (y)) 
            wsize = int ((float (x) * float (hpercent)))
            userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
            return userImages, (818,0), 1
        userImages = userImages.resize((basewidth, hsize), Image.LANCZOS)
        return userImages, (0,0), 0
    else:
        basewidth = 1087
        wpercent = (basewidth / float(userImages.size[0]))
        hsize = int((float(userImages.size[1]) * float(wpercent)))
        userImages = userImages.resize((basewidth, hsize), Image.LANCZOS)
        return userImages, (759,-61), 2

def openBgElementFive(element):
    nc = _get_nc_bg()
    if nc is not None:
        return _nc_cover(nc, 2605, 997)
    if element == "Fire":
        return openFile.PYROTeampleFive
    elif element== "Grass":
        return openFile.DENDROTeampleFive
    elif element == "Electric":
        return openFile.ELECTROTeampleFive
    elif element == "Water":
        return openFile.GYDROTeampleFive
    elif element == "Wind":
        return openFile.ANEMOTeampleFive
    elif element== "Rock":
        return openFile.GEOTeampleFive
    else:
        return openFile.CRYOTeampleFive


async def creatFiveBg(userImages,element = "Rock",adapt = False):
    if adapt:
        img, px, format = centrFive(userImages)
        if format == 0:
            bg = openBgElementFive(element).copy().convert("RGBA")
            bg.alpha_composite(img,px)
            imgBlur = img.filter(ImageFilter.GaussianBlur(radius=15)).resize((2605,997)).convert("RGBA")
            bg = Image.composite(bg, imgBlur, openFile.MASKA_ADAPT_WIDTH.convert("L"))
        elif format == 1:
            bg = openBgElementFive(element).copy().convert("RGBA")
            grandientLeft = userAdaptGrandient(img.convert("RGB").copy(), size = (2, 997),left = True)
            grandientLeft = grandientLeft.resize((1302,997))
            grandientRight = userAdaptGrandient(img.convert("RGB").copy(), size = (2, 997))
            grandientRight = grandientRight.resize((1302,997))
            bg.alpha_composite(grandientLeft,(0,0))
            bg.alpha_composite(grandientRight,(1303,0))
            Effect = openFile.STARS_BG.copy().convert("RGBA")
            grandient = ImageChops.soft_light(bg,Effect)
            Effect.alpha_composite(img,px)
            bg = Image.composite(Effect, grandient, openFile.MASKA_ADAPT_HEIGHT_TWO.convert("L"))
        else:
            bg = openBgElementFive(element).copy().convert("RGBA")
            grandientLeft = userAdaptGrandient(img.convert("RGB").copy(), size = (2, 997),left = True)
            grandientLeft = grandientLeft.resize((1302,997))
            grandientRight = userAdaptGrandient(img.convert("RGB").copy(), size = (2, 997))
            grandientRight = grandientRight.resize((1302,997))
            bg.alpha_composite(grandientLeft,(0,0))
            bg.alpha_composite(grandientRight,(1303,0))
            Effect = openFile.STARS_BG.copy().convert("RGBA")
            grandient = ImageChops.soft_light(bg,Effect)
            Effect.alpha_composite(img,px)
            bg = Image.composite(Effect, grandient, openFile.MASKA_ADAPT_HEIGHT.convert("L"))
    else:
        bg = openBgElementFive(element).copy().convert("RGBA")
        effect = bg.copy()
        bg.alpha_composite(userImages,(0,-122))
        bg = Image.composite(bg, effect, openFile.MASKA_ADAPT_SPLASH.convert("L"))
    bg.alpha_composite(openFile.SHADOW_TEAMPLEfive,(0,540))
    return bg


async def openBgElementSeven(element):
    nc = _get_nc_bg()
    if nc is not None:
        return _nc_cover(nc, 940, 1010)
    if element == "Fire":
        return openFile.PYRO_SEVEN
    elif element== "Grass":
        return openFile.DENDRO_SEVEN
    elif element == "Electric":
        return openFile.ELECTRO_SEVEN
    elif element == "Water":
        return openFile.GYDRO_SEVEN
    elif element == "Wind":
        return openFile.ANEMO_SEVEN
    elif element== "Rock":
        return openFile.GEO_SEVEN
    else:
        return openFile.CRYO_SEVEN

async def centerSeven(userImages):
    x,y = userImages.size
    if max(x, y) / min(x, y) < 1.1:
        baseheight = 734
        hpercent = (baseheight / float (y)) 
        wsize = int ((float (x) * float (hpercent)))
        userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
        return userImages, (108,-50)
        # квадратное 
        pass
    elif x > y:
        basewidth = 940 
        wpercent = (basewidth / float(userImages.size[0]))
        hsize = int((float(userImages.size[1]) * float(wpercent)))
        if hsize > 1690:
            baseheight = 734
            hpercent = (baseheight / float (y)) 
            wsize = int ((float (x) * float (hpercent)))
            userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
            return userImages, (108,-50)
        userImages = userImages.resize((basewidth, hsize), Image.LANCZOS)
        return userImages, (0,0)
    else:
        basewidth = 734
        wpercent = (basewidth / float(userImages.size[0]))
        hsize = int((float(userImages.size[1]) * float(wpercent)))
        userImages = userImages.resize((basewidth, hsize), Image.LANCZOS)
        return userImages, (108,-50)


async def creatSevenBg(userImages,element = "Rock",adapt = False):
    if adapt:
        img, px = await centerSeven(userImages)
        color = await colorBg(img)
        bgA = Image.new("RGBA",(940,1010) ,color)
        bg = bgA.copy()
        bgA.alpha_composite(img,px)
        bg = Image.composite(bg, bgA, openFile.MASKA_ADAPT.convert("L"))

        bg = ImageChops.soft_light(bg,openFile.overlay_SEVEN.convert("RGBA"))        
    else:
        bgA = await openBgElementSeven(element)
        bgA = bgA.copy().convert("RGBA")
        bg = bgA.copy()
        bgA.alpha_composite(userImages,(-224,-97))
        bg = Image.composite(bg, bgA, openFile.MASKA_SPLASH.convert("L"))
    bg.alpha_composite(openFile.SHADOW_SEVEN,(0,0))
    bg.alpha_composite(openFile.FRAME_SEVEN,(0,0))    
    return bg

        


async def charterElement(element):
    if element == "Fire":
        return openFile.PYROTeampleFiveElement
    elif element== "Grass":
        return openFile.DENDROTeampleFiveElement
    elif element == "Electric":
        return openFile.ELECTROTeampleFiveElement
    elif element == "Water":
        return openFile.GYDROTeampleFiveElement
    elif element == "Wind":
        return openFile.ANEMOTeampleFiveElement
    elif element== "Rock":
        return openFile.GEOTeampleFiveElement
    else:
        return openFile.CRYOTeampleFiveElement

async def starFive(x,weapon = True):
    if weapon:
        if x == 1:
            return openFile.stars_light1
        elif x == 2:
            return openFile.stars_light2
        elif x == 3:
            return openFile.stars_light3
        elif x == 4:
            return openFile.stars_light4
        elif x == 5:
            return openFile.stars_light5
    else:
        if x == 1:
            return openFile.stars_frame1
        elif x == 2:
            return openFile.stars_frame2
        elif x == 3:
            return openFile.stars_frame3
        elif x == 4:
            return openFile.stars_frame4
        elif x == 5:
            return openFile.stars_frame5
        

async def open_bg_artifact(x, template = 1):
    if template == 1:
        if x == 5:
            return openFile.bg_5stars.copy()
        elif x == 4:
            return openFile.bg_4stars.copy()
        elif x == 3:
            return openFile.bg_3stars.copy()
        elif x == 2:
            return openFile.bg_2stars.copy()
        elif x == 1:
            return openFile.bg_1stars.copy()
