"""Send a post valid post request to help debug playback"""
from requests import post

url = "http://192.168.1.30:3000/login"

r = post(url, data={"username": "nick", "password": "123", "submit": "Sign In"}, allow_redirects=True)