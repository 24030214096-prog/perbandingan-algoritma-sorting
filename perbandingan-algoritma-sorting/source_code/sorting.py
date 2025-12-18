import random
import string
import datetime
import time
import os
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")   
import matplotlib.pyplot as plt

# SORTING ALGORITHMS 
def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)
    return arr

# DATA GENERATOR 
def generate_random_numbers(n):
    return [random.randint(1, 10000) for _ in range(n)]

def generate_random_ascii(n):
    return [ord(random.choice(string.ascii_letters)) for _ in range(n)]

def generate_random_datetimes(n):
    base = datetime.datetime(2025, 1, 1)
    return [base + datetime.timedelta(days=random.randint(0, 365)) for _ in range(n)]

# TEST FUNCTION 
def test_sorting(algorithm, data, is_quick=False):
    arr = data.copy()
    start = time.time()
    if is_quick:
        algorithm(arr, 0, len(arr) - 1)
    else:
        algorithm(arr)
    return time.time() - start

# MAIN 
if __name__ == "__main__":

    sizes = [100, 500, 1000]

    results_for_plot = {
        "Random Numbers": {"Bubble": [], "Insertion": [], "Quick": []},
        "ASCII Codes": {"Bubble": [], "Insertion": [], "Quick": []},
        "Datetime Objects": {"Bubble": [], "Insertion": [], "Quick": []}
    }

    table_results = []

    print("\nHASIL PERBANDINGAN SORTING\n")
    print("No | Data Size | Dataset Type      | Bubble Sort | Insertion Sort | Quick Sort")
    print("--------------------------------------------------------------------------")

    no = 1
    for n in sizes:
        datasets = {
            "Random Numbers": generate_random_numbers(n),
            "ASCII Codes": generate_random_ascii(n),
            "Datetime Objects": generate_random_datetimes(n)
        }

        for name, data in datasets.items():
            data_b = data.copy()
            data_i = data.copy()
            data_q = data.copy()

            b = test_sorting(bubble_sort, data_b)
            i = test_sorting(insertion_sort, data_i)
            q = test_sorting(quick_sort, data_q, is_quick=True)

            results_for_plot[name]["Bubble"].append(b)
            results_for_plot[name]["Insertion"].append(i)
            results_for_plot[name]["Quick"].append(q)

            table_results.append({
                "Ukuran Data": n,
                "Jenis Dataset": name,
                "Bubble Sort (s)": round(b, 6),
                "Insertion Sort (s)": round(i, 6),
                "Quick Sort (s)": round(q, 6)
            })

            print(f"{no:<3}| {n:<4} | {name:<17} | {b:.6f} | {i:.6f} | {q:.6f}")
            no += 1

    # SIMPAN KE EXCEL 
    df = pd.DataFrame(table_results)
    df.to_excel("hasil_sorting.xlsx", index=False)

    # GRAFIK (DISIMPAN KE FILE) 
    output_dir = "hasil_grafik"
    os.makedirs(output_dir, exist_ok=True)

    for dataset in results_for_plot:
        plt.figure()
        plt.plot(sizes, results_for_plot[dataset]["Bubble"], marker='o')
        plt.plot(sizes, results_for_plot[dataset]["Insertion"], marker='o')
        plt.plot(sizes, results_for_plot[dataset]["Quick"], marker='o')

        plt.xlabel("Ukuran Data")
        plt.ylabel("Waktu Eksekusi (detik)")
        plt.title(f"Perbandingan Algoritma Sorting ({dataset})")
        plt.legend(["Bubble Sort", "Insertion Sort", "Quick Sort"])
        plt.grid(True)

        filename = dataset.replace(" ", "_").lower() + ".png"
        plt.savefig(os.path.join(output_dir, filename))
        plt.show()     
        plt.close()

    print("\nSemua grafik disimpan di folder 'hasil_grafik'")
    print("Tabel hasil disimpan sebagai 'hasil_sorting.xlsx'")