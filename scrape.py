from lxml import html, etree
import cssselect
from numpy import full
import requests

base = 'https://subslikescript.com'
url = 'https://subslikescript.com/series/Family_Guy-182576'
response = requests.get(url)
document = html.document_fromstring(response.content)

anchors = [a for a in document.cssselect('a') if 'episode' in a.get('href')]

for a in anchors:
    href = a.get('href')

    season = href[href.index('season-') + 7 : href.index('/episode')]
    episode = href
    episode = episode[episode.index('episode-') + 8:]
    episode = episode[:episode.index('-')]

    # print(f'{season}/{episode}')

    response = requests.get(base + href)
    document = html.document_fromstring(response.content)
    fullscript = document.cssselect('.full-script')[0]
    content = str(etree.tostring(fullscript))
    formatted = content.replace('<br/>', '\n') \
                       .replace('(adsbygoogle = window.adsbygoogle || []).push({});', '') \
                       .replace('\\\'', '\'') \
                       .replace('\\n', '') \
                       .replace('b\'', '') \
                       .replace('<div class="full-script">', '') \
                       .replace('<script async="" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"/><!-- subslikescript native automated \'subslikescript article\' --><ins class="adsbygoogle" style="display:block; text-align:center;" data-ad-layout="in-article" data-ad-format="fluid" data-ad-client="ca-pub-6250492176235895" data-ad-slot="8633658590"/><script>     </script>', '') \
                       .replace('\n\n', '\n')

    outfile = open(f'{season}_{episode}.txt', 'w')
    outfile.write(formatted)
    outfile.close()

