# Simple orbbec astra example
# Detect connexion/disconnexion of a device
# If a device is connected, open a stream and show fps
# It dosnt read frames content


import os
from openni import openni2
from time import sleep
from threading import Lock, Event

class DeviceListener(openni2.DeviceListener):
    def __init__(self):
        self._lock  = Lock()
        self._event = Event()
        self._cnt   = len(openni2.Device.enumerate_uris())
        if self._cnt > 0: self._event.set()
        openni2.DeviceListener.__init__(self)

    def on_connected(self, devinfo):
        print('New Device: %s %s' % (
            devinfo.vendor.decode('ascii'), 
            devinfo.name.decode('ascii')))
        with self._lock:
            self._cnt += 1
            self._event.set()

    def on_disconnected(self, devinfo):
        print('Lost Device: %s %s' % (
            devinfo.vendor.decode('ascii'), 
            devinfo.name.decode('ascii')))

        with self._lock:
            self._cnt -= 1
            if self._cnt == 0:
                self._event.clear()
    
    def __bool__(self):
        return self._cnt > 0
    
    def wait_for_connection(self, timeout=None):
        return self._event.wait(timeout)
# #####################################


class FrameCounter:
    def __init__(self):
        self._lock  = Lock()
        self._count = 0
    
    def clear(self):
        with self._lock:
            self._count = 0
    
    def increment(self):
        with self._lock:
            self._count += 1

    @property
    def count(self):
        return self._count
# #####################################    


try:
    # init openni
    openni2.initialize()
    print('Openni2 initialized')
    # init variables
    device          = None
    stream          = None
    frame_counter   = FrameCounter()
    device_listener = DeviceListener()

    while True:
        if device is None:
            if device_listener.wait_for_connection():
                try:
                    device = openni2.Device.open_any()
                except Exception as what:
                    print('Error openning device: %s' % what.__class__.__name__)
                    print('\t%s' % what)
                    device = None
                    sleep(1.0)
                else:
                    print('Device openned')
                    stream = device.create_depth_stream()
                    stream.set_video_mode(
                        openni2.c_api.OniVideoMode(
                            pixelFormat = openni2.c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, 
                            resolutionX = 640, 
                            resolutionY = 480, 
                            fps         = 30
                        )
                    )
                    stream.set_mirroring_enabled(0)
                    stream.register_new_frame_listener(lambda _: frame_counter.increment())
                    stream.start()
                    print('Stream started')
            else:
                print('No device at the moment')

        elif device_listener:
            frame_counter.clear()
            sleep(1.0)
            print('Fps: %d' % frame_counter.count)

        else:
            stream.unregister_all_new_frame_listeners()
            stream.stop()
            stream = None
            print('Stream closed')
            device.close()
            device = None
            print('Device closed')

except KeyboardInterrupt:
    print('Stopped with Ctrl+C')

finally:
    if stream is not None:
        stream.unregister_all_new_frame_listeners()
        stream.stop()
        stream = None
        print('Stream closed')
    if device is not None:
        device.close()
        device = None
        print('Device closed')
    if openni2.is_initialized():
        openni2.unload()
        print('Openni unloaded')
