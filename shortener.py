import unittest
import string

CHARACTER_MAP = string.ascii_lowercase + string.ascii_uppercase + \
           string.digits + '-_'
CHARACTER_MAP_REVERSE = dict((c, i) for (i, c) in enumerate(CHARACTER_MAP))
BASE = len(CHARACTER_MAP)

def id_to_base64(n):
    s = []
    while True:
        n, r = divmod(n, BASE)
        s.append(CHARACTER_MAP[r])
        if n == 0: break
    return ''.join(reversed(s))

def base64_to_id(s):
    n = 0
    for c in s:
        n = n * BASE + CHARACTER_MAP_REVERSE[c]
    return n



class ShortenerTests(unittest.TestCase):

    def setUp(self):
        self.results = {}
        for i in xrange(0, 700):
            self.results[i] = id_to_base64(i)
            print "%s -> %s" % (i, self.results[i])

    def test_spot(self):
        pass
        # self.assertEqual(self.results[1], 'b')
        # self.assertEqual(self.results[63], '_')
        # self.assertEqual(self.results[64], 'ba')

    # def test_bulk(self):
    #     passed_tests = False
    #     for i in range(1, 1000):
    #         passed_tests &= (i == num_decode(num_encode(i)))
    #         print num_decode(num_encode(i))
    #     self.assertTrue(passed_tests)

if __name__ == '__main__':
    unittest.main()




# import base64
# import string
# 
# ALLOWED_CHARS = string.ascii_lowercase + \
#                 string.ascii_uppercase + \
#                 string.digits + \
#                 '-_'
# BASE_SIZE = len(ALLOWED_CHARS)
# CHARACTER_MAP = {}
# for i, char in enumerate(ALLOWED_CHARS):
#     CHARACTER_MAP[i] = char
# 
# 
# def id_to_base64(integer):
#     """Convert a base 10 integer into a base 64 encoded string from the sequence
#     [a-z][A-Z][0-9][-_]
#     """
#     def id_to_base64_generator(integer):
#         """Convert a base 10 integer into base 64 encoded string
#         """
#         quotient = integer / BASE_SIZE
#         if quotient < BASE_SIZE:
#             if quotient is not 0:
#                 yield quotient # Special case for integers below 63
#         else:
#             for v in id_to_base64_generator(quotient):
#                 yield v
#         yield integer % BASE_SIZE # Remainder
# 
#     return "".join([CHARACTER_MAP[i] for i in id_to_base64_generator(integer)])
# 
# 
# def base64_to_id(base64):
#     """Convert base 64 encoded string into a base 10 integer. E.g.
#     
#     boi => 1, 14, 8 => (1 * 64 * 64) + (14 * 64) + 8 = 5000
#     """
#     integers = []
#     for char in base64[::-1]:
#         integers.append([k for k,v in CHARACTER_MAP.items() if v == char][0])
#     total = 0
#     for i, v in enumerate(integers):
#         total += v * (64**i) # Remember 64**0 = 1
#     return total
# 
# 
# if __name__ == '__main__':
#     import sys
#     if sys.argv[1] == '-tests':
#         passed_tests = True
#         for i in xrange(0, 10000):
#             passed_tests &= (i == base64_to_id(id_to_base64(i)))
#         print passed_tests
# 
# 
# # print id_to_base64(5000) # boi
# # print base64_to_id('boi') # 5000