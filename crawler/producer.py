# 注意這裡不是直接呼叫函式, 而是把它當作「任務」送出去
from crawler.task import crawler


crawler.delay(x=0)