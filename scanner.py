import ping


connected_devices = []

for i in range(1,254):
        ip = "192.168.0." + str(i)
        ans = str(ping.quiet_ping(ip, 0.003, 1))
        #print(ans(0))
        if ans[1] == "0":
                connected_devices.append(ip)

print("connected devices: ")
for adress in connected_devices:
        print(adress)




