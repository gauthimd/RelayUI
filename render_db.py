from application.models import Data
from sys import argv
from mongoengine import connect

db = 'RelayUI'


def populate_data():
    Data.drop_collection()
    sample_data = {'channel_1': False}

    data = Data(**sample_data)
    print 'inserted data: {}'.format(data.save().id)


def query_data():
    print Data.objects().first().channel_1


def connect_db():
    try:
        if argv[0] == 'production':
            connect(host='mongodb://mongodb/{}'.format(db))
        else:
            connect(db=db)
    except:
        print 'no args supplied, connecting test database locally'
        connect(db=db)


def init_db():
    connect_db()
    # populate_data()
    query_data()
    return 0


if __name__ == "__main__":
    init_db()
