import argparse
import os
import tempfile
import time
from urllib.request import urlopen

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('urls',metavar='URL',nargs='+', help='URL to download')
    parser.add_argument('--output-dir', help='Directory to use for downloaded files')

    methods = parser.add_argument_group('Download methods')
    methods.add_argument('--all',action='store_true', help='All download methods')
    methods.add_argument('--request',action='store_true')

    debugging = parser.add_argument_group('Debugging')
    debugging.add_argument('--null', action='store_true', help='Null download')

    return parser.parse_args()

def download():
    if args.null:
        time_download(null)

def stats(bytes, seconds, url):
    mb = bytes/1e6
    print('    {:5.2f} MB/s, {:5.2f} MB, {:5.2f} seconds, URL: {}'.format(mb/seconds, mb, seconds, url), flush=True)

def time_download(fun, block_size = 0):
    name = '{}-{:.2f}'.format(fun.__name__,block_size/M)
    print('Timing {}'.format(name))
    total_bytes = 0
    total_seconds = 0
    for url in args.urls:
        file = os.path.join(output_dir,name)
        start = time.time()
        fun(url, file, block_size)
        seconds = time.time() - start
        bytes = os.path.getsize(file)
        stats(bytes, seconds, url)
        total_bytes = total_bytes + bytes
        total_seconds = total_seconds + seconds
    stats(total_bytes, total_seconds, 'ALL')
    
#
# Download methods
#
def null(url, file, block_size):
    with open(file,'w') as fout:
        fout.write('xxxxxxxxxx')

def request(url, file, block_size):
    response = urlopen(url)
    with open(file, 'wb') as f:
        while True:
            chunk = response.read(block_size)
            if not chunk:
                break
            f.write(chunk)

if __name__ == "__main__":
    args = parse_args()
    M = 1024 * 1024

    with tempfile.TemporaryDirectory() as output_dir:
        if args.output_dir:
            output_dir = args.output_dir
        if args.null:
            time_download(null)
        if args.request:
            for block_size in [1 * M, 2 * M, 4 * M, 8 * M, 16 * M]:
                time_download(request, block_size)