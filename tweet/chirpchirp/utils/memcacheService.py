import memcache

class MemcacheService:

    def __init__(self,ipString,port):
        # init the memcache connection
        self.mc = memcache.Client([(ipString, port)])


    # get the result from memcache storage
    def get(self,query):
        # turn the mongodb search query into a str key.
        query = self.compressedToQueryString(query)
        if query in self.mc:
            return self.mc.get(query)
        return None



    # set query - result into memcache
    def set(self,query,result):
        # turn the mongodb search query into a str key.
        query = self.compressedToQueryString(query)
        self.mc.set(query,result)



    # delete query - result from memcache
    def delete(self,query):
        # turn the mongodb search query into a str key.
        query = self.compressedToQueryString(query)
        if query in self.mc:
            self.mc.delete(query)



    # turn the mongodb search query into a str key, remove spaces.
    def compressedToQueryString(self,query):
        if not isinstance(query,str):
            query = str(query)
            # gets rid of all spaces in the str query
        return query.replace(" ","")
