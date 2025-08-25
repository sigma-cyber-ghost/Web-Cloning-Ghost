#!/usr/bin/env python3
import os 
import sys
import requests
import random
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import socks
import socket
import re
from fnmatch import fnmatch

class SigmaGhostCloner:
    def __init__(self):
        self.banner = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠃⠈⠘⠋⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠆⠀⠀⡀⡄⠀⠀⠀⠂⠀⠀⠀⠀⠘⣳⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠄⠀⠀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢡⣿⡷⠀⠠⣜⢳⡄⢠⡀⠈⠁⠄⣀⠀⠀⠀⠀⠀⠀⠀⡀⢀⠀⠈⠀⠁⠀
⠀⠀⠀⠀⠀⠐⠀⠀⢻⠄⡈⠄⠀⠂⠀⠀⠀⠀⣠⠊⡌⠀⠀⠀⣧⡌⠄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⠀⢱⠐⠄⣬⠁⠀⠀⠘⢏⠀⠀⠀⠈⠦⠀⠐⠀⠠⠐⠀⠂⠀⠄
⠀⠀⠀⠀⠀⠀⠀⠀⠠⠁⠄⡐⠀⠠⠀⠀⠀⣰⠃⠀⠉⡽⠀⠀⡏⠳⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢟⠋⢀⡈⢮⡟⠆⠀⠀⠀⠀⠀⡐⠠⢀⠀⠂⠈⢀⠀⠁⠐⠀⡀
⠀⠀⠀⠀⠀⠀⠀⠄⣾⣆⡁⠐⠠⠀⢀⠀⢀⡇⢀⠂⡜⠡⠄⡀⠇⠀⢈⣐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢢⠀⠘⣼⡄⠀⠀⠀⠀⠄⠐⠠⢁⢸⣷⣦⣅⡀⡼⡄⠀⢂⠀
⠀⠀⠀⠀⠀⠀⠈⠄⢼⢟⠁⠌⠀⣈⡀⢀⠀⣧⠎⡔⢣⡀⠀⠄⢰⣿⣈⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠸⣰⣸⠁⠀⠀⢀⠐⠀⢈⠐⠠⢸⣿⣿⣿⣿⣖⡄⠐⠀⢂
⠀⠀⠀⠀⠀⠀⠀⠀⠡⠁⠀⠀⠀⠈⠉⠀⠀⠸⣞⢭⣫⢳⣄⡀⠸⠟⣋⣁⣠⣤⣤⣤⣤⣤⣄⣀⣀⠀⠀⢀⣠⡾⣡⠿⣱⠏⠀⠀⠀⠲⠀⡀⠀⠌⡐⢸⣿⣿⣿⣿⣿⠿⢶⣀⠡
⠀⢤⣆⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠁⠀⢈⢣⡝⣯⢎⣛⠶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡶⠟⣵⠺⣭⠟⠁⠀⢀⠀⠀⢀⠐⠠⠐⣦⡀⠀⣿⣿⢯⣛⠷⡈⠀⡽⢶
⠀⠈⠁⠀⠀⠀⠀⠀⢀⠁⡀⠄⠠⢀⠀⠀⠀⠈⠄⡂⠌⡓⠽⣎⢶⡐⡈⢍⠛⢛⠛⠟⡛⢛⡛⢛⠫⡐⣎⣳⡸⠟⠁⢀⠀⠄⠂⠌⡀⠂⢌⣤⣒⣷⣿⡄⠙⡿⣟⠄⢛⢠⣦⣬⢜
⣀⠀⣶⣿⠠⣁⢂⠀⠄⣢⣴⠈⡅⢢⠘⡄⠡⠐⢈⠔⡡⠒⣴⣿⣯⣷⣙⢦⡩⢆⣍⢲⣡⢣⡜⣡⢇⣳⣞⣁⣡⠀⡔⠂⡌⠤⢁⠊⠄⠡⠈⣿⣿⣿⣿⣿⡰⣝⣷⣾⣄⣸⣿⣿⣿
⠹⣼⠵⣉⣶⣽⣎⢮⣳⣝⡃⠜⣠⠃⡜⣠⠃⡌⠐⣎⡱⡁⣿⣿⣿⠟⠛⠚⢵⣯⣞⣷⣮⣷⡽⠃⠛⠳⢿⣿⣿⠘⣌⠳⣄⢨⣤⣈⡆⣥⣁⢹⣿⣿⣿⣿⣿⣯⡮⡈⠹⡸⣿⣟⣿
⠀⠰⡹⡿⢻⣯⡿⣫⣵⣷⣿⣲⠠⡙⠴⣡⢚⠤⣃⠼⣱⠃⡿⣿⠁⠀⠀⠀⠀⢿⣿⣿⣿⡿⠀⠀⠀⠀⠈⣿⣿⠐⢦⡱⢈⠎⣻⣿⣷⣽⣿⣿⣽⣿⣏⠻⣿⣝⠤⠙⡳⠲⢿⣏⡖
⠀⠀⠃⠔⢣⡙⡓⣾⣿⣿⣿⣧⠳⡌⠸⣥⢋⡾⢄⠻⣵⣃⢻⢿⡀⠀⠀⠀⠀⢘⣿⣿⣿⡇⠀⠀⠀⠀⢀⣧⡿⢈⡳⡘⢥⢊⡔⣩⢻⣟⡿⣿⣿⣷⡹⠆⡌⠻⣄⠫⡒⠛⠀⢫⠆
⠀⠀⠡⡈⣄⢒⣼⣿⣿⣻⢿⣿⣛⡴⢃⣎⠿⣜⣣⡙⢶⣻⠸⡿⣧⡀⠀⠀⠀⣸⣿⣿⣿⣧⠀⠀⠀⠀⣼⣿⡇⢭⠓⡭⢂⡝⢰⣅⡞⡌⣙⡾⡿⣿⣿⣜⠰⢁⣦⡆⠀⢤⣤⡴⡃
⠀⡌⢦⣱⣮⣞⢟⣵⡞⣿⣯⢖⡽⣜⠣⣌⠿⣹⢦⡙⣦⢣⢇⡹⣿⡿⡦⣤⣶⣿⣿⣿⣿⣿⣶⣤⣴⣾⣷⠏⣌⠶⣹⢖⢧⠪⠽⣻⣿⣗⣦⣺⠗⡍⣿⣿⣷⢼⣿⡇⠀⠀⠐⠁⠘
⡜⡬⣶⡾⣏⠬⢛⣶⣿⣿⣿⣿⡲⣍⣳⣬⢻⣵⣞⣻⢶⣯⢞⣵⣪⡥⠓⠾⠿⠿⠿⠿⡿⠿⠿⠿⠿⠛⢩⡱⣞⡼⣋⠓⠫⣮⣝⣳⣹⣿⢿⣞⢻⣿⣾⡹⣿⣿⣿⣿⡀⢀⣆⠀⠀⡄
⡼⢭⡽⣻⠽⣷⣾⣫⡻⣿⣿⣿⣽⢳⣯⣷⣯⣿⣯⣿⣿⡿⠾⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠙⠻⠽⠯⣵⡷⣏⣶⢷⡽⢿⢯⡳⣍⡻⣏⡿⣿⣿⣿⣿⣎⠳⣧⠀⠇
⢀⡗⣾⣿⡷⢿⡔⡚⡷⣿⣿⣟⣮⣿⣽⣿⣷⡿⠟⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠉⠙⠾⣯⣛⣷⡳⣣⡻⢿⡌⢻⣝⢿⣿⣿⣷⢘⠝⣇⣦
⠢⢜⡱⢯⢿⣿⡷⠙⡌⣽⣿⣿⣿⣿⣿⣿⢏⠔⠁⠀⠀⠀ SIGMA-CYBER-GHOST⠀⠀      ⠀⠀⠀⠀⠈⠗⠲⢶⣿⡻⠁⠀⠈⢫⠂⡙⢿⣿⠅⠈⠂⠀
⠑⢢⡑⡫⠞⠅⠁⢄⣴⢵⣟⣼⢟⢿⣿⠏⣠⡴⠀⠀⡀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠈⢻⣷⣦⣷⣕⢶⠄⠄⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀
⠀⠀⠁⢠⣄⣤⣶⣿⣿⣾⣿⣿⠜⣿⣿⣞⡋⠀⡠⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠀⠀⠀⠁⢄⢻⡿⢫⣮⠀⠀⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠠⠀⠂⣊⢿⡿⢟⣛⡿⢿⡟⣀⠛⠛⠉⠀⠘⣠⣾⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠂⠄⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⣄⢢⡸⣭⣞⣴⣦⡀⠙⠀⢀⢀⢀⠄⠠⠐⠠⠀⠀
⠀⠀⢀⠀⠠⡃⢺⣮⢛⠿⣿⣶⣽⡻⣿⡿⢿⢡⡿⡏⣸⠀⠀⠀⠀⣤⠀⠀⠀⠀⠈⠆⠈⠒⢄⡀⢈⡰⢀⠰⣦⠀⠀⡀⠀⠀⠉⠁⠒⡒⠊⠛⠋⣀⠤⠒⠐⢈⢸⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠐⠀⠰⣌⣹⢘⡎⢗⢴⡲⠳⣎⢠⣝⡴⡫⠿⣿⡆⢰⣄⠈⠿⣇⠀⠀⠀⠀⣿⡆⠀⠀⠀⢰⣿⣶⣄⠱⣯⡆⣰⣶⢰⡄⠀⢄⣟⡀⣠⠞⠁⠀⠀⠀⢺⠃⠘⠀⠀⠀⠀⠀
⣠⢴⡚⠞⠿⠃⠩⢹⢿⣿⣿⣷⠗⡪⢌⡈⠻⢿⣿⣾⣷⣶⡤⣭⣝⣛⡻⢇⠀⠀⠀⣿⣿⠀⠀⠀⣾⣿⠏⢠⢶⢏⣾⣿⠟⠁⠀⢀⣀⣉⣐⣃⡈⠀⠀⠀⠀⠈⠄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠐⠀⠀⠐⠈⠃⠒⠀⠂⠌⠐⡁⠚⡽⢾⢷⣝⡯⠑⢂⢉⡈⡭⣉⠑⠀⠀⠀⠺⠒⠀⠀⠸⠉⢒⢂⡷⡡⠾⣒⡭⣖⠲⠍⢋⣪⠗⡪⡖⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠄⣒⠄⢤⣶⡷⡶⠶⢦⠤⠀⠄⡀⠁⠀⠂⠁⠈⠄⠀⠀⠀⣀⢠⠠⠄⠂⠀⠈⠑⠋⠀⠐⠲⡐⠂⠋⠀⠀⠘⠁⠓⠈⠁⠘⠰⠨⢡⠃⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        """
        self.colors = {
            'green': '\033[92m',
            'red': '\033[91m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'cyan': '\033[96m',
            'bold': '\033[1m',
            'end': '\033[0m'
        }
        self.font_counter = 1
        self.resource_total = 0
        self.resource_done = 0
        self.proxy_config = None
        self.session = None
        
        # Enhanced browser headers to mimic real user
        self.headers_list = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0',
            },
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0',
            },
            {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0',
            }
        ]

    def print_banner(self):
        print(f"{self.colors['green']}{self.banner}{self.colors['end']}")
        print(f"{self.colors['bold']}{self.colors['cyan']}Sigma Ghost Website Cloner{self.colors['end']}")
        print(f"{self.colors['yellow']}Connect with me:{self.colors['end']}")
        print(f"{self.colors['cyan']}  Twitter : https://twitter.com/safderkhan0800_{self.colors['end']}")
        print(f"{self.colors['cyan']}  YouTube : https://www.youtube.com/@sigma_ghost_hacking{self.colors['end']}")
        print(f"{self.colors['cyan']}  YouTube : https://www.youtube.com/@Sigma-Cyber-Ghost{self.colors['end']}")
        print(f"{self.colors['cyan']}  Telegram: https://t.me/Sigma_Cyber_Ghost{self.colors['end']}")
        print(f"{self.colors['cyan']}  GitHub  : https://github.com/sigma-cyber-ghost{self.colors['end']}\n")

    def print_error(self, message):
        print(f"{self.colors['red']}[!] ERROR : {message}{self.colors['end']}")

    def print_success(self, message):
        print(f"{self.colors['green']}[+] SUCCESS : {message}{self.colors['end']}")

    def print_info(self, message):
        print(f"{self.colors['cyan']}[i] INFO : {message}{self.colors['end']}")

    def print_processing(self, message):
        print(f"{self.colors['yellow']}[>] PROCESSING : {message}{self.colors['end']}")

    def print_saved(self, message):
        print(f"{self.colors['blue']}[~] SAVED : {message}{self.colors['end']}")

    def setup_proxy(self):
        print(f"\n{self.colors['yellow']}Proxy Options:{self.colors['end']}")
        print(f"{self.colors['cyan']}[1] No Proxy{self.colors['end']}")
        print(f"{self.colors['cyan']}[2] SOCKS4{self.colors['end']}")
        print(f"{self.colors['cyan']}[3] SOCKS5{self.colors['end']}")
        print(f"{self.colors['cyan']}[4] HTTP{self.colors['end']}")
        print(f"{self.colors['cyan']}[5] HTTPS{self.colors['end']}")
        
        choice = input("Select proxy type > ").strip()
        
        if choice == "1":
            self.proxy_config = None
            return None
            
        proxy_url = input("Enter proxy (host:port) > ").strip()
        username = input("Username (leave empty if none) > ").strip()
        password = input("Password (leave empty if none) > ").strip()
        
        if choice == "2":
            proxy_type = socks.SOCKS4
        elif choice == "3":
            proxy_type = socks.SOCKS5
        elif choice == "4":
            proxy_type = "http"
        elif choice == "5":
            proxy_type = "https"
        else:
            self.print_error("Invalid proxy type selection")
            return None
        
        # For SOCKS proxies, we'll use a different approach
        if choice in ["2", "3"]:
            # Parse host and port
            if ":" in proxy_url:
                host, port = proxy_url.split(":")
                port = int(port)
            else:
                self.print_error("Invalid proxy format. Use host:port")
                return None
                
            self.proxy_config = {
                'type': proxy_type,
                'host': host,
                'port': port,
                'username': username if username else None,
                'password': password if password else None
            }
        else:
            # Format proxy URL with authentication if provided
            if username and password:
                proxy_url = f"{username}:{password}@{proxy_url}"
                
            self.proxy_config = {
                'type': proxy_type,
                'url': f"{proxy_type}://{proxy_url}"
            }
        
        return self.proxy_config

    def create_session(self):
        """Create a requests session with proxy configuration"""
        session = requests.Session()
        
        # Configure SOCKS proxy if needed
        if self.proxy_config and self.proxy_config['type'] in [socks.SOCKS4, socks.SOCKS5]:
            # Set up SOCKS proxy
            socks.set_default_proxy(
                self.proxy_config['type'],
                self.proxy_config['host'],
                self.proxy_config['port'],
                username=self.proxy_config['username'],
                password=self.proxy_config['password']
            )
            socket.socket = socks.socksocket
            
            # Test the proxy connection
            try:
                # Try to make a test connection
                test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                test_socket.settimeout(10)
                test_socket.connect(("www.google.com", 80))
                test_socket.close()
                self.print_success("SOCKS proxy connection successful")
            except Exception as e:
                self.print_error(f"SOCKS proxy connection failed: {e}")
                return None
                
        # For HTTP/HTTPS proxies, set them in the session
        elif self.proxy_config and self.proxy_config['type'] in ["http", "https"]:
            session.proxies = {
                'http': self.proxy_config['url'],
                'https': self.proxy_config['url']
            }
            
            # Test the proxy connection
            try:
                test_response = session.get("http://httpbin.org/ip", timeout=10)
                if test_response.status_code == 200:
                    self.print_success("HTTP proxy connection successful")
                else:
                    self.print_error("HTTP proxy connection test failed")
                    return None
            except Exception as e:
                self.print_error(f"HTTP proxy connection failed: {e}")
                return None
        
        return session

    def get_safe_path(self, url, save_dir, is_main_page=False):
        parsed = urlparse(url)
        path = parsed.path.lstrip("/")

        if is_main_page:
            return os.path.join(save_dir, "index.html")

        if "fonts.googleapis.com" in parsed.netloc:
            filename = f"google-fonts-{self.font_counter}.css"
            self.font_counter += 1
            path = os.path.join("css", filename)

        elif not path or path.endswith("/"):
            path = os.path.join("misc", "file.html")

        if not os.path.splitext(path)[1]:
            path = path + ".html"

        return os.path.join(save_dir, path)

    def download_resource(self, session, url, save_dir, is_main_page=False):
        try:
            if not is_main_page:
                self.resource_done += 1
                self.print_processing(f"({self.resource_done}/{self.resource_total}) {url}")

            # Rotate headers for each request
            headers = random.choice(self.headers_list)
            
            # Set appropriate timeout
            timeout = 30 if any(ext in url for ext in ['.js', '.css', '.png', '.jpg', '.jpeg', '.gif']) else 10
            
            # Add random delay to mimic human behavior
            time.sleep(random.uniform(0.5, 1.5))
            
            response = session.get(url, timeout=timeout, verify=True, headers=headers)
            
            if response.status_code == 200:
                save_path = self.get_safe_path(url, save_dir, is_main_page)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                
                with open(save_path, "wb") as f:
                    f.write(response.content)
                
                if not is_main_page:
                    self.print_saved(save_path)
                return os.path.relpath(save_path, save_dir)
            else:
                self.print_error(f"Failed to download {url}: Status code {response.status_code}")
                return None
        except Exception as e:
            self.print_error(f"Failed to download {url}: {e}")
            return None

    def get_page_with_advanced_techniques(self, session, target_url):
        """Try multiple techniques to bypass bot detection"""
        techniques = [
            self.try_direct_request,
            self.try_with_referer,
            self.try_with_custom_cookies,
            self.try_with_javascript_emulation,
        ]
        
        for technique in techniques:
            try:
                result = technique(session, target_url)
                if result and result.status_code == 200:
                    # Check if we got a challenge page instead of the actual content
                    if self.is_challenge_page(result.text):
                        self.print_info("Detected challenge page, trying next technique...")
                        continue
                    return result
            except Exception as e:
                continue
                
        return None

    def is_challenge_page(self, content):
        """Check if the response is a challenge page (e.g., Cloudflare, DDoS protection)"""
        challenge_indicators = [
            "cloudflare",
            "ddos protection",
            "access denied",
            "challenge",
            "security check",
            "captcha",
            "enable javascript",
            "verification"
        ]
        
        content_lower = content.lower()
        for indicator in challenge_indicators:
            if indicator in content_lower:
                return True
        return False

    def try_direct_request(self, session, target_url):
        """Direct request with random headers"""
        headers = random.choice(self.headers_list)
        return session.get(target_url, timeout=15, headers=headers)

    def try_with_referer(self, session, target_url):
        """Request with referer header"""
        headers = random.choice(self.headers_list)
        headers['Referer'] = 'https://www.google.com/'
        return session.get(target_url, timeout=15, headers=headers)

    def try_with_custom_cookies(self, session, target_url):
        """Request with custom cookies"""
        headers = random.choice(self.headers_list)
        cookies = {
            'accept': '1',
            'accept-language': 'en-US,en;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
        }
        return session.get(target_url, timeout=15, headers=headers, cookies=cookies)
    
    def try_with_javascript_emulation(self, session, target_url):
        """Try to emulate JavaScript-enabled browser"""
        headers = random.choice(self.headers_list)
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        headers['Sec-Fetch-Dest'] = 'document'
        headers['Sec-Fetch-Mode'] = 'navigate'
        headers['Sec-Fetch-Site'] = 'none'
        headers['Sec-Fetch-User'] = '?1'
        headers['Upgrade-Insecure-Requests'] = '1'
        headers['Cache-Control'] = 'max-age=0'
        
        return session.get(target_url, timeout=15, headers=headers)

    def fix_relative_paths(self, html_content, base_url, save_dir):
        """Fix relative paths in HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Update all links
        for tag in soup.find_all(['a', 'link']):
            if tag.has_attr('href'):
                original_url = tag['href']
                if not original_url.startswith(('http://', 'https://', '#')):
                    absolute_url = urljoin(base_url, original_url)
                    tag['href'] = os.path.relpath(self.get_safe_path(absolute_url, save_dir), save_dir)
        
        # Update all src attributes
        for tag in soup.find_all(['img', 'script', 'iframe', 'source', 'audio', 'video']):
            if tag.has_attr('src'):
                original_url = tag['src']
                if not original_url.startswith(('http://', 'https://', 'data:')):
                    absolute_url = urljoin(base_url, original_url)
                    tag['src'] = os.path.relpath(self.get_safe_path(absolute_url, save_dir), save_dir)
        
        return str(soup)

    def clone_website(self, target_url, save_dir="cloned_site"):
        if not target_url.startswith(('http://', 'https://')):
            target_url = "https://" + target_url

        # Create session with proxy configuration
        session = self.create_session()
        if not session:
            self.print_error("Failed to create session with proxy")
            return

        try:
            # Add cookies to appear more like a real browser
            session.cookies.update({
                'sessionid': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=32)),
                'csrftoken': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=32)),
                'accept_cookies': 'true',
            })
            
            # Random delay before first request
            time.sleep(random.uniform(2, 5))
            
            # Try multiple techniques to bypass protection
            response = self.get_page_with_advanced_techniques(session, target_url)
            
            if not response:
                self.print_error("Failed to access the website with all techniques.")
                self.print_info("This website has strong anti-bot protection.")
                self.print_info("Try a different website or use a professional proxy/VPN service.")
                return
                
            if response.status_code == 403:
                self.print_error("403 Forbidden: Website has strong anti-bot protection.")
                self.print_info("Try a different website or use a proxy/VPN.")
                return
            
            response.raise_for_status()
            
        except Exception as e:
            self.print_error(str(e))
            return

        os.makedirs(save_dir, exist_ok=True)
        
        # Save the main page as index.html first
        main_page_path = os.path.join(save_dir, "index.html")
        with open(main_page_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        
        # Parse the HTML
        try:
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            self.print_error(f"Failed to parse HTML: {e}")
            return

        resources = []
        for tag in soup.find_all(["img", "script", "link", "source", "iframe", "video", "audio"]):
            if tag.name == "link" and tag.get("rel") and "stylesheet" in tag.get("rel"):
                attr = "href"
            elif tag.name in ["img", "script", "source", "iframe", "video", "audio"]:
                attr = "src" if tag.has_attr("src") else "data-src"
            else:
                continue
                
            if tag.has_attr(attr):
                res_url = urljoin(target_url, tag[attr])
                # Skip the main page URL to avoid downloading it again
                if res_url == target_url:
                    continue
                resources.append((tag, attr, res_url))

        self.resource_total = len(resources)
        self.resource_done = 0

        # Download all resources
        for tag, attr, res_url in resources:
            new_path = self.download_resource(session, res_url, save_dir)
            if new_path:
                tag[attr] = new_path.replace("\\", "/")
            
            # Random delay between requests to avoid detection
            time.sleep(random.uniform(0.5, 2.0))

        # Fix relative paths in the HTML
        fixed_html = self.fix_relative_paths(str(soup), target_url, save_dir)
        
        # Save the modified HTML
        index_path = os.path.join(save_dir, "index.html")
        try:
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(fixed_html)
            self.print_success(f"Cloned {target_url} → {save_dir}")
        except Exception as e:
            self.print_error(f"Failed to save index.html: {e}")

    def menu(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.print_banner()
            print(f"{self.colors['green']}[1] Clone a website{self.colors['end']}")
            print(f"{self.colors['red']}[2] Exit{self.colors['end']}\n")
            choice = input("Select option > ").strip()

            if choice == "1":
                # Setup proxy before cloning
                self.setup_proxy()
                
                target = input("Target URL > ").strip()
                save_dir = input("Save dir (default: cloned_site) > ").strip() or "cloned_site"
                self.print_info(f"Cloning {target} → {save_dir}")
                self.clone_website(target, save_dir)
                input("Press Enter to continue...")
            elif choice == "2":
                self.print_info("Exiting... Stay Ghost 👻")
                break
            else:
                self.print_error("Invalid option. Try again.")
                time.sleep(1)

if __name__ == "__main__":
    cloner = SigmaGhostCloner()
    cloner.menu()
