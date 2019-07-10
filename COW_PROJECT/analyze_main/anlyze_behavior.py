import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as mpl3d
import pandas as pd
import numpy as np
import scipy as sp
import sklearn.decomposition as skd
import hmm
import sklearn

# 3次元散布図を作成する
def show_3d_plot(df):
    # グラフ作成
    fig = plt.figure()
    ax = mpl3d.Axes3D(fig)

    # 軸ラベルの設定
    ax.set_xlabel("Accumulated distance")
    ax.set_ylabel("D/A rate")
    ax.set_zlabel("CV/A rate")
    #ax.set_zlabel("interval")

    #clust_array = np.array([df['E'], df['N'], df['P']])
    #clust_array = clust_array.T
    #pred = sklearn.cluster.KMeans(n_clusters = 2).fit_predict(clust_array)
    pred = []
    for d, ad in zip(df['E'], df['N']):
        if (d >= 9):
            if (0.2 < ad and ad < 0.8):
                pred.append(1)
            else:
                pred.append(0)
        else:        
            pred.append(0)

    a = translate_dt_to_int(df['A'])
    # 散布図作成
    #A:Start time,B:Latitude,C:Longitude,D:Continuous time,E:Moving amount,F:Average velocity,G:Moving distance,H:Moving direction,I:Last rest length,J:Last rest interval,K:Label
    #ax.plot(df['H'], df['J'], df['L'], "o", color="#00aa00", ms=4, mew=0.5)
    #plt.show()
    #ax.plot(df['E'], df['N'], df['P'], "o", color="#00aa00", ms=4, mew=0.5)
    ax.scatter(df['E'], df['N'], df['P'], "o", c=pred)
    plt.show()

#datetime型のデータを整数型に直して系列を作成する
def translate_dt_to_int(dt_list):
    i_list = []
    for i, dt in enumerate(dt_list):
        i_list.append(i)
    return pd.Series(i_list)

#3次元のデータを主成分分析し，2次元にする
def reduce_dim_from3_to2(x, y, z):
    print("今から主成分分析を行います")
    features = np.array([x.values, y.values, z.values]).T
    pca = skd.PCA()
    pca.fit(features)
    transformed = pca.fit_transform(features)
    print("累積寄与率: ", pca.explained_variance_ratio_)
    print("主成分分析が終了しました")
    return transformed[:, 0], transformed[:, 1]

if __name__ == '__main__':
    #0:Start time, 1:Latitude, 2Longitude, 3:Continuous time, 4:Moving amount, 5:Average velocity, 6:Moving distance, 7:Moving direction, 8:Last rest length, 9:Last rest interval, 10:Label
    df = pd.read_csv(filepath_or_buffer = "features.csv", encoding = "utf-8", sep = ",", header = 0, usecols = [0,3,4,5,6,7,8,10,12,13,14,15], names=('A', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'M', 'N', 'O', 'P'))
    show_3d_plot(df)