import psycopg2

dbnametwitter = "testpython"
usertwitter = "ioana"
passwordtwitter = "ioana"
hosttwitter = "localhost"
porttwitter = "5432"


def delete_rows(name):
    conn_twitter_del = psycopg2.connect(dbname=dbnametwitter, user=usertwitter, password=passwordtwitter,
                                        host=hosttwitter, port=porttwitter)
    cursor_twitter_del = conn_twitter_del.cursor()

    cursor_twitter_del.execute("DELETE FROM %s a using %s b WHERE a.id>b.id AND a.tweet = b.tweet;" % (name, name,))

    conn_twitter_del.commit()

    cursor_twitter_del.close()
    conn_twitter_del.close()


name = "tweets_predict_avengers"

if __name__ == '__main__':
    delete_rows(name)
