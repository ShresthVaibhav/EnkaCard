from PIL import ImageDraw,Image,ImageFont
from .FunctionsPill import imagSize,centrText,imgD
import os, asyncio
import time
import requests
from . import openFile

pfps = {}
PFP_URL = "https://raw.githubusercontent.com/EnkaNetwork/API-docs/refs/heads/master/store/gi/pfps.json"
class _LazyPfps:
    _data = None

    def __getitem__(self, key):
        if self._data is None:
            type(self)._data = requests.get(PFP_URL, timeout=15).json()
        return self._data[key]


pfp_data = _LazyPfps()

path = os.path.dirname(__file__).replace("utils","assets")

async def characters(player,assets,image,compare):
    t12 = ImageFont.truetype(openFile.font, 12)
    result = []
    charterList = {}
    charactersArg = []
    charactersids = []
    for key in player:
        if not compare:
            pass
        elif compare and key.id in compare:
            pass
        elif compare and key.id not in compare:
            continue
        person = assets.character(key.id)
        if not key.name in charterList:
            charterList[key.name] = {"rarity": person.rarity, "image": key.icon.url, "element": key.element.value, "id": key.id}
            charactersArg.append(key.name)
            charactersids.append(key.id)
        if image:
            if person.rarity == 4:
                iconCharter = Image.open(f'{path}/InfoCharter/iconCharter4.png')
            else:
                iconCharter = Image.open(f'{path}/InfoCharter/iconCharter5.png')
            iconsCharter = await imagSize(link = key.icon.url, fixed_width = 50)
            lvlCharter = str(key.level)
            d = ImageDraw.Draw(iconCharter)
            iconCharter.paste(iconsCharter,(3,3),iconsCharter)
            d.text((19,56), lvlCharter, font= t12, fill=(255,255,255,255))
            result.append(iconCharter)

    return result,charterList,charactersArg,charactersids


async def charactersTwo(player,assets,image,compare):
    t12 = ImageFont.truetype(openFile.font, 11)
    result = []
    charterList = []
    charactersArg = []
    charactersids = []
    for key in player:
        if not compare:
            pass
        elif compare and key.id in compare:
            pass
        elif compare and key.id not in compare:
            continue
        charter_bg = openFile.charter_bg.copy()
        person = assets.character(key.id)
        nameCharter = key.name
        nameCharters = key.icon.filename.split("Costume")[0].split("AvatarIcon_")[1]
        if nameCharters in ["PlayerGirl","PlayerBoy"]:
            linkImgCard = "https://gi.yatta.moe/assets/UI/UI_AvatarIcon_PlayerGirl.png"
        else:
            linkImgCard = f"https://enka.network/ui/UI_NameCardPic_{nameCharters}_P.png"
        try:
            banner = await imagSize(link = linkImgCard,size = (130,57))
        except:
            try:
                linkImgCard = f"https://enka.network/ui/UI_NameCardPic_{nameCharters}1_P.png"
                banner = await imagSize(link = linkImgCard,size = (130,57))
            except:
                pass

        charter_icon_mask = openFile.charter_icon_mask
        charactersArg.append(key.name)
        charactersids.append(key.id)

        charterList.append({"name": key.name, "rarity": person.rarity, "image": key.icon.url, "element": key.element.value, "id": key.id})
        if image:
            if person.rarity == 4:
                iconCharter = openFile.charter_icon_4.copy()
            else:
                iconCharter = openFile.charter_icon_5.copy()

            iconsCharterImg = await imagSize(link = key.icon.url, fixed_width = 71)
            lvlCharter = str(key.level)
            iconCharters = Image.composite(iconCharter, iconsCharterImg, charter_icon_mask.convert("L"))
            try:
                charter_bg.alpha_composite(banner,(32,11))
            except Exception as e:
                pass
            charter_bg.alpha_composite(iconCharter,(0,5))
            charter_bg.alpha_composite(iconCharters,(0,5))

            d = ImageDraw.Draw(charter_bg)

            xx = t12.getlength(nameCharter)
            d.text((int(111-xx/2),-1), nameCharter, font= t12, fill=(255,255,255,255))

            d.text((26,69), lvlCharter, font= t12, fill=(0,0,0,255))
            d.text((27,69), lvlCharter, font= t12, fill=(255,255,255,255))

            result.append(charter_bg)

    return {"r": result,"c": charterList, "ca": charactersArg, "cid":charactersids}


