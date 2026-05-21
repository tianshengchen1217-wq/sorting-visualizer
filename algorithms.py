# --- 1.bubble_sort alg ---
def bubble_sort(data):
    step = []
    comparisons = 0
    swaps = 0
    step.append((data.copy(), comparisons, swaps, [], "compare"))
    for i in range(len(data) - 1):
        for j in range(len(data) - 1 - i):
            comparisons += 1
            step.append((data.copy(), comparisons, swaps, [j, j+1], "compare"))
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                swaps += 1
                step.append((data.copy(), comparisons, swaps, [j, j+1], "swap"))
    return step, comparisons, swaps

# --- 2.selection_sort alg ---
def selection_sort(data):
    step = []
    comparisons = 0
    swaps = 0
    step.append((data.copy(), comparisons, swaps, [], "compare"))
    for i in range(len(data) - 1):
        min_index = i
        for j in range(i + 1, len(data)):
            comparisons += 1
            step.append((data.copy(), comparisons, swaps, [min_index, j], "compare"))
            if data[j] < data[min_index]:
                min_index = j
        if min_index != i:                                                  
            data[i], data[min_index] = data[min_index], data[i]
            swaps += 1
            step.append((data.copy(), comparisons, swaps, [i, min_index], "swap"))
    return step, comparisons, swaps

# --- 3.quick_sort alg ---
def quicksort(data):
    step = []
    counter = [0, 0]    
    step.append((data.copy(), counter[0], counter[1], [], "compare"))
    _quicksort(data, 0, len(data) - 1, step, counter)
    return step, counter[0], counter[1]


def _quicksort(data, lo, hi, step, counter):
    if lo >= hi:
        return                  

    pivot = data[hi]
    i = lo

    for j in range(lo, hi):
        counter[0] += 1            # comparisons +=1
        step.append((data.copy(), counter[0], counter[1], [j, hi], "compare"))
        if data[j] < pivot:
            data[i], data[j] = data[j], data[i]
            counter[1] += 1        # swaps +=1
            step.append((data.copy(), counter[0], counter[1], [i, j], "swap"))
            i += 1

    data[i], data[hi] = data[hi], data[i]
    counter[1] += 1
    step.append((data.copy(), counter[0], counter[1], [i, hi], "swap")) 

    _quicksort(data, lo, i - 1, step, counter)
    _quicksort(data, i + 1, hi, step, counter)

# --- 4.mergesort_sort alg ---
def mergesort(data):
    step = []
    counter = [0, 0]
    step.append((data.copy(), counter[0], counter[1], [], "compare"))
    _mergesort(data, 0, len(data) - 1, step, counter)
    return step, counter[0], counter[1]


def _mergesort(data, lo, hi, step, counter):
    if lo >= hi:
        return
    mid = (lo + hi) // 2
    _mergesort(data, lo, mid, step, counter)
    _mergesort(data, mid + 1, hi, step, counter)
    _merge(data, lo, mid, hi, step, counter)


def _merge(data, lo, mid, hi, step, counter):
    buffer_left  = data[lo : mid + 1]
    buffer_right = data[mid + 1 : hi + 1]

    i = 0
    j = 0
    k = lo

    while i < len(buffer_left) and j < len(buffer_right):
        counter[0] += 1
        step.append((data.copy(), counter[0], counter[1], [k], "compare"))
        if buffer_left[i] < buffer_right[j]:
            data[k] = buffer_left[i]
            i += 1
        else:
            data[k] = buffer_right[j]
            j += 1
        counter[1] += 1
        step.append((data.copy(), counter[0], counter[1], [k], "swap"))
        k += 1

    while i < len(buffer_left):
        data[k] = buffer_left[i]
        i += 1
        counter[1] += 1
        step.append((data.copy(), counter[0], counter[1], [k], "swap"))
        k += 1

    while j < len(buffer_right):
        data[k] = buffer_right[j]
        j += 1
        counter[1] += 1
        step.append((data.copy(), counter[0], counter[1], [k], "swap"))
        k += 1