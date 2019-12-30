



def is_valid(a,mid,m):


    s = 0
    count = 1
    for num in a:

        s += num

        if s > mid:
            s = num
            count += 1


    
    return count <= m




def split_array_largest_sum(a,days):


    minimum = max(a)
    maximum = sum(a)
    
    min_capacity = None

    while minimum <= maximum:

        mid = (minimum + maximum) // 2

        if is_valid(a,mid,days):
            min_capacity = mid
            maximum = mid - 1
        else:
            minimum = mid + 1
    

    return min_capacity




if __name__ == "__main__":
    
    a = list(range(1,11))
    days = 5
    print(split_array_largest_sum(a,days))









