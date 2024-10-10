def main():
    path = "14,2,3,4"
    fruits = path.split(',')  # 按逗号分割

    for i in range(0, len(fruits)):
        print(fruits[i])
    
    print(type(fruits))

if __name__ == "__main__":
    main()