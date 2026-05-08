#從大資料庫裡面找到檔案叫 task.py 從那份文件中，指名要拿出的那個特定任務（標註了 @app.task 的函式）。
from crawler.task import crawler


crawler.delay(x=0)