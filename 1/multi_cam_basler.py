from pypylon import pylon,genicam
import time

devices = pylon.TlFactory.GetInstance().EnumerateDevices()
for dev in devices:
	print(dev.GetSerialNumber())


camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(devices[0]))


camera.StartGrabbing()
print(camera.IsGrabbing())
n = 0
while n<10:
    n+=1
    grabResult = camera.RetrieveResult(5000,
            pylon.TimeoutHandling_ThrowException)
    if grabResult.GrabSucceeded():
        image = grabResult.Array
        print(image.shape)
        time.sleep(0.02)
    
camera.StopGrabbing()