async def nameCard(player, fullBg):
    banner_light = openFile.banner_light
    if player.namecard.navbar.url == "https://enka.network/ui/.png":
        bannerUserNamecard = Image.open(f'{path}/InfoCharter/DEFAULT.png')
    else:
        bannerUserNamecard = await imgD(link = player.namecard.banner.url)
    bannerUserNamecard = bannerUserNamecard.transpose(Image.FLIP_LEFT_RIGHT)
    bannerUserNamecard = bannerUserNamecard.rotate(90, expand = True)
    bannerUserNamecard = bannerUserNamecard.resize((194,327))
    fullBg.paste(bannerUserNamecard,(26,0),openFile.banner_mask.convert("L"))
    fullBg.alpha_composite(banner_light,(26,0))

    return fullBg

async def avatar(fullBg,player, uid):
    ram_avatar = openFile.ram_avatar
    if player.avatar.icon is None:
        try:
            if player.avatar:
                avatar = "https://enka.network"+pfp_data[str(player.avatar.id)]["IconPath"]
            else:
                avatar ="https://enka.network/ui/UI_AvatarIcon_PlayerGirl_Circle.png"
        except Exception as e:
            avatar ="https://enka.network/ui/UI_AvatarIcon_PlayerGirl_Circle.png"
    else:
        avatar = player.avatar.icon.url
    picturesProfile = await imagSize(link = avatar,fixed_width = 159)
    avatar_user_bg = openFile.avatar_user_bg.copy()
    avatar_user_bg.alpha_composite(picturesProfile,(0,0))
    avatar_user_bg = avatar_user_bg.resize((159,159))
    fullBg.paste(avatar_user_bg,(475,25),openFile.avatar_user_mask)
    fullBg.alpha_composite(ram_avatar,(475,25))
    return fullBg

async def drawText(text):
    line = []
    lineText = ""
    if len(text) > 13:
        for key in text.split():
            lineText += f"{key} "
            if len(lineText) > 13:
                line.append(lineText)
                lineText = ""
        line.append(lineText)
        return "\n ".join(line[:3])

    else:
        return text


async def usersInfo(player, lang,hide,uid):
    fullBg = openFile.bgProfile.copy().convert("RGBA")
    bg = openFile.info_user.copy()
    d = ImageDraw.Draw(bg)
    t20 = ImageFont.truetype(openFile.font, 20)
    t14 = ImageFont.truetype(openFile.font, 14)
    xx = t20.getlength(player.nickname)
    d.text((int(109-xx/2),43), str(player.nickname), font= t20, fill=(255,255,255,255))

    d.text((330,10), f"{lang['WL']}:", font= t20, fill=(255,255,255,255))
    d.text((371,10), str(player.world_level), font= t20, fill=(203,75,75,255))

    d.text((348,47), f"{lang['AR']}:", font= t20, fill=(255,255,255,255))
    d.text((388,47), str(player.level), font= t20, fill=(203,75,75,255))

    d.text((349,84), f"{lang['AB']}:", font= t14, fill=(255,255,255,255))
    xx = t14.getlength(lang['AB'])
    d.text((349+xx+10,84), f"{player.abyss_floor}-{player.abyss_room}", font= t14, fill=(203,75,75,255))

    d.text((336,114), f"{lang['AC']}:", font= t14, fill=(255,255,255,255))
    xx = t14.getlength(lang['AC'])
    d.text((336+xx+10,115), str(player.achievement), font= t14, fill=(203,75,75,255))

    if hide:
        d.text((70,10), "UID:", font= t14, fill=(255,255,255,255))
        d.text((106,10), "Hidden", font= t14, fill=(203,75,75,255))
    else:
        d.text((70,10), "UID:", font= t14, fill=(255,255,255,255))
        d.text((108,10), str(uid), font= t14, fill=(203,75,75,255))
    signature = player.signature

    result = await drawText(signature)
    d.multiline_text((23,85), result, font= t14, fill=(255,255,255,255))

    fullBg.alpha_composite(bg,(285,26))
    fullBg = await avatar(fullBg,player, uid)

    return await nameCard(player,fullBg)

