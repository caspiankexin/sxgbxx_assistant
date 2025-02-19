import datetime
import hashlib

today = datetime.datetime.today()
year = today.year
month = today.month

mac_address = input('请输入本机mac地址:')

original_informant = mac_address + '-' + str(year) + '-' + str(month) + '-' + '2022年11月6日14:05:55'
md5 = hashlib.md5(original_informant.encode()).hexdigest()
sha1 = hashlib.sha1(md5.encode()).hexdigest()
sha256 = hashlib.sha256(sha1.encode()).hexdigest()

print('本机的授权码为：' + sha256)
input('Press <Enter>')


