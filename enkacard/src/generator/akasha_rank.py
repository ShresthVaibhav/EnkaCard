import random
from ..utils import pill, git
from PIL import ImageDraw,Image
from curl_cffi.requests import AsyncSession

_of = git.ImageCache()

api_url = "https://akasha.cv/api/getCalculationsForUser/{uid}"
api_update = "https://akasha.cv/api/user/refresh/{uid}"

#https://akasha.cv/api/leaderboards/{uid}/{hash}?variant=profilePage - ПОЛУЧИТЬ ХАШ ОБЩИЙ И ДЛЯ ПЕРСОНАЖЕЙ
#https://akasha.cv/api/substatPriority/{uid}/{hash} - ПОЛУЧИТЬ ИНФОРМАЦИЮ О СТАТАХ ПЕРСОНАЖА


data_akasha = {}

class AkashaCreat:
    def __init__(self,card = None,teample= None,rank= None,uid= None) -> None:
        self.card = card
        self.teample = teample
        self.rank = rank
        self.uid = uid

    async def get_hash(self, charter_id):
        async with AsyncSession(impersonate="chrome124") as session:
            try:
                await session.get(api_update.format(uid=self.uid))
            except Exception:
                pass
            response = await session.get(api_url.format(uid=self.uid))
            data = response.json()
            for key in data.get("data", []):
                if str(charter_id) == str(key["characterId"]):
                    return key["md5"]

    async def update(self):
        async with AsyncSession(impersonate="chrome124") as session:
            response = await session.get(api_update.format(uid=self.uid))
            return response.json()

    async def get_info_character(self, id):
        hash = await self.get_hash(id)
        if not hash:
            return {}
        url = f'https://akasha.cv/api/leaderboards/{self.uid}/{hash}?variant=profilePage'
        async with AsyncSession(impersonate="chrome124") as session:
            response = await session.get(url)
            if response.status_code == 200:
                return response.json().get("data") or {}
            return {}

    async def get_rank_akasha(self):
        if self.uid in data_akasha:
            return data_akasha[self.uid]
        akaska_info = []
        async with AsyncSession(impersonate="chrome124") as session:
            try:
                await session.get(api_update.format(uid=self.uid))
            except Exception:
                pass
            response = await session.get(api_url.format(uid=self.uid))
            if response.status_code == 200:
                for key in response.json().get("data", []):
                    calculator = key.get("calculations", {}).get("fit", {})
                    if calculator:
                        rank = int(str(calculator.get("ranking", "0")).replace("~", ""))
                        out = int(calculator.get("outOf", "1"))
                        percentage = round((rank / out) * 100)
                        if percentage == 0:
                            percentage = 1
                        akaska_info.append({"id": key["characterId"], "rank": rank, "out": out, "precent": percentage})
        data_akasha[self.uid] = akaska_info
        return akaska_info

    async def creat_logo(self):
        logo = await _of.akasha
        logo = logo.copy()
        
        background = Image.new("RGBA",(264,79) ,(0,0,0,0))
        
        background.alpha_composite(logo)
        
        font = await pill.get_font(12)
        d = ImageDraw.Draw(background)
        d.text((61,55), f'Rank: ~{self.rank.rank}/{self.rank.out}', font = font, fill= (255,255,255,255)) 
        d.text((61,39), f'Top: {self.rank.precent}%', font = font, fill= (255,255,255,255)) 
        
        return background
        
        
    async def start(self):
        if self.rank is None:
            return self.card

        logo = await self.creat_logo()

        if self.teample == 1:
            self.card.alpha_composite(logo, (11, 409))
        elif self.teample == 2:
            self.card.alpha_composite(logo, (952, 13))
        elif self.teample == 101:
            self.card.alpha_composite(logo, (10, 710))
        elif self.teample == 102:
            self.card.alpha_composite(logo, (30, -9))
        elif self.teample == 103:
            self.card.alpha_composite(logo, (250, 722))
        elif self.teample == 104:
            self.card.alpha_composite(logo, (460, 920))
        elif self.teample == 105:
            self.card.alpha_composite(logo, (1700, 800))
        elif self.teample == 106:
            self.card.alpha_composite(logo, (350, 935))
        elif self.teample == 107:
            self.card.alpha_composite(logo, (720, 265))
        return self.card