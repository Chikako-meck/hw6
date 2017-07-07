    #!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgi
import urllib

from google.appengine.api import users
import webapp2
import sys

MAIN_PAGE_HTML = """\
    <form action="/pata" method="post">
        <input type="text" name="a">
        <br>
        <input type="text" name="b">
        <br>
        <input type="submit" value="送信">
    </form>
    """

class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.write('<html><head><link type="text/css" rel="stylesheet" href="/stylesheets/main.css" /></head><body>')
        self.response.write(MAIN_PAGE_HTML)
        self.response.write('</html></body>')

class Guestbook(webapp2.RequestHandler):

    def post(self):
        # self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        # self.response.write('Hello, world!')

        a = self.request.get('a')
        b = self.request.get('b')
        a_list = list(a)
        b_list = list(b)
        a_len = len(a_list)
        b_len = len(b_list)
        output_list = []
        if a_len!=0 or b_len != 0:
            if a_len < b_len:
                for i in range(a_len):
                    output_list.append(a_list[i])
                    output_list.append(b_list[i])
                output_list.append("".join(b_list[i+1:]))
            else:
                for i in range(b_len):
                    output_list.append(a_list[i])
                    output_list.append(b_list[i])
                output_list.append("".join(a_list[i+1:]))

            output = "".join(output_list)
        else:
            output = ""

        self.response.write('<html><body><pre>')
        self.response.write('<font size="+10">' + cgi.escape(output) + '</font></pre>')
        self.response.write(MAIN_PAGE_HTML)
        self.response.write('</body></html>')
        param = [('a', a), ('b', b)]
        # self.redirect('/pata?')# + urllib.urlencode(param, 'sjis'))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/pata', Guestbook),
], debug=True)
