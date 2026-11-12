import subprocess, sys, os
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))

SCRIPT = r"""
<script>
(function () {
  const vw = document.documentElement.clientWidth;
  const rows = [];
  const all = [...document.querySelectorAll('body *')];
  all.forEach(el => {
    const cs = getComputedStyle(el);
    if (cs.position === 'fixed') return;
    const r = el.getBoundingClientRect();
    if (!r.width && !r.height) return;
    const over = Math.round(r.right - vw);
    const under = Math.round(-r.left);
    if (over > 1 || under > 1) {
      const tag = el.tagName.toLowerCase();
      const cls = (el.getAttribute('class') || '').split(' ').slice(0,2).join('.');
      rows.push(`${tag}${cls?'.'+cls:''} R+${over} L-${under} w${Math.round(r.width)}`);
    }
  });
  const doc = document.documentElement;
  const box = document.createElement('div');
  box.style.cssText = 'position:fixed;inset:0 auto auto 0;z-index:99999;background:#fff;color:#000;font:11px/1.4 monospace;padding:8px;width:min(100%,780px);max-height:100vh;overflow:hidden';
  box.textContent =
    `vw=${vw} scrollW=${doc.scrollWidth} scrollH=${doc.scrollHeight} overflowX=${doc.scrollWidth>vw}\n` +
    `OVERFLOWING (${rows.length}):\n` + (rows.length ? rows.join('\n') : '  none');
  document.body.appendChild(box);
})();
</script>
"""

html = open(os.path.join(BASE, 'index.html')).read()
inject = '<style>.reveal{opacity:1!important;transform:none!important}.hero-art,.hero .eyebrow,.hero h1,.hero-text,.hero-actions{animation:none!important}</style>\n</head>'
html = html.replace('loading="lazy"', 'loading="eager"').replace('</head>', inject, 1).replace('</body>', SCRIPT + '</body>', 1)
open(os.path.join(BASE, '_diag.html'), 'w').write(html)

widths = [int(w) for w in sys.argv[1:]] or [320, 390, 480, 768, 1024, 1440]
for w in widths:
    out = f'/tmp/opencode/shots/d{w}.png'
    subprocess.run(['timeout', '120', 'firefox', '--headless', '--no-remote', '--profile', '/tmp/opencode/ffprof',
                    '--window-size', f'{w},1400', '--screenshot', out,
                    f'file://{BASE}/_diag.html'], capture_output=True)
    im = Image.open(out)
    im.crop((0, 0, min(w, 780), 520)).save(f'/tmp/opencode/shots/dc{w}.png')
    print('captured', w, im.size)
