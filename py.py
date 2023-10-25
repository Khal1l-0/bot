a = input('Введите число: ')
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
    
if is_number(a): 
    print('work')
if not is_number(a):
    print('hato') 
# print(type(a))