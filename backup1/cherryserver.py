import cherrypy
import os
import os.path
import gobotov5



class HelloWorld(object):
    def index(self):
        s='''
           Navigate to /boto to populate autoscale values from a web form <br> <br> 
       '''
        s+=os.popen('hostname').readline()
        return s
    index.exposed = True



class boto(object):
    global akid, sac, lcname, asgname, amiid, loadbalancer

    def index(self):
        output=""
        f=open("boto.html",'r').read().split('\n')
        for l in f:
            output+=l+'\n'
        return output
    index.exposed=True
	
	
    def upload(index, akid=None, sac=None, lcname=None, asgname=None, amiid=None, loadbalancer=None):   
		output=""
		output+='<input id="hostname" type="text" value="'+os.popen('hostname').readline()+'"\n>'
		output+= akid + " " + sac + " " +lcname + " " + asgname + " " + amiid + " " + loadbalancer
		return output
		# this function is hooked up to the input form called upload in boto.html; submit passes the values above. they are global variables for goboto-v5.py
    upload.exposed = True
	
class botojs(object):

    def index(self):
        output=""
        f=open("boto.js",'r').read().split('\n')
        for l in f:
            output+=l+'\n'
        return output
    index.exposed = True

    def navigation(self):
        output=""
        f=open("navigation.js",'r').read().split('\n')
        for l in f:
            output+=l+'\n'
        return output
    navigation.exposed = True

    def one(self):
        output=""
        f=open("one.js",'r').read().split('\n')
        for l in f:
            output+=l+'\n'
        return output
    one.exposed = True

    def two(self):
        output=""
        f=open("two.js",'r').read().split('\n')
        for l in f:
            output+=l+'\n'
        return output
    two.exposed = True

    def three(self):
        output=""
        f=open("three.js",'r').read().split('\n')
        for l in f:
            output+=l+'\n'
        return output
    three.exposed = True
		
    def four(self):
        output=""
        f=open("four.js",'r').read().split('\n')
        for l in f:
            output+=l+'\n'
        return output
    four.exposed = True

    def style(self):
        output=""
        f=open("style.css",'r').read().split('\n')
        for l in f:
            output+=l+'\n'
        return output
    style.exposed = True

    def jquery171min(self):
        output=""
        f=open("jquery171min",'r').read().split('\n')
        for l in f:
            output+=l+'\n'
        return output
    jquery171min.exposed = True

    def jquerydropotron10(self):
        output=""
        f=open("jquerydropotron10",'r').read().split('\n')
        for l in f:
            output+=l+'\n'
        return output
    jquerydropotron10.exposed = True


root=HelloWorld()
root.boto=boto()
root.botojs=botojs()

cherrypy.config.update({'server.socket_host':'0.0.0.0','server.socket_port':8080})
cherrypy.quickstart(root)
