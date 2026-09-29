# Собирает index.html из index.template.html: подставляет контур лилии для узора фона и кнопки контактов.
import re, pathlib
from PIL import Image

root = pathlib.Path(__file__).parent
brand = (root / 'concepts' / 'brand.html').read_text(encoding='utf-8')
m = re.search(r'<symbol id="L" viewBox="([^"]+)"><path fill-rule="evenodd" d="([^"]+)"/></symbol>', brand)
vb, d = m.group(1), m.group(2)

contacts = (root / 'contacts.html').read_text(encoding='utf-8').strip() if (root / 'contacts.html').exists() \
    else '<a class="btn" href="#works">Смотреть проекты</a>'

t = (root / 'index.template.html').read_text(encoding='utf-8')
t = t.replace('{{LILY_VB}}', vb).replace('{{LILY_D}}', d).replace('{{CONTACTS}}', contacts)
(root / 'index.html').write_text(t, encoding='utf-8')

# favicon из 3D-лилии
lily = Image.open(root / 'img' / 'lily3d.png')
fav = Image.new('RGBA', (64, 64), (11, 42, 34, 255))
l = lily.copy(); l.thumbnail((56, 56), Image.LANCZOS)
fav.alpha_composite(l, ((64 - l.width) // 2, (64 - l.height) // 2))
fav.save(root / 'img' / 'favicon.png')

# картинка для превью ссылок (1200x630) из макета
src = root / 'concepts' / 'brand51.png'
if src.exists():
    im = Image.open(src).convert('RGB').resize((1440, 900), Image.LANCZOS)
    im.crop((120, 60, 1320, 690)).save(root / 'img' / 'og.jpg', quality=85)
print('index.html собран')
