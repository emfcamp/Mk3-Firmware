import stm

r1 = stm.mem32[0x1FFF7590]
r2 = stm.mem32[0x1FFF7594]
r3 = stm.mem32[0x1FFF7598]

print("X coord: " + str(r1 & 0xFFFF) + "   Y coord: " + str(r1>>16))
print("Wafer: " + str(r2 & 0xFF))
print("Lot: " + chr(r3>>24) + chr((r3>>16)&0xFF) + chr((r3>>8)&0xFF) + chr(r3&0xFF) +   chr(r2>>24) + chr((r2>>16)&0xFF) + chr((r2>>8)&0xFF))
