import os
import urllib.request
import ipaddress
import time

# 下载带重试机制的函数
def download_with_retries(url, filename, retries=3, delay=5):
    for attempt in range(1, retries + 1):
        try:
            print(f"正在尝试下载（第 {attempt} 次）...")
            urllib.request.urlretrieve(url, filename)
            print("下载成功。")
            return
        except Exception as e:
            print(f"下载失败: {e}")
            if attempt < retries:
                print(f"{delay} 秒后重试...")
                time.sleep(delay)
            else:
                raise RuntimeError(f"多次重试后仍无法下载 {url}")

# 确保在当前脚本目录下工作
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 下载APNIC数据文件（带重试）
url = "https://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest"
download_with_retries(url, "delegated-apnic-latest")

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
                ip = ipaddress.ip_network(f"{start_ip}/{32 - count.bit_length() + 1}", strict=False)
                cn_ipv4_cidrs.append(str(ip))
            elif parts[2] == "ipv6":
                # IPv6 直接使用提供的前缀长度
                ip = ipaddress.ip_network(f"{start_ip}/{count}", strict=False)
                cn_ipv6_cidrs.append(str(ip))

# 写入结果
with open("cn-ipv4-cidr.txt", "w") as f:
    for cidr in cn_ipv4_cidrs:
        f.write(f"{cidr}\n")

with open("cn-ipv6-cidr.txt", "w") as f:
    for cidr in cn_ipv6_cidrs:
        f.write(f"{cidr}\n")

print("中国IPv4段已生成并保存到 cn-ipv4-cidr.txt")
print("中国IPv6段已生成并保存到 cn-ipv6-cidr.txt")
