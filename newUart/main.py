from SerialConnection import SerialConnection

data = [255, 255, 255, 255]
se = SerialConnection(port='/dev/ttyS0', baudrate=115200)
se.sendData(data)
se.closeConnection()