# def bubble_sort(data):
#     step = []
#     comparisons = 0                          
#     swaps = 0
#     step.append(data.copy())
#     for i in range(len(data) - 1):
#         for j in range(len(data) - 1):
#             comparisons += 1
#             if data[j] > data[j + 1]:
#                 data[j], data[j + 1] = data[j + 1], data[j]
#                 swaps += 1
#                 step.append(data.copy())
#     return step, comparisons, swaps   

# def selection_sort(data):
#     step = []
#     comparisons = 0
#     swaps = 0
#     step.append(data.copy())
#     for i in range(len(data) - 1):
#         min_index = i
#         for j in range(i, len(data)):
#             comparisons += 1
#             if data[j] < data[min_index]:
#                 min_index = j
#         data[i], data[min_index] = data[min_index], data[i]
#         swaps += 1
#         step.append(data.copy())
#     return step, comparisons, swaps   

# def sum_to(n):
#     if n == 1:
#         return 1
#     return (n + sum_to(n-1))
    
# print(sum_to(10)) 

# def quicksort(data):
#     # base case: 段 <=1，本来就有序，直接返回
#     if len(data) <= 1:
#         return data

#     pivot = data[0]          

#     less = []                
#     greater = []             
#     for x in data[1:]:       
#         if x < data[0]:  
#             less.append(x)   
#         else:
#             greater.append(x)           

#     return quicksort(less) + [pivot] + quicksort(greater)

# print(quicksort([4, 2, 6, 1, 3]))    

# def quicksort(data, lo, hi):

#     if lo >= hi:
#         return

#     pivot = data[hi]             
#     i = lo                       

#     for j in range(lo, hi):      
#         if data[j] < pivot:
#             data[i], data[j] = data[j], data[i] 
#             i += 1                 
#     data[i], data[hi] = data[hi], data[i] 
                          
#     quicksort(data, lo, i - 1)    
#     quicksort(data, i + 1, hi)   

# d = [5, 2, 8, 1, 4]
# quicksort(d, 0, len(d) - 1)    
# print(d)                      


# def quicksort(data):
#     step = []
#     step.append(data.copy())                 
#     comparisons, swaps = _quicksort(data, 0, len(data) - 1, step)
#     return step, comparisons, swaps
                         
# def _quicksort(data, lo, hi, step):
#     if lo >= hi:
#         return 0, 0             

#     pivot = data[hi]
#     i = lo
#     comparisons = 0
#     swaps = 0

#     for j in range(lo, hi):
#         comparisons += 1                       
#         if data[j] < pivot:
#             data[i], data[j] = data[j], data[i]
#             swaps += 1
#             step.append(data.copy())                 
#             i += 1

#     data[i], data[hi] = data[hi], data[i]
#     swaps += 1
#     step.append(data.copy())                          
    
#     cL, sL = _quicksort(data, lo, i - 1, step)      
#     cR, sR = _quicksort(data, i + 1, hi, step)      
#     return comparisons + cL + cR, swaps + sL + sR   

# d = [5, 2, 8, 1, 4]
# step, comparisons, swaps = quicksort(d)
# print(d)                     
# print(comparisons, swaps)     
# print(len(step), "帧")         

# from algorithms import bubble_sort, selection_sort, quicksort

# print(bubble_sort([5, 2, 8, 1, 9, 3]))
# print(selection_sort([5, 2, 8, 1, 9, 3]))
# print(quicksort([5, 2, 8, 1, 9, 3]))

# def mergesort(data):                       
#     if len(data) <= 1:
#         return data
    
#     mid = len(data) // 2         
#     left = data[:mid]            
#     right = data[mid:]           
                                             
#     left_sorted = mergesort(left)
#     right_sorted = mergesort(right)
                                             
#     return merge(left_sorted, right_sorted)

# def merge(left, right):                                          
#     i = 0
#     j = 0
#     result = []
#     while i < len(left) and j < len(right):
#         if left[i] < right[j]:
#             result.append(left[i])
#             i += 1
#         else:
#             result.append(right[j])
#             j += 1
#     result += left[i:] + right[j:]
#     return result

# print(merge([1, 3, 5], [2, 4]))           
# print(mergesort([5, 2, 8, 1, 9, 3]))     

# # ---- public interface, signature unified with the other three ----  
# def mergesort(data):
#     step = []
#     step.append(data.copy())
#     comparisons, swaps = _mergesort(data, 0, len(data) - 1, step)
#     return step, comparisons, swaps


# # ---- internal recursive helper ----                      
# def _mergesort(data, lo, hi, step):
#     if lo >= hi:
#         return 0, 0
    
#     mid = (lo + hi) // 2        # 区间中点（注意：lo/hi 之间，不是 len(data)//2）
    
#     cL, sL = _mergesort(data, lo, mid, step)        # 排好左半 [lo, mid]
#     cR, sR = _mergesort(data, mid + 1, hi, step)    # 排好右半 [mid+1, hi]
#     cM, sM = _merge(data, lo, mid, hi, step)        # 合并两段（原地写回 data）
    
#     return cL + cR + cM, sL + sR + sM               # 本层+左+右+merge 累加

# # ---- in-place merge with buffer ----
# def _merge(data, lo, mid, hi, step):
#     # 复制两段到独立 buffer（slice 本身返回新列表）                   
#     buffer_left  = data[lo : mid + 1]
#     buffer_right = data[mid + 1 : hi + 1]
    
#     i = 0          # buffer_left 的读取位置
#     j = 0          # buffer_right 的读取位置
#     k = lo         # data 的写入位置（从 lo 开始）
#     comparisons = 0
#     swaps = 0
    
#     # 主循环：两边都还有元素                                     
#     while i < len(buffer_left) and j < len(buffer_right):
#         if buffer_left[i] < buffer_right[j]:
#             data[k] = buffer_left[i]
#             i += 1
#         else:
#             data[k] = buffer_right[j]
#             j += 1
#         k += 1
#         swaps += 1
#         comparisons += 1
#         step.append(data.copy())
    
#     # tail-merge: 把 buffer_left 剩下的写回 data          
#     while i < len(buffer_left):
#         data[k] = buffer_left[i]
#         i += 1
#         k += 1
#         swaps += 1
#         step.append(data.copy())
           
#     # tail-merge: 把 buffer_right 剩下的写回 data               
#     while j < len(buffer_right):
#         data[k] = buffer_right[j]
#         j += 1
#         k += 1
#         swaps += 1
#         step.append(data.copy())
    
#     return comparisons, swaps

# d = [5, 2, 8, 1, 9, 3]
# step, comparisons, swaps = mergesort(d)
# print(d)
# print(comparisons, swaps)
# print(len(step), "帧")

from algorithms import bubble_sort, selection_sort, quicksort, mergesort

#print(bubble_sort([5, 2, 8, 1, 9, 3]))
#print(selection_sort([5, 2, 8, 1, 9, 3]))
#print(quicksort([5, 2, 8, 1, 9, 3]))
print(mergesort([5, 2, 8, 1, 9, 3]))