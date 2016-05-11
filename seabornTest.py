import pandas as pd
from pandas import DataFrame

import seaborn as sns
sns.set_context("talk")
sns.set_style("white")

people = ['Hannah', 'Bethany', 'Kris', 'Alex', 'Earl', 'Lori']
reputation = ['awesome', 'cool', 'brilliant', 'meh', 'awesome', 'cool']
dictionary = dict(zip(people, reputation))
df = pd.DataFrame(dictionary.values(), dictionary.keys())
df = df.rename(columns={0:'reputation'})

# sns.countplot(x='reputation', data=df)
# sns.plt.show()
#
sns.barplot(x=df.reputation, y=df.reputation.value_counts())
sns.plt.show()