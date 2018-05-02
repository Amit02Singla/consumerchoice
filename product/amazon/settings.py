import os

current_dir = os.path.dirname(os.path.realpath(__file__))

# Database
database = "amazon_crawler"
host = ""
user = ""

# Redis
redis_host = "localhost"
redis_port = 6379
redis_db = 0

# Request
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
}
allowed_params = ["node", "rh", "page"]

# Proxies
proxies = [

    'http://103.228.119.125:8080', 'http://89.236.17.106:3128', 'http://153.149.171.26:3128',
     'http://51.15.65.152:8080', 'http://159.65.0.210:3128', 'http://185.93.3.123:3128'
]
proxy_user = ""
proxy_pass = ""
proxy_port = ""

# Crawling Logic
start_file = os.path.join(current_dir, "start-urls.txt")
max_requests = 2 * 10**6  # two million
max_details_per_listing = 9999

# Threads
max_threads = 200

# Logging & Storage
log_stdout = True
image_dir = "/tmp/crawl_images"
export_dir = "/tmp"
