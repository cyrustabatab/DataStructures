




def four_parts(a):

    numbers = []


    four_parts_helper(a,numbers,0,1,4)

def four_parts_helper(a,numbers,current_sum,index,k):

    if k == 0 and current_sum == a:
        print(numbers)
        return
    if k == 0 or index == a:
        return


    for i in range(index,a):
        if current_sum + i <= a:
            numbers.append(i)

            four_parts_helper(a,numbers,current_sum + i,i,k - 1)


            numbers.pop()










        


class Node:

    def










def elementary_math(pairs):
    pass




if __name__ == "__main__":
    

    a = 8

    four_parts(a)
