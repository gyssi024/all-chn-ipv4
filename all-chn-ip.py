import os
import urllib.request
import ipaddress

# 确保在正确的目录中操作
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 下载APNIC数据文件
url = "https://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest"
urllib.request.urlretrieve(url, "delegated-apnic-latest")

# 解析文件并提取中国IP段
cn_ipv4_cidrs = []
cn_ipv6_cidrs = []

with open("delegated-apnic-latest", "r") as f:
    for line in f:
        if line.startswith("apnic|CN|ipv"):
            parts = line.split("|")
            start_ip = parts[3]
            count = int(parts[4])
            
            if parts[2] == "ipv4":
                # 将IPv4范围转换为CIDR
                ip = ipaddress.ip_network(f"{start_ip}/{32-count.bit_length()+1}", strict=False)
                cn_ipv4_cidrs.append(str(ip))
            elif parts[2] == "ipv6":
                # 将IPv6范围转换为CIDR
                ip = ipaddress.ip_network(f"{start_ip}/{count}", strict=False)
                cn_ipv6_cidrs.append(str(ip))

# 将结果写入文件
with open("cn-ipv4-cidr.txt", "w") as f:
    for cidr in cn_ipv4_cidrs:
        f.write(f"{cidr}\n")

with open("cn-ipv6-cidr.txt", "w") as f:
    for cidr in cn_ipv6_cidrs:
        f.write(f"{cidr}\n")

print("中国IPv4段已生成并保存到 cn-ipv4-cidr.txt")
print("中国IPv6段已生成并保存到 cn-ipv6-cidr.txt")
