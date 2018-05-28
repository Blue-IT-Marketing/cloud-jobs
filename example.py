__author__ = 'Justice Ndou'
__website__ = 'http://jobcloud.freelancing-seo.com/'
__email__ = 'justice@freelancing-seo.com'
from google.appengine.ext import db



from feedgen.feed import FeedGenerator
fg = FeedGenerator()
fg.id('http://lernfunk.de/media/654321')
fg.title('Some Testfeed')
fg.author( {'name':'John Doe','email':'john@example.de'} )
fg.link( href='http://example.com', rel='alternate' )
fg.logo('http://ex.com/logo.jpg')
fg.subtitle('This is a cool feed!')
fg.link( href='http://larskiesow.de/test.atom', rel='self' )
fg.language('en')
class Rss(db.Expando):
    feed = db.TextProperty()


