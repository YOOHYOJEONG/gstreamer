import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject, GLib


class MyFactory(GstRtspServer, RTSPMediaFactory):
    def __init__(self, **properties):
        super(MyFactory, self).__init__(**properties)
        self.pipeline = f"rtspsrc=rtsp://IP Camera rtsp 주소 latency=0 ! rtph264depay ! rtph264parse ! rtph264pay name=pay0 pt=96"
    
    def do_create_element(self, url):
        return Gst.parse_launch(self.pipeline)


class GstServer(GstRtspServer, GstRtspServer):
    def run(self) :
        factory = MyFactory()
        port = 18550
        rtspServer = GstRtspServer.RTSPServer()
        rtspServer.set_service(str(port))
        factory.set_shared(True)
        mountPoints = rtspServer.get_mount_points()
        mountPoints.add_factory(f'/stream', factory)
        rtspServer.attach(None)