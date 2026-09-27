import numpy as np


# cari nomor baris dengan |A[baris, kolom]| paling besar, dari mulai_baris ke bawah
def cari_pivot(A, kolom, mulai_baris):
    n = len(A)
    return np.argmax(np.abs(A[mulai_baris:n, kolom])) + mulai_baris


# tukar posisi dua baris pada A dan b sekaligus (b wajib ikut, kalau tidak jawabannya salah)
def tukar_baris(A, b, baris1, baris2):
    A[[baris1, baris2]] = A[[baris2, baris1]]
    b[[baris1, baris2]] = b[[baris2, baris1]]


# pakai baris i untuk menolkan A[h, i] semua baris di bawahnya, b dikenai operasi yang sama
def nolkan_bawah_pivot(A, b, i):
    n = len(A)
    for h in range(i + 1, n):
        m = A[h, i] / A[i, i]
        A[h, :] -= m * A[i, :]
        b[h] -= m * b[i]


# ulang pivot-tukar-nolkan untuk tiap kolom sampai A jadi segitiga atas; tolak kalau singular
def eliminasi_maju(A, b):
    n = len(A)
    for i in range(n - 1):
        k = cari_pivot(A, i, i)
        if k != i:
            tukar_baris(A, b, i, k)
        if A[i, i] == 0:
            raise ValueError("matriks singular, solusi tidak tunggal")
        nolkan_bawah_pivot(A, b, i)
    if A[n - 1, n - 1] == 0:
        raise ValueError("matriks singular, solusi tidak tunggal")
    return A, b


# hitung x dari A yang sudah segitiga atas, dari baris paling bawah naik ke atas
def substitusi_mundur(A_segitiga, y):
    n = len(y)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - A_segitiga[i, i + 1:] @ x[i + 1:]) / A_segitiga[i, i]
    return x


# pembungkus: salin input -> eliminasi maju -> substitusi mundur; hasilkan x dan A segitiga
def gauss(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    A_segitiga, y = eliminasi_maju(A, b)
    return substitusi_mundur(A_segitiga, y), A_segitiga


if __name__ == "__main__":
    A = [[2, 1, -1], [4, 3, 1], [-2, 1, 2]]
    b = [3, 9, 4]

    x, A_segitiga = gauss(A, b)

    print("A mula-mula =\n", np.array(A, dtype=float))
    print("b mula-mula =", np.array(b, dtype=float))
    print()
    print("A setelah bagian bawahnya dinolkan =\n", np.round(A_segitiga, 4))
    print()
    print("x =", np.round(x, 4))
    print("cek A x =", np.round(np.array(A, dtype=float) @ x, 4))