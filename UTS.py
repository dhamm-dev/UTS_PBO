"""
SISTEM RESERVASI HOTEL BERBASIS PEMROGRAMAN BERORIENTASI OBJEK (PBO)
Anggota Kelompok:
1. Mohammad arifin Ilham (25041110006)
2. Idham Kholid          (250411100013)
3. Restu Dwi Haqiqi      (250411100097)
4. Bayu Surya wijaya     (250411100190)
"""

from abc import ABC, abstractmethod


# ==============================================================================
# 1. ABSTRACTION & ENCAPSULATION
# ==============================================================================

class Tamu:
    """Class Tamu dengan enkapsulasi data pribadi."""
    def __init__(self, nama: str, no_telepon: str, nik: str):
        # Public attribute
        self.nama = nama
        
        # Protected attribute (konvensi internal modul)
        self._no_telepon = no_telepon
        
        # Private attribute (name mangling, data sensitif)
        self.__nik = nik

    # Getter & Setter untuk NIK
    @property
    def nik(self) -> str:
        # Menampilkan format tersensor untuk keamanan
        return f"***{self.__nik[-4:]}"

    def get_info_tamu(self) -> str:
        return f"Tamu: {self.nama} | Telp: {self._no_telepon} | NIK: {self.nik}"


class Kamar(ABC):
    """
    Abstract Class Kamar sebagai kerangka dasar (Abstraction).
    Menerapkan Enkapsulasi: Public, Protected (_), dan Private (__).
    """
    def __init__(self, nomor_kamar: str, tipe: str, harga_dasar: float):
        # Protected attributes: diakses oleh class ini dan subclass
        self._nomor_kamar = nomor_kamar
        self._tipe = tipe
        self._tersedia = True
        
        # Private attribute: hanya dapat dimodifikasi lewat setter ber-validasi
        self.__harga_dasar = 0.0
        self.harga_dasar = harga_dasar  # Memanggil setter untuk validasi

    # GETTER (Public Interface)
    @property
    def nomor_kamar(self) -> str:
        return self._nomor_kamar

    @property
    def tipe(self) -> str:
        return self._tipe

    @property
    def is_tersedia(self) -> bool:
        return self._tersedia

    @property
    def harga_dasar(self) -> float:
        return self.__harga_dasar

    # SETTER dengan validasi data (Encapsulation)
    @harga_dasar.setter
    def harga_dasar(self, nilai: float):
        if nilai <= 0:
            raise ValueError("Tarif dasar kamar harus lebih besar dari Rp 0!")
        self.__harga_dasar = float(nilai)

    # Public Method untuk mengubah ketersediaan
    def set_ketersediaan(self, status: bool):
        self._tersedia = status

    # ABSTRACT METHOD: Wajib di-override oleh seluruh subclass
    @abstractmethod
    def hitung_total_biaya(self, malam: int) -> float:
        pass

    def deskripsi(self) -> str:
        status_str = "Tersedia" if self._tersedia else "Dipesan"
        return f"Kamar {self._nomor_kamar} [{self._tipe}] - Tarif Dasar: Rp {self.__harga_dasar:,.0f}/malam ({status_str})"


# ==============================================================================
# 2. INHERITANCE & METHOD OVERRIDING
# ==============================================================================

class KamarStandard(Kamar):
    """Subclass Kamar Standard: Tarif flat tanpa biaya tambahan."""
    def __init__(self, nomor_kamar: str, harga_dasar: float):
        super().__init__(nomor_kamar, "Standard", harga_dasar)

    # Method Overriding
    def hitung_total_biaya(self, malam: int) -> float:
        return self.harga_dasar * malam


class KamarDeluxe(Kamar):
    """Subclass Kamar Deluxe: Tarif dasar ditambah paket sarapan harian."""
    def __init__(self, nomor_kamar: str, harga_dasar: float, biaya_sarapan: float = 75000):
        super().__init__(nomor_kamar, "Deluxe", harga_dasar)
        self.biaya_sarapan = biaya_sarapan

    # Method Overriding
    def hitung_total_biaya(self, malam: int) -> float:
        biaya_per_malam = self.harga_dasar + self.biaya_sarapan
        return biaya_per_malam * malam


