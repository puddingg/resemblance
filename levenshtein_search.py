import Levenshtein as Shtein
import pandas as pd


class LS():
    def __init__(self):
        self.df1 = pd.DataFrame
        self.df2 = pd.DataFrame
       
        pathlist = ['さいたま１.csv','さいたま２.csv']
        columns = ('住所', '名称')
        with open(pathlist[0], 'r', encoding='utf-8') as f:
            self.df1 = pd.read_csv(f, usecols=columns, na_filter=False, dtype=str)
        with open(pathlist[1], 'r', encoding='utf-8') as f:
            self.df2 = pd.read_csv(f, usecols=columns, na_filter=False, dtype=str)

    @staticmethod
    def strip_spaces(string):
        return string.replace(r'\s', '')
      
    @staticmethod
    def distance(str1, str2):
        """just call Levenshtein.distance() """

        return Shtein.distance(str1, str2)

    @staticmethod
    def norm_distance(str1, str2):
        """return Levenshtein distance normalized by the length of the given string (longer one)
        """

        str1 = LS.strip_spaces(str1)
        str2 = LS.strip_spaces(str2)
        
        dis = LS.distance(str1, str2)
        n1 = len(str1)
        n2 = len(str2)
        if n1 >= n2:
            return dis / n1
        else:
            return dis / n2

    def search(self):
        """似たもの同士を抽出"""

        columns = ['元idx','元住所','元名称','住所','名称','住所距離','名称距離','距離積','idx']
        out_df = pd.DataFrame(columns=columns)
        count = 0
        for idx, row in self.df2.iterrows():
            temp_df = self.df1.copy()
            # 住所距離
            s = pd.Series([LS.norm_distance(row['住所'], i) for i in temp_df.loc[:,'住所']])
            temp_df['住所距離'] = s
            # 名称距離
            s = pd.Series([LS.norm_distance(row['名称'], i) for i in temp_df.loc[:,'名称']])
            temp_df['名称距離'] = s

            # 値の調整
            temp_df.loc[temp_df['住所距離'] == 0, '住所距離'] = 0.00001
            temp_df.loc[temp_df['名称距離'] == 0, '名称距離'] = 0.00001

            # 距離積
            temp_df['距離積'] = temp_df['住所距離'] * temp_df['名称距離']

            # 諸情報
            temp_df['元idx'] = idx
            temp_df['元住所'] = row['住所']
            temp_df['元名称'] = row['名称']
            temp_df['idx'] = temp_df.index
            
            # 距離積が一定値以下のレコードを抽出
            temp_df = temp_df.loc[temp_df['距離積'] < 0.000006]
            out_df = out_df.append(temp_df, ignore_index=True)
            count += 1
            print(count)
        
        out_df.to_excel('here.xlsx', columns=columns, index=False)


if __name__ == '__main__':
    from time import time
    s = time()
    LS = LS()
    LS.search()
    e = time()
    print(e-s)
   