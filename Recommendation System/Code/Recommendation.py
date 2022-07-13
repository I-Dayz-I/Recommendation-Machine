import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import networkx as nx
from nxviz import CircosPlot
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def main():
    #Getting Script Paths
    parentFolderPath = os.path.realpath(__file__) + '\..\..'
    
    #Loading the Reviews
    score = pd.read_csv(parentFolderPath + '\Dataset\BX-Book-Ratings.csv',sep=";",error_bad_lines=False, encoding='latin-1')
    
    #Printing info about reviews
    #DatasetScoreInfo(score)
    
    #Eliminating stuff i don't need to make the dataset look kind of like i want
    score = ShaveScoreSet(score)
    
    #Getting the 'books' or hashtags 
    books = pd.read_csv(parentFolderPath + '\Dataset\BX_Books.csv',sep=";",error_bad_lines=False, encoding='latin-1')
    
    #Printing info about books
    #DatasetBooksInfo(books)
    
    users =  pd.read_csv(parentFolderPath + '\Dataset\BX-Users.csv',sep=";",error_bad_lines=False, encoding='latin-1')
    #Printing info about users
    #DatasetUsersInfo(users)
    users = ShaveUserSet(users)
    
    #Merging everything in one big table
    all_in_one = MergeEverything(score,books,users)
    #Deleting stuff i don't need from the dataset
    all_in_one.drop(['Image-URL-S','Image-URL-M','Image-URL-L'],axis=1,inplace=True)
    
    #PlottingExamples(all_in_one)
    #CreatingGraphOfNetwork(all_in_one)
    
    #K_MeansClustering(all_in_one)
    #print(all_in_one)
    
    clean = CleanningData(books, users, score)
    print("100 BOOKS SAMPLE:")
    list1=list(clean['book_name'])
    setlist = set(list1)
    print(setlist)
    bname = 'X'
    while bname not in setlist:
        print("SELECT 1 BOOK:")
        bname = input()
    
    
    KNN(clean,bname)
    
    
    
    



#Deleting duplicate Columns and missing values
def ShaveScoreSet(Scores):
    #print(Scores.shape)
    #print(Scores[Scores == 0].count())
    #Deleting Everything that does not interest me
    Scores.drop_duplicates(inplace=True, keep='first') 
    Scores = Scores.dropna()
    Scores = Scores[Scores['Book-Rating'] != 0]
    #print(Scores.info())
    #print(Scores.shape)
    
    Scores_Clean = Scores
    Scores_Clean.to_csv("rating_clean.csv")
    
    return Scores_Clean


def DatasetScoreInfo(Scores):
    #Printing firsts 10 lines of reviews
    print(Scores.head(10))

    #Printing Full info of Columns
    print(Scores.info())

    #Printing Amount of Rows and columns
    print(Scores.shape)

    #Printing mean of Scores
    rating = Scores['Book-Rating']
    rating_mean = rating.mean() 
    print("Score Mean:" + rating_mean)


def DatasetBooksInfo(Books):
    print(Books.head(3))

def DatasetUsersInfo(Users):
    print(Users['User-ID'].isnull().sum())

def ShaveUserSet(Users):
    Users_Clean = Users.dropna()
    
    return Users_Clean



def MergeEverything(scores, books, users):
    user_scores = pd.merge(scores, users, on='User-ID', how='left')
    #print(user_scores)
    
    user_scores_books = pd.merge(user_scores, books, on='ISBN', how='left')
    #print(user_scores_books)
    
    #Cleaning just in case
    user_scores_books.dropna()
    
    #Renaiming to easier things to write (remember change to true name)
    user_scores_books.rename(columns={
    'User-ID': 'User_ID', 
    'Book-Rating': 'Book_Rating', 
    'Book-Title': 'Book_Title',
    'Book-Author': 'Book_Author',
    'Year-Of-Publication': 'Year_Of_Publication'
    }, inplace=True)
    
    
    
    return user_scores_books

def PlottingExamples(BigData):
    
    #Plotting Top rated Books
    data = BigData.groupby(by="Book_Title").count().sort_values(by="Book_Rating", ascending=False)[:5]["Book_Rating"]
    _x = data.index
    _y = data.values
    
    plt.figure(figsize=(29,8), dpi=100)
    plt.bar(range(len(_x)), _y, width=0.5)
    plt.xticks(range(len(_x)), _x)
    plt.xlabel("Book Title")
    plt.ylabel("Num Counts")
    plt.title("Top Rated Books")
    plt.show()

    #Plotting most active users
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    langs = ['98391', '153662', '235105 ', '16795', '171118']
    students = [5689,1833,1017,956,954]
    ax.bar(langs,students)
    plt.xlabel("User ID")
    plt.ylabel("Num Counts")
    plt.title("Top5 Rating Users")
    plt.show()