async def creatUserProfile(image,player,lang,hide,uid,assets,teample, compare=False):
    start = time.time()
    if teample == 1:
        t12 = ImageFont.truetype(openFile.font, 12)
        t17 = ImageFont.truetype(openFile.font, 17)
        Avatar = Image.open(f'{path}/InfoCharter/AvatarUser.png')
        Background = Image.open(f'{path}/InfoCharter/bg.png')
        UserName = Image.open(f'{path}/InfoCharter/UserName.png')
        Bg = None
        charactersListImage,charactersList,charactersArg,charters_id = await characters(player.characters_preview,assets,image,compare)
        if image:
            if player.namecard.navbar.url == "https://enka.network/ui/.png":
                ibanner = Image.open(f'{path}/InfoCharter/DEFAULT.png')
                bannerUserNamecard = await imagSize(image = ibanner, size = (661,105))
            else:
                try:
                    bannerUserNamecard = await imagSize(link = player.namecard.navbar.url, size = (661,105))
                except:
                    ibanner = Image.open(f'{path}/InfoCharter/DEFAULT.png')
                    bannerUserNamecard = await imagSize(image=ibanner, size=(661, 105))
            Background.paste(bannerUserNamecard,(123 ,145),bannerUserNamecard)
            if player.avatar.icon is None:
                try:
                    if player.avatar:
                        avatarx = "https://enka.network" + pfp_data[str(player.avatar.id)]["IconPath"]
                    else:
                        avatarx ="https://enka.network/ui/UI_AvatarIcon_PlayerGirl_Circle.png"
                except Exception as e:
                    avatarx ="https://enka.network/ui/UI_AvatarIcon_PlayerGirl_Circle.png"
            else:
                avatarx = player.avatar.icon.url
            picturesProfile = await imagSize(link = avatarx,fixed_width = 179)
            picturesProfile = picturesProfile.convert('RGBA')
            Avatar.paste(picturesProfile,(0,0),picturesProfile)
            Background.paste(Avatar,(41,110),openFile.MaskaInfoUser.convert("L"))
            d = ImageDraw.Draw(Background)
            d.text((556,264), f"{player.abyss_floor}-{player.abyss_room}", font= t17, fill=(73,81,100,255))
            d.text((290,264), str(player.achievement), font= t17, fill=(73,81,100,255))
            d = ImageDraw.Draw(UserName)
            centrName,fonts = await centrText(player.nickname, witshRam = 181, razmer = 22, start = 0)
            d.text((centrName,0), player.nickname, font= fonts, fill=(255,255,255,255))

            d.text((12,35), f"{lang['AR']}:{player.level}", font= t17, fill=(255,255,255,255))
            d.text((103,35), f"{lang['WL']}:{player.world_level}", font= t17, fill=(255,255,255,255))
            if hide:
                d.text((66,60), "Hidden", font= t12, fill=(255,255,255,255))
            else:
                d.text((66,61), str(uid), font= t12, fill=(255,255,255,255))

            Background.paste(UserName,(221,156),UserName)

            if len(charactersListImage) > 9:
                x = 215
                for key in charactersListImage:
                    Background.paste(key.resize((round(key.size[0]*0.8), round(key.size[1]*0.8))),(x,80),key.resize((round(key.size[0]*0.8), round(key.size[1]*0.8))))
                    x = x+50
                Bg = Background
            else:
                x = 224
                for key in charactersListImage:
                    Background.paste(key, (x, 70), key)
                    x = x + 66
                Bg = Background
        return {"character": charactersList, "character_name": charactersArg, "character_id": charters_id, "img": Bg, "performed":float('{:.2f}'.format(time.time()-start))}

    else:
        task = [usersInfo(player,lang,hide,uid),charactersTwo(player.characters_preview,assets,image,compare)]
        it = await asyncio.gather(*task)
        fullBg = it[0]
        charactersListImage,charactersList,charactersArg,charters_id = it[1]["r"], it[1]["c"], it[1]["ca"], it[1]["cid"]
        if len(charactersListImage) >8 :
            positions = [
                (265,201),(408,201),(551,201), (694, 201),
                (265,305),(408,305),(551,305), (694, 305),
                (265,409),(408,409), (551,409), (694, 409),
            ]
            rs = 0.75
        else:
            positions = [
                (265, 201), (448, 201), (641, 201),
                (265, 305), (448, 305), (641, 305),
                (369, 400), (552, 400)
            ]
            rs = 1
        i = 0
        for key in charactersListImage:
            fullBg.alpha_composite(key.resize((round(key.size[0]*rs), round(key.size[1]*rs))),positions[i])
            i += 1
        return {"character": charactersList, "character_name": charactersArg, "character_id": charters_id, "img": fullBg, "performed":float('{:.2f}'.format(time.time()-start))}
