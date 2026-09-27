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


# kebalikannya: pakai baris i untuk menolkan A[h, i] semua baris DI ATASNYA
def nolkan_atas_pivot(A, b, i):
    for h in range(i - 1, -1, -1):
        m = A[h, i] / A[i, i]
        A[h, :] -= m * A[i, :]
        b[h] -= m * b[i]


# tahap 1: untuk tiap kolom pilih pivot lalu nolkan yang di bawah -> A jadi segitiga atas
def eliminasi_maju(A, b):
    n = len(A)
    for i in range(n - 1):
        k = cari_pivot(A, i, i)
        if k != i:
            tukar_baris(A, b, i, k)
        nolkan_bawah_pivot(A, b, i)
    return A, b


# tahap 2: untuk tiap kolom nolkan yang di ATAS pivot -> A jadi matriks diagonal
def eliminasi_mundur(A, b):
    n = len(A)
    for i in range(n - 1, 0, -1):
        nolkan_atas_pivot(A, b, i)
    return A, b


# karena A sudah diagonal, tiap x langsung ketemu dengan satu pembagian (tanpa substitusi)
def hitung_x(A, b):
    n = len(A)
    x = np.zeros(n)
    for i in range(n):
        x[i] = b[i] / A[i, i]
    return x


# pembungkus: eliminasi maju -> eliminasi mundur -> bagi; hasilkan x saja
def eliminasi_gauss_jordan(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    A, b = eliminasi_maju(A, b)
    print(A)

    A, b = eliminasi_mundur(A, b)
    print(A)

    x = hitung_x(A, b)
    return x


if __name__ == "__main__":
    A = [[2, 1, -1], [4, 3, 1], [-2, 1, 2]]
    b = [3, 9, 4]

    x = eliminasi_gauss_jordan(A, b)
    print(x)