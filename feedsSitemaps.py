__author__ = 'Justice Ndou'


'''
newsfeed = urlfetch.fetch('http://ae-book.appspot.com/blog/atom.xml/',
allow_truncated=False,
follow_redirects=False,
deadline=10)
newsfeed_xml = newsfeed.content
'''



import os
import webapp2
import jinja2
from ConstantsAndErrorCodes import MyConstants, ErrorCodes
import urllib2
from google.appengine.api import urlfetch
#Jinja Loader
template_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.getcwd()))




class SitemapXMLHandler(webapp2.RequestHandler, MyConstants, ErrorCodes):
    def get(self):
        """
            Consider Dynamically Generating the sitemap from local content on the website everytime the sitemap is called
        :return:
        """
        template = template_env.get_template('templates/sitemap.xml')
        context = {}
        self.response.write(template.render(context))

class RorXMLHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/ror.xml')
        context = {}
        self.response.write(template.render(context))
class RSSHandler(webapp2.RequestHandler):
    def get(self):
        newsfeed = urlfetch.fetch('http://feeds.feedburner.com/FreelancingSolutions',
        allow_truncated=False,
        follow_redirects=False,
        deadline=10)
        newsfeed_xml = newsfeed.content
        self.response.write(newsfeed_xml)

class PodCastHandler(webapp2.RequestHandler):
    def get(self):
        pass

class RobotsTXTHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/robots.txt')
        context = {}
        self.response.write(template.render(context))

class SitemapHTMLHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/sitemap.html')
        context = {}
        self.response.write(template.render(context))




app = webapp2.WSGIApplication([('/sitemap.xml', SitemapXMLHandler),
                               ('/ror.xml', RorXMLHandler),
                               ('/feeds/rss', RSSHandler),
                               ('/feeds/podcasts', PodCastHandler),
                               ('/robots.txt', RobotsTXTHandler),
                               ('/sitemap.html', SitemapHTMLHandler)], debug=True)

