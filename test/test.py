from pyhive import hive
import pandas as pd
connect = hive.connect(host='192.168.0.101', port=10001, username='grid', password='grid', database='test',auth="CUSTOM")
cur = connect.cursor()
from sqlalchemy import create_engine
data = [(None, '1', 'c', None), (None, 'vvvvvvvvvvv', '2021/9/12', None), (None, 'f', None, None), (None, None, '#NAME?', None), (None, None, '#VALUE!', None), (None, None, 'NA', None)]
sql = 'insert into `csv_zw_utf8`(`2`,`a`,`dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd`,`zzzzzzzz10zzzzzzzz20zzzzzzzz30zzzzzzzz40zzzzzzzz50zzzzzzzz60zz`) values(%s,%s,%s,%s)'
cur.executemany(sql, data)
df = pd.DataFrame(data)
engine = create_engine("hive://{0}:{1}@{2}:{3}/{4}".format('grid','grid','192.168.0.101',10001,
                                                                   'test'),connect_args={'auth': 'CUSTOM'},)
df.to_sql('csv_zw_utf8', engine, if_exists='append', index=False, method='multi')