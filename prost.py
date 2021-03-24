def get_count(n):
    count = 0
    for i in range(2, n):
        if n % i == 0:
        	print(i)
            count += 1
    return count


print(get_count(1111111111))