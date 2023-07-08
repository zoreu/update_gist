import re
import base64
from urllib.parse import urlparse, parse_qs, quote, unquote, quote_plus, unquote_plus, urlencode
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6'}

def web_bot(url,headers2):
    headers.update(headers2)
    from selenium import webdriver
    webdriver_path = "./chromedriver"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument(f"--headers={headers}")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    page_source = driver.page_source
    driver.quit()
    return page_source


def get_script_futebolplay(channel):
    canais = {'megapix': ['\x68\x74\x74\x70\x73\x3a\x2f\x2f\x66\x75\x74\x65\x62\x6f\x6c\x70\x6c\x61\x79\x68\x64\x2e\x63\x6f\x6d\x2f\x70\x6c\x61\x79\x65\x72\x2f\x61\x6f\x76\x69\x76\x6f\x2e\x70\x68\x70\x3f\x63\x61\x6e\x61\x6c\x3d\x6d\x65\x67\x61\x70\x69\x78\x73\x64\x26\x70\x61\x73\x74\x61\x3d\x6d\x79\x6c\x69\x76\x65', '\x68\x74\x74\x70\x73\x3a\x2f\x2f\x66\x75\x74\x65\x62\x6f\x6c\x70\x6c\x61\x79\x68\x64\x2e\x63\x6f\x6d\x2f\x61\x73\x73\x69\x73\x74\x69\x72\x2d\x6d\x65\x67\x61\x70\x69\x78\x2d\x61\x6f\x2d\x76\x69\x76\x6f\x2d\x6f\x6e\x6c\x69\x6e\x65\x2d\x32\x34\x2d\x68\x6f\x72\x61\x73\x2f']
        }
    url = canais[channel][0]
    referer = canais[channel][-1]
    referer_player = '\x68\x74\x74\x70\x73\x3a\x2f\x2f\x66\x75\x74\x65\x62\x6f\x6c\x70\x6c\x61\x79\x68\x64\x2e\x63\x6f\x6d\x2f'
    origin = '\x68\x74\x74\x70\x73\x3a\x2f\x2f\x66\x75\x74\x65\x62\x6f\x6c\x70\x6c\x61\x79\x68\x64\x2e\x63\x6f\x6d'
    headers.update({'Referer': referer})
    src = web_bot(url,headers)
    try:
        script = re.findall(r'<script>([^"]+)</script>', src,re.DOTALL|re.IGNORECASE|re.MULTILINE)
        script = script[0]
    except:
        script = ''
    return script,referer_player,origin

def make_url(chann):
    script,referer,origin = get_script_futebolplay(chann)
    import js2py
    context = js2py.EvalJs()
    stubs = r'''
        // Protect Objects

        Object.freeze(console.log);
        Object.freeze(console);


        // Fake DOM

        Element = function() {};
        Element.prototype.innerHTML = '';
        Element.prototype.src = '';

        function Document() {};
        Document.prototype.referrer = 'https://www.futemax.fm/';
        Document.prototype.body = new Document();
        Document.prototype.getElementById = function(id) { return new Element(); };
        Document.prototype.createElement = function(tagName) { return new Element(); };
        Document.prototype.append = function(args) {};

        var document = new Document();


        // Fake LIBs

        p2pml = { 'hlsjs': { 'Engine': { 'isSupported': function () { return false } } } };

        function __clappr__events() {};
        __clappr__events.prototype.PLAYER_STOP = '';

        function __clappr__player() {};
        __clappr__player.prototype.setVolume = function() {};
        __clappr__player.prototype.play = function() {};
        __clappr__player.prototype.on = function() {};

        function __clappr__clappr() {};
        __clappr__clappr.prototype.results = '';
        __clappr__clappr.prototype.Player = function(args) { __clappr__clappr.prototype.results = args; return new __clappr__player() };
        __clappr__clappr.prototype.Events = function() { return new __clappr__events() };

        var Clappr = new __clappr__clappr();
        '''
    context.execute(stubs)
    js2py.disable_pyimport()
    context.execute(script)
    url = context.Clappr.results['source'] + '|User-Agent=' + quote(headers['User-Agent']) + '&Origin=' + quote(origin) + '&Referer=' + quote(referer)
    texto_base64 = base64.b64encode(url.encode("utf-8")).decode("utf-8")
    print(texto_base64)

make_url('megapix')