import requests, re, json
import lxml.etree
import lxml.html.soupparser

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.14 (KHTML, like Gecko) Version/6.0.1 Safari/536.26.14'

json_getter = re.compile(r'trulia\.propertyData\.set\((.*?)\);')

def get(url):
    return requests.get(url, headers={'User-Agent':user_agent})

def parse(html):
    try:
        return lxml.etree.fromstring(html)
    except:
        return lxml.html.soupparser.fromstring(html)

def get_data(city, kind='for_rent',
        price=None, pets=None, amenities=None):
    """
    Get property listings from Trulia.

    city: The name (city, state) of the city to look in
    kind: for_rent or for_sale

    returns: itreator of dicts with result data"""

    assert kind in ('for_rent','for_sale')

    city = city.replace(', ', ',').replace(' ', '_')

    url_chunks = []
    if price:
        url_chunks.append('%d-%d_price' % price)
    if pets:
        url_chunks.append('%s_pets' % pets)
    if amenities:
        if isinstance(amenities, str):
            url_chunks.append('%s_amenities' % amenities)
        else:
            for e in amenities:
                url_chunks.append('%s_amenities' % e)

    base_url = 'http://trulia.com/%s/%s/%s' % (kind, city, '/'.join(url_chunks))
    first_page = get(base_url).text
    res = parse(first_page).xpath("id('4_paging')/a[last()]")[0]
    page_count = int(res.text)

    for page in xrange(page_count):
        if page == 0:
            html = first_page
        else:
            html = get('%s/%d_p/' % (base_url, page)).text
        for blob in json_getter.finditer(html):
            for e in json.loads(blob.group(1)):
                yield e

def get_picture_urls(datum):
    try:
        photos = datum['hasPhotos']
        assert photos is not None
    except:
        return
    for photo in photos:
        yield 'http://thumbs.trulia-cdn.com/pictures/thumbs/%s' % photo.split(':')[0]
