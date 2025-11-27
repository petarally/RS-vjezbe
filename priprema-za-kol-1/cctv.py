import aiohttp

class CCTV_frame:
    # konstruktor
    def __init__ (self, frame_id, location_x, location_y, frame_rate, camera_status, zoom_level, ip_address):
        self.frame_id = frame_id
        self.location_x = location_x
        self.location_y = location_y
        self.frame_rate = frame_rate
        self.camera_status = camera_status
        self.zoom_level = zoom_level
        self.ip_address = ip_address

    def info(self):
        print(f"Frame ID: {self.frame_id}, Location: ({self.location_x}, {self.location_y}), Frame rate: {self.frame_rate}, Camera status: {self.camera_status}, Zoom level: {self.zoom_level}, IP address: {self.ip_address}")