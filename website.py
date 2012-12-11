#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, signal
from subprocess import Popen, PIPE
from string import Template
import cherrypy

DIRECTORY = os.path.join(os.path.abspath("."), u"html")

## jquery_url = os.path.join(DIRECTORY, 'jquery.min.js')
## jquery_ui_url = os.path.join(DIRECTORY, 'jquery-ui.min.js')
## jquery_ui_css_url = os.path.join(DIRECTORY, 'jquery-ui.css')

jquery_url = 'http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js'
jquery_ui_url = 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/jquery-ui.min.js'
jquery_ui_css_url = 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/themes/black-tie/jquery-ui.css'

class MainPage(object):
    test = None
    
    @cherrypy.expose
    def index(self):
        html = open(os.path.join(DIRECTORY, 'index.html'), "r").read()
        t = Template(html)
        page = t.substitute(
            jquery_ui_css_url=jquery_ui_css_url,
            jquery_url=jquery_url,
            jquery_ui_url=jquery_ui_url)
        return page


    @cherrypy.expose
    def startCrawl(self, url, stopVal, depth, **kw):
        command = "python runCrawler.py %s %s %s" % (url, stopVal, depth)
        scroll_to_bottom = '<script type="text/javascript">window.scrollBy(0,50);</script>'
        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE,
                        close_fds=True, preexec_fn=os.setsid)

        cherrypy.session['pid'] = process.pid
        cherrypy.session.save()
        def run_command():
            all_txt = ""
            yield '<style>body {font-family: monospace;}</style>'
            while not process.poll():
                out = process.stdout.read(1) 
                if out == '\n': 
                    out = "\n<br />%s" % scroll_to_bottom 
                yield out 
                all_txt += out
            MainPage.test = all_txt[-88:]
            out = ""
            for char in process.stdout.read():
                if char == "\n":
                    out += "\n<br />%s" % scroll_to_bottom
                else:
                    out += char
            yield out
        #val = run_command()
        #self.path = val[-10:]
        return run_command()
        
    startCrawl._cp_config = {'response.stream': True}

    @cherrypy.expose
    def displayGraph(self, **kw):
        img = """"img/""" + str(int(MainPage.test[9:19])) + """.png" """
        val =  "<img src=" + img + """width="100%" alt="No graph to display."</img>"""
        return val
        #return str(MainPage.test)
    
    @cherrypy.expose
    def killCrawl(self, **kw):
        pid = cherrypy.session.get('pid')
        if not pid:
            return "No crawl to kill"
        try:
            os.killpg(pid, signal.SIGINT)
        except OSError:
            pass
        return "The crawl was stopped."

cherrypy.config.update({
    'log.screen':True,
    'tools.sessions.on': True,
    'checker.on':False
})

conf = {'/img': {'tools.staticdir.on': True,
                 'tools.staticdir.dir': os.path.join(DIRECTORY, 'img'),
                      }}

cherrypy.tree.mount(MainPage(), config=conf)
cherrypy.engine.start()
cherrypy.engine.block()

