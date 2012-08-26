import cherrypy
import os



class HelloWorld(object):
    def index(self):
        s='''
           Navigate to /boto to populate autoscale values from a web form <br> <br>
           

        '''
        s+=os.popen('hostname').readline()
        return s
    index.exposed = True

class botojs(object):
    def index(self):
        output=""
        f=open("boto.js",'r').read().split('\n')
        for l in f:
            output+=l+'\n'
        return output
    index.exposed = True

class boto(object):
    global c

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
    upload.exposed = True

    

root=HelloWorld()
root.boto=boto()
root.botojs=botojs()

cherrypy.config.update({'server.socket_host':'0.0.0.0','server.socket_port':8080})
cherrypy.quickstart(root)
