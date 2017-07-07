#!/usr/bin/env python
# coding: utf-8
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2
import sys

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def read_station(filename):
    file = open(filename)
    stations_with_line = []
    stations = []
    for l in file.readlines():
        stations_line = l.split()
        line = stations_line[0]
        for i in range(1, len(stations_line)):
            station = stations_line[i]
            station_with_line = station
            stations_with_line.append(station_with_line)
            if station not in stations:
                stations.append(station)
    return stations_with_line, stations


def make_stations_graph(stations_with_line, stations):
    graph = {}
    length = len(stations)
    for i in range(length):
        relation_list = []
        indexes = [index for index, x in enumerate(stations_with_line) if x == stations[i]]
        for k in range(len(indexes)):
            index = indexes[k]
            if index == 0:
                relation_list.append(stations_with_line[index+1])
            elif index == (len(stations_with_line)-1):
                relation_list.append(stations_with_line[index-1])
            else :
                relation_list.append(stations_with_line[index-1])
                relation_list.append(stations_with_line[index+1])
        graph[stations[i]] = relation_list
    relations_shinagawa = graph.get('品川')
    relations_shinagawa.pop(len(relations_shinagawa)-1)
    return graph


def search_root(station_from, station_to, graph):
    stack = [station_from]
    visited = []
    while stack:
        label = stack.pop(0)
        if label == station_to:
            visited.append(label)
            return visited
        if label not in visited:
            visited.append(label)
            stack = graph.get(label, []) + stack
    return visited


class MainPage(webapp2.RequestHandler):

    def get(self):
        stations_with_line, stations = read_station("net.txt")
        self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        self.response.write('<html>')
        self.response.write('<head><title>乗り換え検索</title></head>')
        self.response.write('<body><form action="/transit" method="post"><div>出発駅: <select name="from">')
        for i in range(len(stations)):
            station = stations_with_line[i]
            self.response.write('<option value="%s">%s</option>, charset:=utf-8' % (station,station))
        self.response.write('</select></div>')
        self.response.write('<div>到着駅: <select name="to">')
        for i in range(len(stations)):
            station = stations[i]
            self.response.write('<option value="%s">%s</option>, charset:=utf-8' % (station, station))
        self.response.write('</select></div>')
        self.response.write('<div><input type="submit" value="検索"></div>')
        self.response.write('</form></body></html>')


class Transit(webapp2.RequestHandler):

    def post(self):
        stations_with_line, stations = read_station("net.txt")
        station_from = self.request.get('from').encode('UTF-8')
        station_to = self.request.get('to').encode('UTF-8')
        graph = make_stations_graph(stations_with_line, stations)
        root = search_root(station_from, station_to, graph)

        length = len(root)

        self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        self.response.write('<html>')
        self.response.write('<head><title>乗り換え検索</title></head>')
        self.response.write('<body><h3>検索結果</h3>')
        self.response.write('<div>')
        for i in range(length):
            station = root[i]
            self.response.write('%s<br>' % station)
        self.response.write('</div></body>')
        self.response.write('</html>')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/transit', Transit)
], debug=True)
