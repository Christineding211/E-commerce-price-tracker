import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:ppWgnb_mfGe2m_@127.0.0.1:3306/headphone_db"
)

df = pd.read_sql(
    "SELECT * FROM product_price_timeline LIMIT 5",
    engine
)

print(df)