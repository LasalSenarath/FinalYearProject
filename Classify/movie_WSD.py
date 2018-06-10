import pypyodbc

# import MovieSense.WSD_MovieClassifier as WSD
from Classify import WSD_MovieClassifier as WSD

if __name__ == "__main__":
    con = pypyodbc.connect(Trusted_Connection='yes', driver='{SQL Server}', server='DESKTOP-M6FNGC5',
                           database='MovieSystemDB', Uid='sa', Pwd='1234')
    # cursor = con.cursor()
    # cursor.execute("SELECT Id,PreprocessedComment FROM Foreigner WHERE IsPreprocessed='TRUE'")
    #
    # # print(os.path.isfile("E:\MovieRecommendationSystem\WordSenseDisambiguation\MovieSense\day_sense.txt"))
    #
    # count = 0
    # for row in cursor.fetchall():
    #     #print(row[0])
    #     id = str(row[0])
    #     #print(row[1])
    #     tweet = str(row[1])
    #     result = WSD.AccessNewClassifier(tweet)
    #     print(result)
    #
    #
    #     # if result == 'movie':
    #     #     validity = 1
    #     #     count=count+1
    #     #     cursor.execute("UPDATE Foreigner SET Validity='TRUE' WHERE Id =" + str(id))
    #     #     cursor.commit()
    #     # else:
    #     #     validity =0
    #     #     cursor.execute("UPDATE Foreigner SET Validity='FALSE' WHERE Id =" + str(id))
    #
    #
    # print(count)
    # cursor.close()

    result = WSD.AccessNewClassifier("nice acting")
    print(result)