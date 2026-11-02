from PIL import Image,ImageChops
from ...utils import pill, git
import asyncio

try:
    from enkacard.namecard_ctx import get_namecard_bg as _get_nc_bg, nc_cover as _nc_cover
except ImportError:
    def _get_nc_bg(): return None
    def _nc_cover(nc, w, h): return nc.resize((w, h), Image.LANCZOS).convert("RGBA")

_of = git.ImageCache()

class Background:
    def __init__(self,img,element) -> None:
        self.img = img
        self.element = element
        
    async def get_element_color(self):
        if self.element is None:
            #self.element_color = await pill.get_color_art(self.img)
            self.element_color = await  pill.get_background_colors(self.img, 15, common=True, radius=5, quality=800)
            
        else:
            self.element_color = pill.element_color.get(self.element, (149,107,5,255))
            
            
    async def add_overlay(self):
        if self.element is None:
            ll = await pill.light_level(self.element_color)
            if ll < 0.30:
                overlay = await _of.overlay#overlay_dark
                self.background = ImageChops.soft_light(self.background, overlay.convert("RGBA") ) #screen
            else:
                overlay = await _of.overlay_dark
                self.background = ImageChops.soft_light(self.background, overlay.convert("RGBA") )
        else:
            overlay = await _of.overlay
            self.background = ImageChops.soft_light(self.background, overlay.convert("RGBA") )
            
    async def add_mask(self):
        background = Image.new("RGBA", (1511, 1301), (0,0,0,0))
        background_two = Image.new("RGBA", (1511, 1301), (0,0,0,0))
        background.alpha_composite(self.img,(0,308))
        background_two.paste(background,(0,0),self.mask.convert("L"))
        self.background.alpha_composite(background_two)
    
    async def creat_art(self):
        self.img = await pill.get_centr_honkai_art((965,993),self.img)
    
    async def add_shadow(self):
        shadow = await _of.shadow_one
        self.background.alpha_composite(shadow)
        
    async def start(self):
        self.mask =  await _of.maska_art
        self.mask = self.mask.convert("L")
        if not isinstance(self.img, Image.Image):
            self.img = await pill.get_dowload_img(self.img)
        await self.get_element_color()
        nc = _get_nc_bg()
        if nc is not None:
            self.background = _nc_cover(nc, 1511, 1301)
        else:
            self.background = Image.new("RGBA", (1511, 1301), self.element_color)
        await asyncio.gather(self.add_overlay(),self.creat_art())
        await self.add_mask()
        await self.add_shadow()
        
        return self.background 