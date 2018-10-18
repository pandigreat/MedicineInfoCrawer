name = 'proxy_ips.txt'
names = 'ips.txt'
rs = []
with open(name, 'r') as file:
    for line in file:
        rs.append(line.split('@')[0])
with open(names, 'w') as fp:
    for line in rs:
        fp.write(line + '\n')