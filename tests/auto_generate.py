import math


def recursive_sku(end_index,path,general_list,now):
    end_index -=1
    if end_index == 0:
        return
    item = []

    if end_index == len(path):
        for i in range(path[end_index - 1]):
            temp  = [i]
            item.append(temp)
    else:
        temp = general_list[len(path) - (end_index + 1)]
        temp_len = len(temp)
        total = path[now] * temp_len
        for i in range(total):
            if i < temp_len:  
                temp_item = temp[i % temp_len].copy()
                temp_item.insert(0,0)
                item.append(temp_item)
            else:
                temp_item = temp[i % temp_len].copy()
                n = math.ceil( i / temp_len )
                if i % temp_len == 0:
                    temp_item.insert(0, n)
                else:
                    temp_item.insert(0, n-1)
                item.append(temp_item)
        now-=1
            
    general_list.append(item)

    recursive_sku(end_index,path,general_list,now)
    

def main():
    path = [3,2,1,2]
    # general_list = [[[0],[1]],[[0,0],[0,1],[1,0],[1,1]],[[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]],[[0,0,0,0],[0,0,0,1],[0,0,1,0],[0,0,1,1],[0,1,0,0],[0,1,0,1],[0,1,1,0],[0,1,1,1],[1,0,0,0],[1,0,0,1],[1,0,1,0],[1,0,1,1],[1,1,0,0],[1,1,0,1],[1,1,1,0],[1,1,1,1]]]
    general_list = []
    now = len(path) - 2
    end_index = len(path)
    recursive_sku(end_index + 1,path,general_list,now)
    # print(len(general_list))
    # for i in general_list:
    #     print(i)
    #     print('--------------------------------')
    print(general_list[len(path) - 1])
    
if __name__ == "__main__":
    main()

