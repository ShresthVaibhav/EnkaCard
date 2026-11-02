__all__ = ["weaponAdd",
           "nameBanner",
           "stats",
           "constant",
           "create_picture",
           "talants",
           "naborArtifact",
           "artifacAdd",
           "addConst",
           "addTallants",
           "addArtifact",
           "signature",
           "appedFrame",
           ]
from enum import Enum
import math, asyncio, aiohttp
from PIL import ImageDraw, ImageOps, ImageFilter
from . import options
from .Generation import *
from .FunctionsPill import centrText, imgD, imagSize
from .options import *
from . import openFile
import requests

"""class EquipType(Enum):
    Flower = 'EQUIP_BRACER'
    Feather = 'EQUIP_NECKLACE'
    Circlet = 'EQUIP_DRESS'
    Goblet = 'EQUIP_RING'
    Sands = 'EQUIP_SHOES'"""

async def create_picture(element, imgs, splash):
    if imgs:
        frame = userImageTwo(imgs, element=element, adaptation=True)
    else:
        banner = await imagSize(link=splash, size=(1974, 1048))
        frame = maskaAdd(element, banner, teample=2)
    return frame


async def weaponAdd(characters, lvlName):
    if characters.detail.artifact_name_set != "":
        return None
    WeaponBg = openFile.WeaponBgTeampleTwo.copy()
    proc = False
    d = ImageDraw.Draw(WeaponBg)
    name = characters.detail.name
    lvl = characters.level
    lvlUp = characters.refinement
    baseAtt = characters.detail.mainstats.value
    imageStats = None
    dopStat = 0
    for substate in characters.detail.substats:
        imageStats = getIconAdd(substate.prop_id, icon=True, size=(31, 31))
        if not imageStats:
            continue
        dopStat = substate.value
        if str(substate.type) == "DigitType.PERCENT":
            proc = True
    if imageStats:
        WeaponBg.alpha_composite(imageStats, (330, 59))

    stars = star(characters.detail.rarity)
    image = await imagSize(link=characters.detail.icon.url, size=(131, 138))
    WeaponBg.alpha_composite(image, (20, 11))
    position, font = await centrText(name, witshRam=290, razmer=24, start=177, Yram=38, y=17)
    d.text(position, str(name), font=font, fill=coloring)
    d.text((195, 111), str(lvlUp), font=fontSize(24), fill=(248, 199, 135, 255))
    position, font = await centrText(f"{lvlName['lvl']}: {lvl}/90", witshRam=211, razmer=24, start=251, Yram=38, y=107)
    d.text(position, f"{lvlName['lvl']}: {lvl}/90", font=font, fill=coloring)

    position, font = await centrText(baseAtt, witshRam=131, razmer=24, start=167, Yram=38, y=56)
    d.text(position, str(baseAtt), font=font, fill=coloring)
    if proc:
        position, font = await centrText(f'{dopStat}%', witshRam=131, razmer=24, start=333, Yram=38, y=56)
        d.text(position, f'{dopStat}%', font=font, fill=coloring)
    else:
        position, font = await centrText(str(dopStat), witshRam=131, razmer=24, start=333, Yram=38, y=56)
        d.text(position, str(dopStat), font=font, fill=coloring)
    WeaponBg.alpha_composite(stars, (10, 135))
    return WeaponBg


async def nameBanner(characters, lvlName):
    NameBg = openFile.NameBgTeampleTwo.copy()
    d = ImageDraw.Draw(NameBg)
    centrName, fonts = await centrText(characters.name, witshRam=244, razmer=24, start=19, Yram=29, y=0)
    d.text((centrName, 0), characters.name, font=fonts, fill=coloring)
    d.text((33, 45), str(characters.friendship_level), font=fontSize(24), fill=coloring)
    centrName, fonts = await centrText(f"{lvlName['lvl']}: {characters.level}/90", witshRam=209, razmer=24, start=77)
    d.text((centrName, 45), f"{lvlName['lvl']}: {characters.level}/90", font=fonts, fill=coloring)
    NameBg = NameBg.crop((0, 37, 286, 74))
    return NameBg

