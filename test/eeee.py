nums = range(2,20)
for i in nums:
    nums = filter(lambda x: x == i or x % i, nums)
print nums


a = 2
b = 2
if a%b:
    print 'ok'