class KamarSuite(Kamar):
    """Subclass Kamar Suite: Layanan lounge VIP + diskon durasi menginap (>3 malam)."""
    def __init__(self, nomor_kamar: str, harga_dasar: float, biaya_lounge: float = 200000):
        super().__init__(nomor_kamar, "Suite", harga_dasar)
        self.biaya_lounge = biaya_lounge

    # Method Overriding
    def hitung_total_biaya(self, malam: int) -> float:
        subtotal = (self.harga_dasar + self.biaya_lounge) * malam
        # Diskon 10% jika menginap lebih dari 3 malam
        if malam > 3:
            subtotal *= 0.90
        return subtotal


# ==============================================================================
# 3. CLASS PENGELOLA (COMPOSITION & POLYMORPHISM)
# ==============================================================================

class Reservasi:
    """Komposisi yang menghubungkan Tamu dan Kamar."""
    def __init__(self, id_reservasi: str, tamu: Tamu, kamar: Kamar, durasi_malam: int):
        self.id_reservasi = id_reservasi
        self.tamu = tamu
        self.kamar = kamar
        self.durasi_malam = durasi_malam
        # Tandai kamar langsung dipesan
        self.kamar.set_ketersediaan(False)

    # POLYMORPHISM: memanggil hitung_total_biaya tanpa peduli jenis kamar konkret
    def hitung_total(self) -> float:
        return self.kamar.hitung_total_biaya(self.durasi_malam)

    def cetak_invoice(self):
        print("=" * 50)
        print(f"            INVOICE RESERVASI HOTEL #{self.id_reservasi}")
        print("=" * 50)
        print(f"Nama Tamu     : {self.tamu.nama}")
        print(f"Kontak/NIK    : {self.tamu.get_info_tamu()}")
        print(f"Kamar         : {self.kamar.nomor_kamar} ({self.kamar.tipe})")
        print(f"Durasi        : {self.durasi_malam} Malam")
        print(f"Tarif Dasar   : Rp {self.kamar.harga_dasar:,.0f} / malam")
        print("-" * 50)
        print(f"TOTAL TAGIHAN : Rp {self.hitung_total():,.0f}")
        print("=" * 50)


class Hotel:
    """Class Pengelola Utama (Menggunakan Komposisi untuk daftar kamar dan transaksi)."""
    def __init__(self, nama_hotel: str):
        self.nama_hotel = nama_hotel
        # Komposisi: Hotel memiliki koleksi Kamar dan Reservasi
        self._daftar_kamar = []
        self._daftar_reservasi = []
        self.__counter_reservasi = 100

    def tambah_kamar(self, kamar: Kamar):
        self._daftar_kamar.append(kamar)

    def cari_kamar(self, nomor: str):
        for k in self._daftar_kamar:
            if k.nomor_kamar == nomor:
                return k
        return None

    def tampilkan_semua_kamar(self):
        print(f"\n--- KATALOG KAMAR {self.nama_hotel.upper()} ---")
        if not self._daftar_kamar:
            print("Belum ada data kamar.")
            return
        for kamar in self._daftar_kamar:
            print(kamar.deskripsi())

    def buat_reservasi(self, tamu: Tamu, nomor_kamar: str, malam: int) -> bool:
        kamar = self.cari_kamar(nomor_kamar)
        if not kamar:
            print(f"Gagal: Kamar {nomor_kamar} tidak ditemukan!")
            return False
        if not kamar.is_tersedia:
            print(f"Gagal: Kamar {nomor_kamar} saat ini sedang terisi/dipesan!")
            return False

        self.__counter_reservasi += 1
        id_res = f"RSV-{self.__counter_reservasi}"
        reservasi_baru = Reservasi(id_res, tamu, kamar, malam)
        self._daftar_reservasi.append(reservasi_baru)
        print(f"\nReservasi berhasil dibuat dengan ID: {id_res}")
        reservasi_baru.cetak_invoice()
        return True

    def tampilkan_riwayat_reservasi(self):
        print(f"\n--- RIWAYAT RESERVASI {self.nama_hotel.upper()} ---")
        if not self._daftar_reservasi:
            print("Belum ada reservasi aktif.")
            return
        
        # POLYMORPHISM IN ACTION:
        # Menghitung tagihan tiap reservasi tanpa if-else tipe kamar
        total_pendapatan = 0.0
        for r in self._daftar_reservasi:
            tagihan = r.hitung_total()
            total_pendapatan += tagihan
            print(f"[{r.id_reservasi}] Tamu: {r.tamu.nama} | Kamar: {r.kamar.nomor_kamar} ({r.kamar.tipe}) | {r.durasi_malam} Malam | Total: Rp {tagihan:,.0f}")
        print("-" * 50)
        print(f"Total Pendapatan Terakumulasi: Rp {total_pendapatan:,.0f}")

    def checkout_kamar(self, nomor_kamar: str):
        kamar = self.cari_kamar(nomor_kamar)
        if kamar and not kamar.is_tersedia:
            kamar.set_ketersediaan(True)
            print(f"Check-out berhasil! Kamar {nomor_kamar} kini kembali tersedia.")
        else:
            print(f"Kamar {nomor_kamar} tidak sedang dalam status dipesan.")


