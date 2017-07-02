    #!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgi
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
        self.response.write('<html><body>')
        self.response.write(MAIN_PAGE_HTML)
        self.response.write('</html></body>')

class Guestbook(webapp2.RequestHandler):

    def post(self):
        # self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        # self.response.write('Hello, world!')

        a = list(self.request.get('a'))
        b = list(self.request.get('b'))
        a_len = len(a)
        b_len = len(b)
        output_list = []
        if a_len!=0 or b_len != 0:
            if a_len < b_len:
                for i in range(a_len):
                    output_list.append(a[i])
                    output_list.append(b[i])
                output_list.append("".join(b[i+1:]))
            else:
                for i in range(b_len):
                    output_list.append(a[i])
                    output_list.append(b[i])
                output_list.append("".join(a[i+1:]))

            output = "".join(output_list)
        else:
            output = ""

        self.response.write('<html><body><pre>')
        self.response.write('<font size="+10">' + cgi.escape(output) + '</font></pre>')
        self.response.write(MAIN_PAGE_HTML)
        self.response.write('</body></html>')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/pata', Guestbook),
], debug=True)
