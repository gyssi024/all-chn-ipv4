import urllib.request
import ipaddress

# 下载APNIC数据文件
url = "https://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest"
urllib.request.urlretrieve(url, "delegated-apnic-latest")

# 解析文件并提取中国IP段
cn_cidrs = []
with open("delegated-apnic-latest", "r") as f:
    for line in f:
        if line.startswith("apnic|CN|ipv4"):
            parts = line.split("|")
            start_ip = parts[3]
            count = int(parts[4])
            
            # 将IP范围转换为CIDR
            ip = ipaddress.ip_network(f"{start_ip}/{32-count.bit_length()+1}", strict=False)
            cn_cidrs.append(str(ip))

# 将结果写入文件
with open("all_chn_cidr.txt", "w") as f:
    for cidr in cn_cidrs:
        f.write(f"{cidr}\n")

print("中国IP段已生成并保存到 all_cn_cidr.txt")
