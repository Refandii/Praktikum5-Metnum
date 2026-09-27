import numpy as np


# cari nomor baris dengan |A[baris, kolom]| paling besar, dari mulai_baris ke bawah
def cari_pivot(A, kolom, mulai_baris):
    n = len(A)
    return np.argmax(np.abs(A[mulai_baris:n, kolom])) + mulai_baris


# tukar posisi dua baris pada satu matriks saja
def tukar_baris(A, baris1, baris2):
    A[[baris1, baris2]] = A[[baris2, baris1]]


# tukar baris pada L tapi hanya kolom kiri pivot, supaya diagonal 1 di L tetap utuh
def tukar_baris_kiri(L, baris1, baris2, kolom):
    if baris1 != baris2 and kolom > 0:
        L[[baris1, baris2], :kolom] = L[[baris2, baris1], :kolom]


# hitung pengali m = A[h, i]/A[i, i], simpan ke L[h, i], lalu tolakkan baris h dengan m
def eliminasi_kolom(A, L, i):
    n = len(A)
    for h in range(i + 1, n):
        L[h, i] = A[h, i] / A[i, i]
        A[h, :] -= L[h, i] * A[i, :]


# pecah A jadi L, U, dan catatan tukar; U = A setelah bawahnya dinolkan, L = rekaman pengali
def faktorkan_lu(A):
    A = np.array(A, dtype=float)
    n = len(A)
    L = np.eye(n)
    tukar = []

    for i in range(n - 1):
        k = cari_pivot(A, i, i)
        if k != i:
            tukar_baris(A, i, k)
            tukar_baris_kiri(L, i, k, i)
            tukar.append((i, k))
        if A[i, i] == 0:
            raise ValueError("matriks singular, solusi tidak tunggal")
        eliminasi_kolom(A, L, i)

    if A[n - 1, n - 1] == 0:
        raise ValueError("matriks singular, solusi tidak tunggal")
    return L, A, tukar


# ubah catatan tukar jadi matriks P sungguhan, sehingga P A = L U
def matriks_p(tukar, n):
    P = np.eye(n)
    for i, k in tukar:
        tukar_baris(P, i, k)
    return P


# selesaikan L z = y, dari baris paling atas turun ke bawah
def substitusi_maju(L, y):
    n = len(y)
    z = np.zeros(n)
    for i in range(n):
        z[i] = (y[i] - L[i, :i] @ z[:i]) / L[i, i]
    return z


# selesaikan U x = y, dari baris paling bawah naik ke atas
def substitusi_mundur(U, y):
    n = len(y)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - U[i, i + 1:] @ x[i + 1:]) / U[i, i]
    return x


# pembungkus: faktorkan sekali, lalu dua substitusi (L z = P b, U x = z)
def lu_solusi(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    L, U, tukar = faktorkan_lu(A)
    P = matriks_p(tukar, len(b))
    z = substitusi_maju(L, P @ b)
    x = substitusi_mundur(U, z)
    return x, L, U, P


if __name__ == "__main__":
    A = [[2, 1, -1], [4, 3, 1], [-2, 1, 2]]
    b = [3, 9, 4]

    x, L, U, P = lu_solusi(A, b)

    print("A mula-mula =\n", np.array(A, dtype=float))
    print("b mula-mula =", np.array(b, dtype=float))
    print()
    print("P = catatan tukar baris =\n", P)
    print("L = segitiga bawah, diagonal 1, isinya pengali m =\n", np.round(L, 4))
    print("U = segitiga atas, A setelah bagian bawahnya dinolkan =\n", np.round(U, 4))
    print()
    print("cek P A = L U ?", np.allclose(P @ np.array(A, dtype=float), L @ U))
    print("x =", np.round(x, 4))
    print("cek A x =", np.round(np.array(A, dtype=float) @ x, 4))