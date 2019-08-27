import time
import BaseHTTPServer
import os


HOST_NAME = '192.168.1.10' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        datahora = os.popen('TZ=UTC+3 date').read()
        uptime = os.popen('uptime').read().replace("\xc3", "")
        cpu = os.popen('cat /proc/cpuinfo | grep "model name"').read().replace("model name : ", "") + " @ " + os.popen('cat /proc/cpuinfo | grep "cpu MHz"').read().replace("cpu MHz : ", "") + " MHz"
        cpu = cpu.replace("model name", "").replace("cpu MHz", "").replace(":", "")
        cpu_usage = os.popen('grep \'cpu \' /proc/stat | awk \'{usage=($2+$4)*100/($2+$4+$5)} END {print usage "%"}\'').read()
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>Title goes here.</title></head>")
        s.wfile.write("<body><p>This is a test.</p>")
        s.wfile.write("<p>Data e Hora: %s</p>" % datahora)
        s.wfile.write("<p>Uptime: %s</p>" % uptime)
        s.wfile.write("<p>CPU: %s</p>" % cpu)
        s.wfile.write("<p>CPU usage: %s</p>" % cpu_usage)
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        s.wfile.write("<p>You accessed path: %s</p>" % s.path)
        s.wfile.write("</body></html>")

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

