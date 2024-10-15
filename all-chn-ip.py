import urllib.request
import ipaddress
import time

def optimize_cidr(ip_ranges):
    networks = [ipaddress.ip_network(f"{start}/{(end.max_prefixlen - (end._ip - start._ip).bit_length())}", strict=False)
                for start, end in ip_ranges]
    return ipaddress.collapse_addresses(networks)

print("开始下载APNIC数据文件...")
url = "https://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest"
urllib.request.urlretrieve(url, "delegated-apnic-latest")
print("APNIC数据文件下载完成。")

print("开始解析文件并提取中国IP段...")
total_lines = 0
cn_lines = 0
start_time = time.time()
ip_ranges = []

with open("delegated-apnic-latest", "r") as f:
    for line in f:
        total_lines += 1
        if line.startswith("apnic|CN|ipv4"):
            cn_lines += 1
            parts = line.split("|")
            start_ip = parts[3]
            count = int(parts[4])
            
            start = ipaddress.IPv4Address(start_ip)
            end = start + count - 1
            
            ip_ranges.append((start, end))

        if total_lines % 10000 == 0:
            elapsed_time = time.time() - start_time
            print(f"已处理 {total_lines} 行，其中中国IP段 {cn_lines} 个。耗时：{elapsed_time:.2f}秒")

print("正在优化和合并IP段...")
optimized_cidrs = optimize_cidr(ip_ranges)

print("正在写入优化后的IP段...")
with open("all-chn-cidr.txt", "w") as out_f:
    for cidr in optimized_cidrs:
        out_f.write(f"{cidr}\n")

end_time = time.time()
total_time = end_time - start_time
print(f"处理完成！总共处理了 {total_lines} 行，提取了 {cn_lines} 个中国IP段。")
print(f"总耗时：{total_time:.2f}秒")
print("优化后的中国IP段已生成并保存到 all-chn-cidr.txt")
