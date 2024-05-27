import pandas as pd

from dateroll import ddh


# df = ddh('5/25/2024,6/23/2029,6m|NYuWE').split_bond
P = "tests/test_data/spy.csv"
df = pd.read_csv(P,header=[0],index_col=[0])

import code;code.interact(local=dict(globals(),**locals()))


df_at = df[df.index.time==ddh('9h30min+1h11min').time]
st,ed = ddh('9h30min').time,ddh('16h').time
mkt = df.between_time(st,ed)

if __name__=="__main__":
    print(df_at)

