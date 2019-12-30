import hashlib

class BIT:

    def __init__(self,nums):
        self.a = [0] * (len(nums) + 1)

        for i,num in enumerate(nums):
            self.update(i + 1,num)
    
    def update(self,index,num):

        while index < len(self.a):
            num += self.a[index]
            index += index & -index
    

    def query(self,index):
        
        total = 0
        while index > 0:
            total += self.a[index]
            index -= index & -index

        return total

    def range_query(self,a,b):
        return self.query(b) - self.query(a -1)




class BloomFilter:

    def __init__(self,a=10,k=3):
        self.a = [False] * a
        self.hash_algorithms = [hashlib.md5,hashlib.sha1,hashlib.sha256,hashlib.sha384,hashlib.sha512]
        self.hash_functions = [self._get_hash_function(f) for f in self.hash_algorithms[:k]]

    def _get_hash_function(self,f):

        def hash_function(value):

            result = f(str(value).encode('utf-8')).hexdigest()
            return int(result,16) % len(self.a)

        return hash_function
    
    def add(self,value):

        for f in self.hash_functions:
            self.a[f(value)] = True

    def __contains__(self,value):

        return all(f(value) for f in self.hash_functions)


if __name__ == "__main__":
    
    bf = BloomFilter()

    f = bf._get_hash_function(hashlib.sha512)

    print(f(10))



