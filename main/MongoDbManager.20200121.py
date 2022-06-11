import pymongo
import datetime

class MongoDbManager :
    _instance = None
    client = pymongo.MongoClient('mongodb+srv://admin:admin@coupangtest-ribq2.mongodb.net/test?retryWrites=true&w=majority')
    database = client['coupang']

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    #product_db
    def get_productdb_from_collection(cls, _query):
        assert cls.database
        return cls.database.get_collection('product_db').find(_query)

    def delete_productdb_from_collection(cls, _query):
        assert cls.database
        return cls.database.get_collection('product_db').remove(_query)

    def get_product_vendor_count(cls):
        pipeline = [{'$group': {'_id': {'seller_name': '$seller_name','productid': '$productid'},'c_ven': {'$sum': 1}}},
                    {'$group': {'_id': '$_id.seller_name','tot_prd': {'$sum': 1},'tot_ven': {'$sum': '$c_ven'}}}]
        assert cls.database
        return cls.database.get_collection('product_db').aggregate(pipeline)

    def get_product_lastest(cls):
        assert cls.database
        return cls.database.get_collection('product_db').aggregate([{'$sort': {'_id': -1}}, {'$limit': 1}])

    #seller_db
    def get_sellerdb_from_collection(cls, _query):
        assert cls.database
        return cls.database.get_collection('seller_db').find(_query)

    def get_sellerdb_noduplicate_from_collection(cls):
        # pipline = [{'$group': {'_id': {'seller_name': '$seller_name',
        #                                 'seller_number': '$seller_number',
        #                                 'seller_code': '$seller_code',
        #                                 'seller_type': '$seller_type',
        #                                 'total_rating': '$total_rating',
        #                                 'total': '$total',
        #                                 'update': '$update'}}},
        #            {'$project': {'_id':'noduplicate', 'seller_name':'$_id.seller_name', 'seller_number': '$_id.seller_number',
        #                          'seller_code': '$_id.seller_code', 'seller_type': '$_id.seller_type',
        #                          'total_rating': '$_id.total_rating', 'total': '$_id.total', 'update': '$_id.update'}}]
        # assert cls.database
        # return cls.database.get_collection('seller_db').aggregate(pipline)
        pass

    def get_seller_nouduplicate_count(cls):
        pipline = [{'$group': {'_id': {'seller_name': '$seller_name',
                                       'seller_number': '$seller_number',
                                        'seller_code': '$seller_code',
                                        'seller_type': '$seller_type',
                                        'total_rating': '$total_rating',
                                        'total': '$total',
                                        'update': '$update'}}},
                   {'$project': {'_id': 'noduplicate', 'seller_name': '$_id.seller_name',
                                'seller_number': '$_id.seller_number', 'seller_code': '$_id.seller_code',
                                'seller_type': '$_id.seller_type', 'total_rating': '$_id.total_rating',
                                'total': '$_id.total', 'update': '$_id.update'}},
                   {'$count': 'seller_name'}]
        assert cls.database
        return cls.database.get_collection('seller_db').aggregate(pipline)

    def get_seller_lastest(cls):
        assert cls.database
        return cls.database.get_collection('seller_db').aggregate([{'$sort': {'_id': -1}}, {'$limit': 1}])

    #winner_db
    def get_winnerdb_from_collection(cls, _query):
        assert cls.database
        return cls.database.get_collection('winner_db').find(_query)

    def get_all_winnerdb_from_collection(cls):
        assert cls.database
        return cls.database.get_collection('winner_db').aggregate([{'$project': {'_id': 0}}])

    def get_all_winner_count(cls):
        assert cls.database
        return cls.database.get_collection('winner_db').aggregate([{'$unwind': {'path': '$winner'}},
                                                                    {'$count': 'winner'}])
    def get_new_winner_count(cls):
        assert cls.database
        return cls.database.get_collection('winner_db').aggregate([{'$unwind': {'path': '$winner'}},
                                                                   {'$match': {'update': {'$gt': datetime.datetime.today().strftime('%Y-%m-%d 05:00')}}},
                                                                     {'$count': 'winner'}])
    def get_winnerdb_log(cls):
        assert cls.database
        return cls.database.get_collection('winner_db_log').aggregate([{'$sort': {'end_time': -1}}, {'$limit': 1}])

    def get_winner_lastest(cls):
        assert cls.database
        return cls.database.get_collection('winner_db').aggregate([{'$sort': {'_id': -1}}, {'$limit': 1}])

    #register
    def add_user_on_collection(cls, _data):
        if type(_data) is list:
            return cls.database.insert_many(_data)
        else:
            return cls.database.insert_one(_data)

    #cateogry db
    def get_all_mancat_collection(cls,_query):
        assert cls.database
        return cls.database.get_collection('man_cat').find(_query)

    def get_all_womancat_collection(cls,_query):
        assert cls.database
        return cls.database.get_collection('woman_cat').find(_query)

    def get_setcat(cls,_query):
        assert cls.database
        return cls.database.get_collection('setting').find(_query)

    def get_cat_log(cls):
       assert cls.database
       return cls.database.get_collection('mcat_log').aggregate([{'$sort': {'end_time': -1}}, {'$limit': 1}])


    # winner db
    # def get_winnerdb_from_collection(cls,_query):
    #     assert cls.database
    #     return cls.database.get_collection('product_db').aggregate(_query)

