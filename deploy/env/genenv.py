# 匯入標準函式庫
import socket       # 用來取得本機主機名稱
import os           # 處理檔案與環境變數
from configparser import ConfigParser  # 讀取 .ini 設定檔的工具

# 建立 ConfigParser 實例，讀取 ini 設定檔
local_config = ConfigParser()
local_config.read("local.ini")  # 讀取 local.ini 檔案

# 根據優先順序決定使用哪個 section：
# 優先順序：1. 環境變數 ENV 指定的 section > 2. 主機名稱對應的 section > 3. 預設 DEFAULT section
if os.environ.get("ENV", ""):
    # 若有設 ENV 環境變數，使用對應 section
    section = local_config[os.environ.get("ENV", "")]
else:
    # 都沒有的話，使用 DEFAULT 區段
    section = local_config["DEFAULT"]

# 將選到的 section 裡的設定轉為 .env 格式的內容
# 例如 key=value，每行一筆
env_content = ""
for sec in section:
    env_content += "{}={}\n".format(sec.upper(), section[sec])  # Key 轉大寫

# 將組好的內容寫入 .env 檔案中
with open(".env", "w", encoding="utf8") as env:
    env.write(env_content)
