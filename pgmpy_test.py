from pgmpy.readwrite import BIFReader
reader = BIFReader("./models/LOCA.bif")
print(reader.get_network_name())