import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject, GLib


if __name__ == '__main__':
    loop = GLib.MainLoop()
    GObject.threads_init()
    Gst.init(None)

    class RTSPFactory(GstRtspServer, RTSPMediaFactory):
        def __init__(self, **properties):
            # super(MyFactory, self).__init__(**properties)
            # self.pipeline = f"rtspsrc=rtsp://IP Camera rtsp 주소 latency=0 ! rtph264depay ! rtph264parse ! rtph264pay name=pay0 pt=96"
            GstRtspServer.RTSPMediaFactory.__init__(self)
        
        def do_create_element(self, url):
            pipeline = "rtspsrc location=rtsp://<IP Camera rtsp address> latency=0 ! rtph264depay ! h264parse ! rtph264pay name=pay0 pt=96"    # h264 format -> h264 format
            return Gst.parse_launch(pipeline)

    class GstServer():
        def __init__(self):
            self.server = GstRtspServer.RTSPserver()
            self.server.set_service("8550")   # rtsp 스트리밍 포트 번호
            factory = RTSPFactory()
            factory.set_shared(True)
            mount = self.server.get_mount_points()
            mount.add_factory("/test", factory)   # rtsp 주소에 들어갈 서브 url string
            self.server.attach(None)

    server = GstServer()
    loop.run()


# class MyFactory(GstRtspServer, RTSPMediaFactory):
#     def __init__(self, **properties):
#         super(MyFactory, self).__init__(**properties)
#         self.pipeline = f"rtspsrc=rtsp://IP Camera rtsp 주소 latency=0 ! rtph264depay ! rtph264parse ! rtph264pay name=pay0 pt=96"
    
#     def do_create_element(self, url):
#         return Gst.parse_launch(self.pipeline)


# class GstServer(GstRtspServer, GstRtspServer):
#     def run(self) :
#         factory = MyFactory()
#         port = 18550
#         rtspServer = GstRtspServer.RTSPServer()
#         rtspServer.set_service(str(port))
#         factory.set_shared(True)
#         mountPoints = rtspServer.get_mount_points()
#         mountPoints.add_factory(f'/stream', factory)
#         rtspServer.attach(None)