from scrape_any_url import scrape_site, keywords

vc_websites = [
    'https://www.accel.com/', 'https://www.a16z.com/', 'https://www.greylock.com/',
    'https://www.benchmark.com/', 'https://www.sequoiacap.com/', 'https://www.indexventures.com/',
    'https://www.kpcb.com/', 'https://www.lsvp.com/', 'https://matrix.vc/',
    'https://www.500.co/', 'https://www.sparkcapital.com/', 'https://www.insightpartners.com/'
]

for website in vc_websites:
    scrape_site(website, keywords)