async def nameBannertwo(characters, lvlName):
    NameBg = openFile.NameBgTeampleTwo.copy()
    d = ImageDraw.Draw(NameBg)
    centrName, fonts = await centrText(characters.name, witshRam=244, razmer=24, start=19, Yram=29, y=0)
    d.text((centrName, 0), characters.name, font=fonts, fill=coloring)
    d.text((33, 45), str(characters.friendship_level), font=fontSize(24), fill=coloring)
    centrName, fonts = await centrText(f"{lvlName['lvl']}: {characters.level}/90", witshRam=209, razmer=24, start=77)
    d.text((centrName, 45), f"{lvlName['lvl']}: {characters.level}/90", font=fonts, fill=coloring)
    NameBg = NameBg.crop((0, 0, 286, 37))
    return NameBg


def starsAdd(person):
    StarsBg = openFile.StarBg.copy()
    starsIcon = star(person.rarity)
    StarsBg.alpha_composite(starsIcon, (17, -1))

    return StarsBg


async def stats(characters,assets):
    postion = (15,10)
    AttributeBg = openFile.AttributeBgTeampleTwo.copy()
    AttributeBg = AttributeBg.resize((round(AttributeBg.size[0]*1.3), AttributeBg.size[1]))
    g = characters[0].stats
    ff = characters[1].stats
    dopVal = {}
    checklist1 = []
    checklist2 = []
    elementUp = True
    сout = 0
    for key in g:
        if key[0] in ["BASE_HP", "FIGHT_PROP_BASE_ATTACK", "FIGHT_PROP_BASE_DEFENSE"]:
            if not key[0] in dopVal:
                dopVal[key[0]] = int(key[1].value)
        if key[1].id in [2000, 2001, 2002]:
            iconImg = getIconAdd(key[0])
            txt = assets.get_hash_map(key[0])
            Attribute = openFile.AttributeTeampleTwo.copy()
            attri = Attribute.crop((Attribute.size[0]//1.37, 0, Attribute.size[0], Attribute.size[1]))
            d = ImageDraw.Draw(Attribute)
            tt = ImageDraw.Draw(attri)
            icon = await imagSize(image=iconImg, fixed_width=26)

            Attribute.alpha_composite(icon, (10, 4))

            if not key[1].id in stat_perc:
                value = str(math.ceil(key[1].value))
            else:
                value = f"{round(key[1].value * 100, 1)}%"
            mey = [ee for ee in ff if ee[1].id == key[1].id]
            mey = mey[0]
            if not mey[1].id in stat_perc:
                value2 = str(math.ceil(mey[1].value))
            else:
                value2 = f"{round(mey[1].value * 100, 1)}%"
            pX, fnt = await centrText(value, witshRam=151, razmer=24, start=410)
            pX2, fnt2 = await centrText(value2, witshRam=151, razmer=24, start=0)
            d.text((pX, 7), value, font=fnt, fill=coloring)
            d.text((67, 7), str(txt), font=fontSize(24), fill=coloring)
            tt.text((pX2, 7), value2, font=fnt, fill=coloring)
            AttributeBg.alpha_composite(Attribute, (postion[0], postion[1]))
            AttributeBg.alpha_composite(attri, (Attribute.size[0]+40, postion[1]))
            postion = (postion[0], postion[1] + 55)
            сout += 1
            if сout == 3:
                break
    for key in g:
        if key[1].id in [40, 41, 42, 43, 44, 45, 46]:
            if elementUp:
                key = max((x for x in g if 40 <= x[1].id <= 46), key=lambda x: x[1].value)
                elementUp = False
            else:
                continue
        if key[1].value == 0 or key[1].id in [2000, 2001, 2002]:
            continue
        iconImg = getIconAdd(key[0])
        if not iconImg:
            continue
        checklist1.append(key)
        txt = assets.get_hash_map(key[0])
        Attribute = openFile.AttributeTeampleTwo.copy()
        attri = Attribute.crop((Attribute.size[0] // 1.37, 0, Attribute.size[0], Attribute.size[1]))
        d = ImageDraw.Draw(Attribute)
        tt = ImageDraw.Draw(attri)
        icon = await imagSize(image=iconImg, fixed_width=26)

        Attribute.alpha_composite(icon, (10, 4))

        if not key[1].id in stat_perc:
            value = str(math.ceil(key[1].value))
        else:
            value = f"{round(key[1].value * 100, 1)}%"
        mey = [ee for ee in ff if ee[1].id == key[1].id]
        mey = mey[0]
        if not mey[1].id in stat_perc:
            value2 = str(math.ceil(mey[1].value))
        else:
            value2 = f"{round(mey[1].value * 100, 1)}%"
        pX, fnt = await centrText(value, witshRam=151, razmer=24, start=410)
        pX2, fnt2 = await centrText(value2, witshRam=151, razmer=24, start=0)
        d.text((pX, 7), value, font=fnt, fill=coloring)
        d.text((67, 7), str(txt), font=fontSize(24), fill=coloring)
        tt.text((pX2, 7), value2, font=fnt, fill=coloring)
        AttributeBg.alpha_composite(Attribute, (postion[0], postion[1]))
        AttributeBg.alpha_composite(attri, (Attribute.size[0] + 40, postion[1]))
        postion = (postion[0], postion[1] + 55)
    for key in ff:
        if key[1].id in [40, 41, 42, 43, 44, 45, 46]:
            if key[1].value*100 >0:
                checklist2.append(key)
                key = max((x for x in g if 40 <= x[1].id <= 46), key=lambda x: x[1].value)
            else:
                continue
        if key[1].value == 0 or key[1].id in [2000, 2001, 2002]:
            continue
        iconImg = getIconAdd(key[0])
        if not iconImg:
            continue
        checklist2.append(key)
    check1_names = [item[0] for item in checklist1]
    distinctlist = []
    for ijk in checklist2:
        if ijk[0] not in check1_names:
            distinctlist.append(ijk)
    for mlk in distinctlist:
        iconImg = getIconAdd(mlk[0])
        if not iconImg:
            continue
        Attribute = openFile.AttributeTeampleTwo.copy()
        attri = Attribute.crop((Attribute.size[0] // 1.37, 0, Attribute.size[0], Attribute.size[1]))
        d = ImageDraw.Draw(Attribute)
        tt = ImageDraw.Draw(attri)
        txt = assets.get_hash_map(mlk[0])
        icon = await imagSize(image=iconImg, fixed_width=26)
        Attribute.alpha_composite(icon, (10, 4))

        if not mlk[1].id in stat_perc:
            value2 = str(math.ceil(mlk[1].value))
        else:
            value2 = f"{round(mlk[1].value * 100, 1)}%"
        mey = [ee for ee in g if ee[1].id == mlk[1].id]
        mey = mey[0]
        if not mey[1].id in stat_perc:
            value = str(math.ceil(mey[1].value))
        else:
            value = f"{round(mey[1].value * 100, 1)}%"
        pX, fnt = await centrText(value, witshRam=151, razmer=24, start=410)
        pX2, fnt2 = await centrText(value2, witshRam=151, razmer=24, start=0)
        d.text((pX, 7), value, font=fnt, fill=coloring)
        d.text((67, 7), str(txt), font=fontSize(24), fill=coloring)
        tt.text((pX2, 7), value2, font=fnt, fill=coloring)
        AttributeBg.alpha_composite(Attribute, (postion[0], postion[1]))
        AttributeBg.alpha_composite(attri, (Attribute.size[0] + 40, postion[1]))
        postion = (postion[0], postion[1] + 55)

    return AttributeBg


async def constant(characters):
    constantRes = []
    for key in characters.constellations:
        closeConstBg = openFile.ClossedBg.copy()
        closeConsticon = openFile.Clossed.copy()
        openConstBg = openImageElementConstant(characters.element.value)
        imageIcon = await imgD(link=key.icon.url)
        imageIcon = imageIcon.resize((43, 48))
        if not key.unlocked:
            closeConstBg.alpha_composite(imageIcon, (19, 20))
            closeConstBg.alpha_composite(closeConsticon, (0, -2))
            const = closeConstBg
        else:
            openConstBg.alpha_composite(imageIcon, (19, 20))
            const = openConstBg
        constantRes.append(const)
    XYZ = addConst(constantRes)
    return XYZ


async def talants(characters):
    tallantsRes = []
    for key in characters.skills:
        if key.level == 0:
            continue
        if key.level > 9:
            talantsBg = openFile.TalantsFrameGoldLvlTeampleTwo.copy()
        else:
            talantsBg = openFile.TalantsFrameTeampleTwo.copy()
        talantsCount = openFile.TalantsCountTeampleTwo.copy()
        d = ImageDraw.Draw(talantsCount)
        imagesIconTalants = await imgD(link=key.icon.url)
        imagesIconTalants = imagesIconTalants.resize((52, 52))
        talantsBg.alpha_composite(imagesIconTalants, (7, 6))
        if len(str(key.level)) == 2:
            d.text((3, 2), str(key.level), font=fontSize(18), fill=(248, 199, 135, 255))
        else:
            d.text((6, 2), str(key.level), font=fontSize(18), fill=(248, 199, 135, 255))
        talantsBg.alpha_composite(talantsCount, (20, 47))
        tallantsRes.append(talantsBg)
    return addTallants(tallantsRes)


async def naborArtifact(info, ArtifactNameBg):
    naborAll = []
    for key in info:
        if info[key] > 1:
            ArtifactNameFrame = openFile.ArtifactNameFrameTeampleTwo.copy()
            d = ImageDraw.Draw(ArtifactNameFrame)
            centrName, fonts = await centrText(key, witshRam=287, razmer=24, start=2, Yram=28, y=1)
            d.text((centrName[0], 0), str(key), font=fonts, fill=coloring)
            d.text((356, 0), str(info[key]), font=fontSize(24), fill=coloring)
            naborAll.append(ArtifactNameFrame)
    position = (156, 38)
    for key in naborAll:
        if len(naborAll) == 1:
            ArtifactNameBg.alpha_composite(key, (156, 54))
        else:
            ArtifactNameBg.alpha_composite(key, position)
            position = (position[0], position[1] + 34)

    return ArtifactNameBg


async def creatArtifact(infpart, imageStats):
    ArtifactBg = openFile.ArtifactBgTeampleTwo.copy()
    ArtifactUp = openFile.ArtifactBgUpTeampleTwo.copy()
    artimg = await imagSize(link=infpart.detail.icon.url, size=(120, 107))
    ArtifactBg.alpha_composite(artimg, (-5, 0))
    ArtifactBg.alpha_composite(ArtifactUp, (0, 0))
    d = ImageDraw.Draw(ArtifactBg)
    if str(infpart.detail.mainstats.type) == "DigitType.PERCENT":
        val = f"{infpart.detail.mainstats.value}%"
    else:
        val = infpart.detail.mainstats.value
    centrName, fonts = await centrText(val, witshRam=62, razmer=17, start=50)
    d.text((centrName, 76), str(val), font=fonts, fill=coloring)

    ArtifactBg.alpha_composite(imageStats, (7, 2))
    d.text((81, 97), str(infpart.level), font=fontSize(17), fill=coloring)
    starsImg = star(infpart.detail.rarity).resize((77, 22))
    ArtifactBg.alpha_composite(starsImg, (2, 97))
    cs = 0
    positionIcon = (130, 21)
    for key in infpart.detail.substats:
        ArtifactBgStat = openFile.ArtifactDopStatTeampleTwo.copy()
        d = ImageDraw.Draw(ArtifactBgStat)
        v = f"+{key.value}"
        if str(key.type) == "DigitType.PERCENT":
            v = f"{v}%"
        imageStats = getIconAdd(key.prop_id, icon=True)
        if not imageStats:
            continue
        imageStats = await imagSize(image=imageStats, fixed_width=24)
        ArtifactBgStat.alpha_composite(imageStats, (3, 1))
        d.text((57, 2), v, font=fontSize(24), fill=coloring)
        ArtifactBg.alpha_composite(ArtifactBgStat, positionIcon)
        cs += 1
        positionIcon = (positionIcon[0] + 185, positionIcon[1])
        if cs == 2:
            positionIcon = (130, 72)
    return ArtifactBg


async def artifacAdd(characters):
    count = 0
    listArt = {}
    artifacRes = {}
    ArtifactNameBg = openFile.ArtifactNameBgTeampleTwo.copy()
    for key in characters.equipments:
        if key.detail.artifact_name_set == "":
            continue
        if not key.detail.artifact_name_set in listArt:
            listArt[key.detail.artifact_name_set] = 1
        else:
            listArt[key.detail.artifact_name_set] += 1

        imageStats = getIconAdd(key.detail.mainstats.prop_id, icon=True, size=(21, 27))
        if not imageStats:
            continue
        count += 1
        artifacRes[str(key.detail.artifact_type.name)] = await creatArtifact(key, imageStats)

    rezArtSet = await naborArtifact(listArt, ArtifactNameBg)
    return {"art": addArtifact(artifacRes), "nab": rezArtSet}


async def creatUserInfotwo(hide, uid, player, lang, nameCharter=None, namecard=False):
    if not namecard:
        bannerUserNamecard = await imagSize(link=player.namecard.banner.url, size=(601, 283))
    else:
        nameCharter = nameCharter.split("Costume")[0]
        try:
            if nameCharter in ["PlayerGirl", "PlayerBoy"]:
                linkImgCard = "https://gi.yatta.moe/assets/UI/UI_AvatarIcon_PlayerGirl.png"
            else:
                linkImgCard = f"https://enka.network/ui/UI_NameCardPic_{nameCharter}_P.png"
            bannerUserNamecard = await imagSize(link=linkImgCard, size=(601, 283))
        except:
            linkImgCard = f"https://enka.network/ui/UI_NameCardPic_{nameCharter}1_P.png"
            bannerUserNamecard = await imagSize(link=linkImgCard, size=(601, 283))
    bannerUserNamecard = bannerUserNamecard.crop((0, 32, 601, 255))
    defoldBgNamecard = openFile.infoUserBgTeampleTwo.copy()
    maskaBannerNamecard = openFile.infoUserMaskaTeampleTwo.copy().convert('L')
    defoldBgNamecard = Image.composite(defoldBgNamecard, bannerUserNamecard, maskaBannerNamecard)
    frameUserNamecard = openFile.infoUserFrameTeampleTwoTwo.copy()
    defoldBgNamecard.alpha_composite(openFile.infoUserFrameBannerTeampleTwo, (0, 0))
    defoldBgNamecard = defoldBgNamecard.resize((round(defoldBgNamecard.size[0]*1.3), defoldBgNamecard.size[1]))
    if player.avatar.icon is None:
        try:
            from curl_cffi.requests import Session
            with Session(impersonate="chrome124") as _s:
                try:
                    _s.get(f"https://akasha.cv/api/user/refresh/{uid}")
                except Exception:
                    pass
                _r = _s.get(f"https://akasha.cv/api/user/{uid}")
            if _r.status_code == 200:
                avatar = _r.json()['data']['account']['profilePictureLink']
            else:
                avatar = "https://enka.network/ui/UI_AvatarIcon_Furina.png"
        except:
            avatar = "https://enka.network/ui/UI_AvatarIcon_Furina.png"
    else:
        avatar = player.avatar.icon.url
    avatar = await imagSize(link=avatar, size=(150, 150))
    avatar = Image.composite(frameUserNamecard, avatar, openFile.infoUserMaskaAvatarTeampleTwo.convert('L'))
    frameUserNamecard = ImageOps.mirror(frameUserNamecard)
    frameUserNamecard.alpha_composite(avatar, (205,0))
    d = ImageDraw.Draw(frameUserNamecard)
    centrName, fonts = await  centrText(player.nickname, witshRam=150, razmer=19, start=0)
    d.text((205+centrName, 155), player.nickname, font=fonts, fill=coloring)
    d.text((130, 34), f"{lang['AR']}:{player.level}", font=fonts, fill=coloring)
    d.text((130, 65), f"{lang['WL']}:{player.world_level}", font=fonts, fill=coloring)
    d.text((75, 99), f"{lang['AB']}:{player.abyss_floor}-{player.abyss_room}", font=fonts, fill=coloring)
    d.text((5, 131), f"{lang['AC']}:{player.achievement}", font=fonts, fill=coloring)

    if hide:
        d.text((45, 4), "UID: Hidden", font=fontSize(17), fill=coloring)
    else:
        d.text((45, 4), "UID: "+str(uid), font=fontSize(17), fill=coloring)

    defoldBgNamecard = ImageOps.mirror(defoldBgNamecard)
    defoldBgNamecard.alpha_composite(frameUserNamecard, (410, 21))

    return defoldBgNamecard


def addConst(constantRes):
    position = (1,10)
    bgConstant = openFile.ConstantBG.copy().rotate(90, expand=True)
    bgConstant = openFile.infoUserFrameBannerTeampleTwo.copy().rotate(90, expand=True).resize((round(bgConstant.size[0]*1.7), round(bgConstant.size[1]/1.7)))
    f = 0
    for key in constantRes:
        x = 0
        if f%2==1:
            x = 60
        bgConstant.alpha_composite(key ,(position[0]+x,position[1]))
        position = (position[0],position[1]+60)
        f+=1
    return bgConstant


def addTallants(talatsRes):
    position = (4, 8)
    bgTallatns = openFile.TalantsBGTeampleTwo.copy()
    bgTallatns = openFile.infoUserFrameBannerTeampleTwo.copy().resize((round(bgTallatns.size[0]/1.4), round(bgTallatns.size[1]*1.92))).rotate(90, expand=True)
    f = 1
    for key in talatsRes:
        j = 0
        if f == 2:
            j = 60
        key = key.resize((round(key.size[0]*1.15), round(key.size[1]*1.15)))
        bgTallatns.alpha_composite(key, (position[0]+j, position[1]))
        position = (position[0], position[1]+76)
        f+=1
    return bgTallatns


def addArtifact(artifacRes):
    position = (0, 0)
    width, height = 493, 700
    frameArtifact = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    if "Flower" in artifacRes:
        frameArtifact.alpha_composite(artifacRes["Flower"], (position[0], position[1]))
    position = (position[0], position[1] + 140)
    if "Feather" in artifacRes:
        frameArtifact.alpha_composite(artifacRes["Feather"], (position[0], position[1]))
    position = (position[0], position[1] + 140)
    if "Sands" in artifacRes:
        frameArtifact.alpha_composite(artifacRes["Sands"], (position[0], position[1]))
    position = (position[0], position[1] + 140)
    if "Circlet" in artifacRes:
        frameArtifact.alpha_composite(artifacRes["Circlet"], (position[0], position[1]))
    position = (position[0], position[1] + 140)
    if "Goblet" in artifacRes:
        frameArtifact.alpha_composite(artifacRes["Goblet"], (position[0], position[1]))
    position = (position[0], position[1] + 140)
    return frameArtifact


async def creatUserInfoOne(hide, uid, player, lang, nameCharter=None, namecard=False):
    if not namecard:
        bannerUserNamecard = await imagSize(link=player.namecard.banner.url, size=(601, 283))
    else:
        nameCharter = nameCharter.split("Costume")[0]
        try:
            if nameCharter in ["PlayerGirl", "PlayerBoy"]:
                linkImgCard = "https://gi.yatta.moe/assets/UI/UI_AvatarIcon_PlayerGirl.png"
            else:
                linkImgCard = f"https://enka.network/ui/UI_NameCardPic_{nameCharter}_P.png"
            bannerUserNamecard = await imagSize(link=linkImgCard, size=(601, 283))
        except:
            linkImgCard = f"https://enka.network/ui/UI_NameCardPic_{nameCharter}1_P.png"
            bannerUserNamecard = await imagSize(link=linkImgCard, size=(601, 283))
    bannerUserNamecard = bannerUserNamecard.crop((0, 32, 601, 255))
    defoldBgNamecard = openFile.infoUserBgTeampleTwo.copy()
    maskaBannerNamecard = openFile.infoUserMaskaTeampleTwo.copy().convert('L')
    defoldBgNamecard = Image.composite(defoldBgNamecard, bannerUserNamecard, maskaBannerNamecard)
    frameUserNamecard = openFile.infoUserFrameTeampleTwo.copy()
    defoldBgNamecard.alpha_composite(openFile.infoUserFrameBannerTeampleTwo, (0, 0))
    defoldBgNamecard = defoldBgNamecard.resize((round(defoldBgNamecard.size[0]*1.3), defoldBgNamecard.size[1]))
    if player.avatar.icon is None:
        try:
            from curl_cffi.requests import Session
            with Session(impersonate="chrome124") as _s:
                try:
                    _s.get(f"https://akasha.cv/api/user/refresh/{uid}")
                except Exception:
                    pass
                _r = _s.get(f"https://akasha.cv/api/user/{uid}")
            if _r.status_code == 200:
                avatar = _r.json()['data']['account']['profilePictureLink']
            else:
                avatar = "https://enka.network/ui/UI_AvatarIcon_Furina.png"
        except:
            avatar = "https://enka.network/ui/UI_AvatarIcon_Furina.png"
    else:
        avatar = player.avatar.icon.url
    avatar = await imagSize(link=avatar, size=(150, 150))
    avatar = Image.composite(frameUserNamecard, avatar, openFile.infoUserMaskaAvatarTeampleTwo.convert('L'))
    frameUserNamecard.alpha_composite(avatar, (0, 0))
    d = ImageDraw.Draw(frameUserNamecard)
    centrName, fonts = await  centrText(player.nickname, witshRam=150, razmer=19, start=0)
    d.text((centrName, 155), player.nickname, font=fonts, fill=coloring)
    d.text((163, 34), f"{lang['AR']}:{player.level}", font=fonts, fill=coloring)
    d.text((163, 65), f"{lang['WL']}:{player.world_level}", font=fonts, fill=coloring)
    d.text((163, 99), f"{lang['AB']}:{player.abyss_floor}-{player.abyss_room}", font=fonts, fill=coloring)
    d.text((163, 131), f"{lang['AC']}:{player.achievement}", font=fonts, fill=coloring)
    if hide:
        d.text((205, 3), "Hidden", font=fontSize(17), fill=coloring)
    else:
        d.text((205, 3), str(uid), font=fontSize(17), fill=coloring)
    defoldBgNamecard.alpha_composite(frameUserNamecard, (17, 21))

    return defoldBgNamecard

async def finalartimaker(characters):
    tassk = []
    tassk.append(artifacAdd(characters[0]))
    tassk.append(artifacAdd(characters[1]))
    ec = await asyncio.gather(*tassk)
    width, height = ec[-1]['art'].size[0] * 2 + 30, ec[-1]['art'].size[1]
    frameArtifact = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    frameArtifact.alpha_composite(ec[-2]['art'], (0, 0))
    frameArtifact.alpha_composite(ec[-1]['art'], (513, 0))
    return [frameArtifact, ec[0]['nab'], ec[1]['nab']]

async def makerimage(data):
    background = Image.new("RGBA", (1640, 200), (0, 0, 0, 0))
    frame = openFile.infoUserFrameBannerTeampleTwo.copy().convert("RGBA")
    background.alpha_composite(frame.resize((1640, 170)), (0, 0))
    font = options.fontSize(90)
    d = ImageDraw.Draw(background)
    if data is None:
        background = background.resize((600, 60))
        return background
    zzz = f'Top: {data["precent"]}%'
    yyy = f'Rank: ~{data["rank"]}/{round(data["out"] / 1000)}K'
    d.text((30, 30), zzz, font=font, fill=(255, 255, 255, 255))
    d.text((903 - 300, 30), yyy, font=font, fill=(255, 255, 255, 255))
    background = background.resize((600, 60))
    return background

async def make_ranks(uid, uid2, cid):
    tasks = []
    tasks.append(gat_rank_akasha(uid, cid))
    tasks.append(gat_rank_akasha(uid2, cid))
    ec = await asyncio.gather(*tasks)
    x = await makerimage(ec[0])
    y = await makerimage(ec[1])
    return [x,y]


async def gat_rank_akasha(uid, chart_id):
    api_url = f"https://akasha.cv/api/getCalculationsForUser/{uid}"

    from curl_cffi.requests import AsyncSession
    async with AsyncSession(impersonate="chrome124") as session:
        try:
            await session.get(f"https://akasha.cv/api/user/refresh/{uid}")
        except Exception:
            pass
        response = await session.get(api_url)
        if response.status_code != 200:
            return None
        try:
            data = response.json()
        except Exception:
            return None

        for key in data.get("data", []):
            if str(key["characterId"]) != str(chart_id):
                continue

            calculator = key.get("calculations", {}).get("fit", {})
            if calculator:
                rank = int(str(calculator.get("ranking", "0")).replace("~", ""))
                out = int(calculator.get("outOf", "1"))
                percentage = round((rank / out) * 100)
                if int(percentage) == 0:
                    percentage = 1
                return {"rank": rank, "out": out, "precent": percentage}
    return None

def appedFrame(ec, starsRes, elementRes, person, signatureRes):
    banner = ec[0].convert("RGBA")
    banner = banner.filter(ImageFilter.GaussianBlur(radius=10)).resize((round(banner.size[0]*0.95), round(banner.size[1]*0.85)))
    banner.alpha_composite(signatureRes[0], (0,0))
    banner.alpha_composite(signatureRes[1], (1069,0))
    banner.alpha_composite(ec[4], (175, 175))
    banner.alpha_composite(ec[6], (1169+210, 175))
    weap1 = ec[1].resize((385, 127))
    weap2 = ec[2].resize((385, 127))
    banner.alpha_composite(weap1, (0, 228))
    banner.alpha_composite(weap2, (390, 228))
    banner.alpha_composite(ec[5], (0, 360))
    banner.alpha_composite(ec[3], (796+42,-10))
    banner.alpha_composite(starsRes, (796+62,-10+210+5))
    banner.alpha_composite(ec[7], (785,-10+175+5))
    banner.alpha_composite(ec[-3], (786,238))
    banner.alpha_composite(ec[-2], (936, 238))
    banner.alpha_composite(ec[-5], (786, 488))
    banner.alpha_composite(ec[-4], (935, 488))
    arti = ec[-1][0].resize((784, 528))
    banner.alpha_composite(arti, (1084, 233))
    artiset = Image.new('RGBA', (789, 140), (0, 0, 0, 0))
    artiset.alpha_composite(ec[-1][1].resize((377, 88)), (0,0))
    artiset.alpha_composite(ec[-1][2].resize((377, 88)), (392,0))
    banner.alpha_composite(artiset, (1084, 750))
    ranks = ec[8]
    banner.alpha_composite(ranks[0].resize((377, 50)), (1084, 750+88+5))
    banner.alpha_composite(ranks[1].resize((377, 50)), (1084+392, 750+88+5))
    return banner

async def charactericon(url):
    bg = openFile.BGStatsTeampleFive.copy()
    bg = bg.convert("RGBA").resize((175,175))
    bannerUserNamecard = await imagSize(link=url, size=(165, 165))
    bg.alpha_composite(bannerUserNamecard, (5,5))
    return bg

async def generationCompare(uid, uid2, lang, characters, assets, signatureRes, img=None):
    person = assets.character(characters[0].id)
    starsRes = starsAdd(person)
    elementRes = elementIconPanel(characters[0].element.value)
    tassk = []
    tassk.append(create_picture(characters[0].element.value, img, characters[0].image.banner.url))
    tassk.append(weaponAdd(characters[0].equipments[-1], lang))
    tassk.append(weaponAdd(characters[1].equipments[-1], lang))
    tassk.append(charactericon(person.images.icon.url))
    tassk.append(nameBanner(characters[0], lang))
    tassk.append(stats(characters, assets))
    tassk.append(nameBanner(characters[1], lang))
    tassk.append(nameBannertwo(characters[1], lang))
    tassk.append(make_ranks(uid, uid2, characters[0].id))
    tassk.append(constant(characters[0]))
    tassk.append(constant(characters[1]))
    tassk.append(talants(characters[0]))
    tassk.append(talants(characters[1]))
    tassk.append(finalartimaker(characters))
    ec = await asyncio.gather(*tassk)
    result = appedFrame(ec, starsRes, elementRes, person, signatureRes)
    return result


