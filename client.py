import requests
import json 

def set(k,v, url = "http://localhost:8080/"):
	r = requests.post(url,data = json.dumps({"cmd":"set", "key":k, "value":v}))
	ret = json.loads(r.text)
	return ret 

def get(k, url = "http://localhost:8080/"):
	r = requests.post(url,data = json.dumps({"cmd":"get", "key":k}))
	ret = json.loads(r.text)
	return ret 


if __name__== "__main__":
	print(get("abcdd"))
	print(set("abc","12dd3"))
	print(get("abc"))