# ==============================================================================
# 4. PROGRAM UTAMA (CLI INTERAKTIF)
# ==============================================================================

def inisialisasi_data(hotel: Hotel):
    """Menambahkan data awal kamar."""
    hotel.tambah_kamar(KamarStandard("101", 350000))
    hotel.tambah_kamar(KamarStandard("102", 350000))
    hotel.tambah_kamar(KamarDeluxe("201", 600000, biaya_sarapan=80000))
    hotel.tambah_kamar(KamarDeluxe("202", 600000, biaya_sarapan=80000))
    hotel.tambah_kamar(KamarSuite("301", 1200000, biaya_lounge=250000))


def main():
    hotel = Hotel("Grand Madura Hotel")
    inisialisasi_data(hotel)

    while True:
        print("\n" + "=" * 45)
        print(f"   SISTEM RESERVASI {hotel.nama_hotel.upper()}")
        print("=" * 45)
        print("1. Lihat Daftar Kamar")
        print("2. Tambah Kamar Baru")
        print("3. Buat Reservasi Kamar")
        print("4. Riwayat Reservasi & Rekap Pendapatan")
        print("5. Check-out Tamu")
        print("0. Keluar")
        print("=" * 45)
        
        pilihan = input("Pilih menu (0-5): ").strip()

        if pilihan == "1":
            hotel.tampilkan_semua_kamar()

        elif pilihan == "2":
            print("\n--- Tambah Kamar Baru ---")
            no = input("Nomor Kamar: ").strip()
            print("Pilihan Tipe: 1. Standard  2. Deluxe  3. Suite")
            tipe_opsi = input("Pilih Tipe (1-3): ").strip()
            try:
                tarif = float(input("Tarif Dasar per Malam: Rp "))
                if tipe_opsi == "1":
                    hotel.tambah_kamar(KamarStandard(no, tarif))
                elif tipe_opsi == "2":
                    sarapan = float(input("Biaya Sarapan Tambahan: Rp "))
                    hotel.tambah_kamar(KamarDeluxe(no, tarif, sarapan))
                elif tipe_opsi == "3":
                    lounge = float(input("Biaya Layanan Lounge VIP: Rp "))
                    hotel.tambah_kamar(KamarSuite(no, tarif, lounge))
                else:
                    print("Tipe kamar tidak valid!")
                    continue
                print(f"Kamar {no} berhasil ditambahkan.")
            except ValueError as e:
                print(f"Input tidak valid: {e}")

        elif pilihan == "3":
            print("\n--- Formulir Reservasi ---")
            nama = input("Nama Tamu       : ").strip()
            telp = input("Nomor Telepon   : ").strip()
            nik = input("NIK             : ").strip()
            no_kamar = input("Nomor Kamar     : ").strip()
            try:
                malam = int(input("Durasi Menginap (malam): "))
                if malam <= 0:
                    print("Durasi malam harus minimal 1.")
                    continue
                tamu = Tamu(nama, telp, nik)
                hotel.buat_reservasi(tamu, no_kamar, malam)
            except ValueError:
                print("Durasi menginap harus berupa angka bulat.")

        elif pilihan == "4":
            hotel.tampilkan_riwayat_reservasi()

        elif pilihan == "5":
            no_kamar = input("Masukkan Nomor Kamar yang Check-out: ").strip()
            hotel.checkout_kamar(no_kamar)

        elif pilihan == "0":
            print("\nTerima kasih telah menggunakan sistem reservasi.")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")


if __name__ == "__main__":
    main()