#DRAWING BIPARTITE GRAPH, EXTREMLY SLOW!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def CreatingGraphOfNetwork(All_in_one):
    #I Have to do This cuz if i Don't this gonna crash
    BigData = All_in_one.head(100)
    
    BigData['ISBN']=pd.to_numeric(BigData['ISBN'],errors='coerce')
    BigData.dropna(inplace=True)
    print(BigData.head())
    print(BigData.info())
    
    G = nx.Graph()
    m=list(BigData['User_ID'])
    n=list(BigData['Book_Title'])
    zip_list=list(zip(m,n))
    # Add nodes with the node attribute "bipartite"
    G.add_nodes_from(m, bipartite=0)
    G.add_nodes_from(n, bipartite=1)
    G.add_edges_from(list(zip(m,n)))
    
    pdd=pd.DataFrame(zip_list,columns=['source','target'])
    top_nodes = {n for n, d in G.nodes(data=True) if d["bipartite"] == 0}
    bottom_nodes = set(G) - top_nodes
    
    nodes = G.nodes()
    degree = G.degree()
    colors = [degree[n] for n in nodes]

    pos = nx.bipartite_layout(G,top_nodes)
    cmap = plt.cm.viridis_r
    #cmap = plt.cm.Greys

    vmin = min(colors)
    vmax = max(colors)

    fig = plt.figure(figsize = (15,15), dpi=100)

    nx.draw(G,pos,alpha = 0.8, nodelist = nodes, node_color = 'r', node_size = 10, with_labels= True,font_size = 6,font_color='b', width = 0.2, cmap = cmap, edge_color ='blue')
    #fig.set_facecolor('#0B243B')

    plt.show()
    c = CircosPlot(G,node_color='bipartite',node_grouping='bipartite')
    c.draw()
    plt.show()


def K_MeansClustering(All_in_one):
    BigData = All_in_one.head(5000)
    
    BigData['ISBN']=pd.to_numeric(BigData['ISBN'],errors='coerce')
    BigData.dropna(inplace=True)
    BigData.drop(['Book_Title','Publisher','Location'],axis=1,inplace=True)
    BigData.head()
    BigData.info()

    #use get_dummies function to change those qualitative columns into binary ones
    data_encoded = pd.get_dummies(BigData)
    print(data_encoded)
    
    scaler = MinMaxScaler()
    train_X,test_X = train_test_split(data_encoded, test_size=0.3, random_state=930)
    X_train = scaler.fit_transform(train_X)
    X_test = scaler.transform(test_X)

    X = scaler.transform(data_encoded)
    
    K = range(1, 20)
    meanDispersions = []
    for k in K:
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(X_train)

        meanDispersions.append(kmeans.inertia_)

    plt.plot(K, meanDispersions, 'rx-')
    plt.xlabel('k')
    plt.ylabel('Average Dispersion')
    plt.title('Selecting k with the Elbow Method')
    plt.show() 


def CleanningData(books, users , scores):
    books.drop(['Image-URL-S','Image-URL-M','Image-URL-L'],axis=1,inplace=True)
    books.rename(columns={'Book-Title':'book_name','Book-Author':'author','Year-Of-Publication':'year','Publisher':'publisher'},inplace=True)
    users.rename(columns={'User-ID':'user_id','Location':'location','Age':'age'},inplace=True)
    scores.rename(columns={'User-ID':'user_id','ISBN':'ISBN','Book-Rating':'book-rating'},inplace=True)
    #users who have reviewed more than 30 books (frequent users)
    x = scores['user_id'].value_counts()>30
    #Getting raitngs of those users
    index1 = x.index
    scores = scores[scores['user_id'].isin(index1)]
    merged = scores.merge(books, on = 'ISBN')
    merged_groupby=merged.groupby('book_name')['book-rating'].count().reset_index()
    merged_groupby.rename(columns={'book-rating':'number_of_ratings'},inplace=True)
    merged_groupby=merged_groupby[merged_groupby['number_of_ratings']>30]
    merged_groupby.head()
    integrated_merged=merged.merge(merged_groupby, on='book_name')
    integrated_merged.drop_duplicates(['user_id','book_name'],inplace=True)
    
    return integrated_merged
    
    
    
    
    
    
    
    
def KNN(score_table, book_name):
    pivot=pd.pivot_table(score_table, columns='user_id',index='book_name',fill_value=0,values='book-rating')
    pivot_csr=csr_matrix(pivot)
    model=NearestNeighbors(algorithm='brute')
    model.fit(pivot_csr)
    
    book_id = np.where(pivot.index == book_name)[0][0]
    distances, recommendations = model.kneighbors(pivot.iloc[book_id,:].values.reshape(1,-1))
    for i in range(len(recommendations)):
        if i == 0:
            print(f"For book \"{book_name}\" we would recommend the following:")
        if not i:
            list2=pivot.index[recommendations[i]]
            for j in range(len(list2)):
                print(list2[j])



main()





