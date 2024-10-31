import requests

def download_pdf(pdfId, jwt, output_file):
    url = f'https://e-reserve.lib.pku.edu.cn:8443/api/foxit-pdfview/getPDFURIByPdfId?pdfId={pdfId}'
    headers = {
        'appId': '10029',
        'authorization': jwt,
        'Referer': 'https://e-reserve.lib.pku.edu.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
    }

    # 获取文件大小
    headers['Range'] = 'bytes=0-1'
    response = requests.get(url, headers=headers)

    if response.status_code == 206:
        total_size = int(response.headers['Content-Range'].split('/')[-1])
        print(f"文件大小: {total_size} 字节")

        # 创建输出文件
        with open(output_file, 'wb') as f:
            downloaded_size = 0
            chunk_size = 131072  # 128 KB

            while downloaded_size < total_size:
                # 计算要下载的字节范围
                start = downloaded_size
                end = min(downloaded_size + chunk_size - 1, total_size - 1)
                headers['Range'] = f'bytes={start}-{end}'

                # 下载当前片段
                response = requests.get(url, headers=headers)
                
                if response.status_code == 206:
                    f.write(response.content)
                    downloaded_size += len(response.content)
                    print(f"已下载: {downloaded_size} 字节")
                else:
                    print(f"下载失败，状态码: {response.status_code}")
                    break
    else:
        print(f"无法获取文件大小，状态码: {response.status_code}")

if __name__ == "__main__":
    pdfId = 23712
    jwt = 'eyJhbG..'  # Replace with your JWT

    output_file = f'{pdfId}.pdf'
    download_pdf(pdfId, jwt, output_file)
