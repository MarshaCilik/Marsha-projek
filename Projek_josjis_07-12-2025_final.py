import psycopg2 as pg
from tabulate import tabulate
import pyfiglet as pf
from colorama import Fore, Back, Style, init
import questionary as q

init(autoreset=True)

conn = pg.connect(
    host = "localhost",
    database = "projek_basdah",
    user = "postgres",
    password = "devara2006",
    port = "5432"
)
mycursor = conn.cursor()

pkUser_recent = None
user_recent = ''
namauser = ''
pilihanUtamaPetani = None
kategori_valid = ["sayuran", "buah", "bahan pokok"]
pkKeranjang_recent = None
symbols = "!@#$%^&*()_+-=[]{}|;:'\",.<>?/`~"

def checkKecamatan(entitas, atribut, lokasi):
    mycursor.execute("select setval('kecamatan_id_kecamatan_seq', (SELECT MAX(id_kecamatan) from kecamatan))")#PERUBAHAN PENTING DARI RANI
    mycursor.execute(f"SELECT EXISTS (SELECT 1 FROM {entitas} WHERE {atribut} ilike '%{lokasi}%')")
    row = mycursor.fetchone()[0]
    if row == False:
        mycursor.execute(f"insert into {entitas} ({atribut}) values ('{lokasi}')")
        mycursor.execute(f"select * from {entitas} where {atribut} ilike '%{lokasi}%'")
        pk = mycursor.fetchone()[0]
        conn.commit()
    elif row == True:
        mycursor.execute(f"select * from {entitas} where {atribut} ilike '%{lokasi}%'")
        pk = mycursor.fetchone()[0]
        conn.commit()
    return pk

def signup_petani():
    mycursor.execute("select setval('desa_id_desa_seq', (SELECT MAX(id_desa) from desa))")  
    mycursor.execute("select setval('kecamatan_id_kecamatan_seq', (SELECT MAX(id_kecamatan) from kecamatan))")
    header = "PASTANI"
    headerbagus = pf.figlet_format(header, font="slant")
    print(headerbagus)
    print("SIGN UP sebagai petani\n")

#USERNAME
    while True:
        username = ''
        username = kekosongan(username, 'username')
        if any(s in username for s in symbols):
            print(f"Tolong jangan memasukkan simbol({symbols}) pada username!")
            continue
        elif not any(s in username for s in symbols):
            if username.isdigit():
                print("username tidak boleh penuh angka!")
                continue
            elif not username.isdigit():
                mycursor.execute(f"select exists (select 1 from petani where username = '{username}')")
                cekusername = mycursor.fetchone()[0]
                if cekusername == True:
                    print("username telah digunakan!")
                    continue
                elif cekusername == False:
                    break
                
            
        


    # mycursor.execute(f"select exists (select 1 from petani where username ilike '{username}')")
    # cekusername = mycursor.fetchone()[0]
    # while cekusername == True:
    #     print("username telah digunakan!")
    #     username = kekosongan(username, 'username')
    #     mycursor.execute(f"select exists (select 1 from petani where username ilike '{username}')")
    #     cekusernameLagi = mycursor.fetchone()[0]
    #     if cekusernameLagi == False:
    #         print("username bisa digunakan!")
    #         break
    password = ''
    password = kekosongan(password,'password')
    
    nama = ''
    nama = kekosongan(nama,'nama')
    

#NOMOR
    nomor = ''
    nomor = kekosongan(nomor,'Nomor Telepon')
    
    while len(nomor) > 13:
        print("Nomor tidak boleh lebih dari 13!")
        nomor = kekosongan(nomor,'Nomor Telepon')
    mycursor.execute(f"select exists (select 1 from petani where nomor_telepon ilike '{nomor}')")
    ceknomor = mycursor.fetchone()[0]
    while ceknomor == True:
        print("nomor sudah terdaftar!")
        nomor = kekosongan(nomor,'Nomor Telepon')
        mycursor.execute(f"select exists (select 1 from petani where nomor_telepon ilike '{nomor}')")
        cekNomorLagi = mycursor.fetchone()[0]
        if cekNomorLagi == False:
            print("Nomor bisa digunakan!")
            break

#EMAIL
    email = ''
    email = kekosongan(email,'email')
    
    while not '@' in email:
        print("tolong masukkan email menggunakan '@'")
        email = kekosongan(email,'email')
    mycursor.execute(f"select exists (select 1 from petani where email ilike '{email}')")
    cekEmail = mycursor.fetchone()[0]
    while cekEmail == True:
        print("email sudah terdaftar!")
        email = kekosongan(email,'email')
        mycursor.execute(f"select exists (select 1 from petani where email ilike '{email}')")
        cekEmailLagi = mycursor.fetchone()[0]
        if cekEmailLagi == False:
            print("\nemail bisa digunakan!\n")
            break

#ALAMAT
    alamat = ''
    alamat = kekosongan(alamat,'alamat')
    
    mycursor.execute(f"select exists (select 1 from alamat where nama_jalan ilike '{alamat}')")
    cekAlamatAda = mycursor.fetchone()[0]
    while cekAlamatAda == True:
        print("Maaf alamat sudah digunakan")
        alamat = kekosongan(alamat,'alamat')
        mycursor.execute(f"select exists (select 1 from alamat where nama_jalan ilike '{alamat}')")
        cekAlamatLagi = mycursor.fetchone()[0]
        if cekAlamatLagi == False:
            print("\nAlamat bisa digunakan!\n")
            break

    desa = ''
    desa = kekosongan(desa,'desa')
    
    kecamatan = ''
    kecamatan = kekosongan(kecamatan,'kecamatan')
    
    checkKecamatan('kecamatan', 'nama_kecamatan', kecamatan)
    mycursor.execute(f"SELECT EXISTS (SELECT 1 FROM desa WHERE nama_desa ilike '{desa}')")
    row = mycursor.fetchone()[0]
    if row == False:
        mycursor.execute(f"insert into desa (nama_desa, id_kecamatan) values ('{desa}', '{checkKecamatan('kecamatan', 'nama_kecamatan', kecamatan)}')")
        mycursor.execute(f"select * from desa where nama_desa ilike '{desa}'")
        pkDesa = mycursor.fetchone()[0]
        mycursor.execute(f"insert into alamat (nama_jalan, id_desa) values ('{alamat}','{pkDesa}')")
        mycursor.execute(f"select * from alamat where nama_jalan ilike '{alamat}'") #cek pk alamat
        pkAlamat = mycursor.fetchone()[0]
        mycursor.execute(f"insert into petani (nama_petani, nomor_telepon, email, username, password_petani, status_petani, id_alamat) values ('{nama}', '{nomor}', '{email}', '{username}', '{password}', FALSE, '{pkAlamat}')")
    elif row == True:
        mycursor.execute(f"select * from desa where nama_desa ilike '{desa}'")
        pkDesa = mycursor.fetchone()[0] #mengambil pk desa
        mycursor.execute(f"insert into alamat (nama_jalan, id_desa) values ('{alamat}','{pkDesa}')")
        mycursor.execute(f"select * from alamat where nama_jalan ilike '{alamat}'") #cek pk alamat
        pkAlamat = mycursor.fetchone()[0]
        mycursor.execute(f"insert into petani (nama_petani, nomor_telepon, email, username, password_petani, status_petani, id_alamat) values ('{nama}', '{nomor}', '{email}', '{username}', '{password}', FALSE, '{pkAlamat}')")

    conn.commit()
    print("\nAKUN TELAH DIDAFTARKAN\n")
    input("Tekan enter untuk melanjutkan...")
    
def kekosongan(x, y):
    x = input(f'{y}: ')
    while len(x.strip()) == 0:
        print(f"{y} tidak boleh kosong atau spasi")
        x = input(f'{y}: ')
        if not len(x.strip()) == 0:
            break
    return x
    
        
def signup_konsumen():
    mycursor.execute("select setval('desa_id_desa_seq', (SELECT MAX(id_desa) from desa))")  
    mycursor.execute("select setval('kecamatan_id_kecamatan_seq', (SELECT MAX(id_kecamatan) from kecamatan))")#PERUBAHAN TIWI
    header = "PASTANI"
    headerbagus = pf.figlet_format(header, font="slant")
    print(headerbagus)
    print("SIGN UP sebagai customer\n")

#USERNAME
    while True:
        username = ''
        username = kekosongan(username, 'username')
        if any(s in username for s in symbols):
            print(f"Tolong jangan memasukkan simbol({symbols}) pada username!")
            continue
        elif not any(s in username for s in symbols):
            if username.isdigit():
                print("username tidak boleh penuh angka!")
                continue
            elif not username.isdigit():
                mycursor.execute(f"select exists (select 1 from konsumen where username = '{username}')")
                cekusername = mycursor.fetchone()[0]
                if cekusername == True:
                    print("username telah digunakan!")
                    continue
                elif cekusername == False:
                    break
    password = ''
    password = kekosongan(password, 'password')
    
    nama = ''
    nama = kekosongan(nama, 'nama')

#NOMOR
    nomor = ''
    nomor = kekosongan(nomor, 'Nomor Telepon')
    while len(nomor) > 13:
        print("Nomor tidak boleh lebih dari 13!")
        nomor = kekosongan(nomor,'Nomor Telepon')
    mycursor.execute(f"select exists (select 1 from konsumen where nomor_telepon ilike '{nomor}')")
    ceknomor = mycursor.fetchone()[0]
    while ceknomor == True:
        print("nomor sudah terdaftar!")
        nomor = nomor = kekosongan(nomor, 'nomor')
        mycursor.execute(f"select exists (select 1 from konsumen where nomor_telepon ilike '{nomor}')")
        cekNomorLagi = mycursor.fetchone()[0]
        if cekNomorLagi == False:
            print("Nomor bisa digunakan!")
            break
    
#EMAIL
    email = ''
    email = kekosongan(email, 'email')
    
    while not '@' in email:
        print("tolong masukkan email menggunakan '@'")
        email = input("Email: ")
    mycursor.execute(f"select exists (select 1 from konsumen where email ilike '{email}')")
    cekEmail = mycursor.fetchone()[0]
    while cekEmail == True:
        print("email sudah terdaftar!")
        email = input("Email: ")
        mycursor.execute(f"select exists (select 1 from konsumen where email ilike '{email}')")
        cekEmailLagi = mycursor.fetchone()[0]
        if cekEmailLagi == False:
            print("\nemail bisa digunakan!\n")
            break

#ALAMAT
    alamat = ''
    alamat = kekosongan(alamat,'alamat')
    
    mycursor.execute(f"select exists (select 1 from alamat where nama_jalan ilike '{alamat}')")
    cekAlamatAda = mycursor.fetchone()[0]
    while cekAlamatAda == True:
        print("Maaf alamat sudah digunakan")
        alamat = kekosongan(alamat,'alamat')
        mycursor.execute(f"select exists (select 1 from alamat where nama_jalan ilike '{alamat}')")
        cekAlamatLagi = mycursor.fetchone()[0]
        if cekAlamatLagi == False:
            print("\nAlamat bisa digunakan!\n")
            break

    desa = ''
    desa = kekosongan(desa, 'desa')
    
    kecamatan = ''
    kecamatan = kekosongan(kecamatan, 'kecamatan')
    
    checkKecamatan('kecamatan', 'nama_kecamatan', kecamatan)
    mycursor.execute(f"SELECT EXISTS (SELECT 1 FROM desa WHERE nama_desa ilike '{desa}')")
    row = mycursor.fetchone()[0]
    if row == False:
        mycursor.execute("SELECT setval('desa_id_desa_seq', (SELECT MAX(id_desa) from desa))") #PERUBAHAN TIWI
        mycursor.execute(f"insert into desa (nama_desa, id_kecamatan) values ('{desa}', '{checkKecamatan('kecamatan', 'nama_kecamatan', kecamatan)}')")
        mycursor.execute(f"select * from desa where nama_desa ilike '%{desa}%'")
        pkDesa = mycursor.fetchone()[0]
        mycursor.execute(f"insert into alamat (nama_jalan, id_desa) values ('{alamat}','{pkDesa}')")
        mycursor.execute(f"select * from alamat where nama_jalan ilike '{alamat}'") #cek pk alamat
        pkAlamat = mycursor.fetchone()[0]
        mycursor.execute(f"insert into konsumen (nama_konsumen, nomor_telepon, email, username, password_konsumen, id_alamat) values ('{nama}', '{nomor}', '{email}', '{username}', '{password}', '{pkAlamat}')")
    elif row == True:
        mycursor.execute(f"select * from desa where nama_desa ilike '%{desa}%'")
        pkDesa = mycursor.fetchone()[0] #mengambil pk desa
        mycursor.execute(f"insert into alamat (nama_jalan, id_desa) values ('{alamat}','{pkDesa}')")
        mycursor.execute(f"select * from alamat where nama_jalan ilike '{alamat}'") #cek pk alamat
        pkAlamat = mycursor.fetchone()[0]
        mycursor.execute(f"insert into konsumen (nama_konsumen, nomor_telepon, email, username, password_konsumen, id_alamat) values ('{nama}', '{nomor}', '{email}', '{username}', '{password}', '{pkAlamat}')")

    mycursor.execute(f"select id_konsumen from konsumen where username like '{username}'")
    Keranmen = mycursor.fetchone()[0]
    mycursor.execute(f"insert into keranjang(id_konsumen) values ({Keranmen})")
    conn.commit()
    print("\nAKUN TELAH DIDAFTARKAN\n")
    input("Tekan enter untuk melanjutkan...")

def loginFunction(role):
    while True:
        global pkUser_recent
        global user_recent
        try:
            print("KOSONGKAN LALU ENTER UNTUK KEMBALI")
            username = input("username: ").strip()
            if username == '':
                return
            mycursor.execute(f"select exists (select 1 from {role} where username ilike '{username}')")
            cekKeberadaan = mycursor.fetchone()[0]
            while cekKeberadaan == False:
                print("Username tidak terdaftar!")
                username = input("username: ")
                if username == '':
                    return
                mycursor.execute(f"select exists (select 1 from {role} where username ilike '{username}')")
                cekKeberadaan = mycursor.fetchone()[0]
                if cekKeberadaan == True:
                    print("\nusername benar!\n")
                    break

            password = input("password: ")
            if password == '':
                return
            mycursor.execute(f"select password_{role} from {role} where username ilike '{username}'")
            cekpassword = mycursor.fetchone()[0]
            while password != cekpassword:
                print("PASSWORD SALAH!")
                password = input("password: ")
                mycursor.execute(f"select password_{role} from {role} where username ilike '{username}'")
                cekpassword = mycursor.fetchone()[0]
                if password == cekpassword:
                    print("password benar!")
            user_recent = username
            mycursor.execute(f"select id_{role} from {role} where username ilike '{user_recent}'")
            pkUser_recent = mycursor.fetchone()[0]
            print('LOGIN BERHASIL!')
            return username
        except Exception as e:
            print("Mohon maaf terjadi kesalahan: ", e)
        finally:
            input("Tekan enter untuk melanjutkan...")
  
def signup():
    header = "PASTANI"
    headerbagus = pf.figlet_format(header, font="slant")
    print(headerbagus)
    print("HALAMAN SIGN UP")
    sebagai = q.select("Daftar sebagai: ", choices=[
        "Petani",
        "Customer",
        "Kembali"
    ]).ask()
    if sebagai == 'Petani':
        signup_petani()
    elif sebagai == 'Customer':
        signup_konsumen()
    elif sebagai == 'Kembali':
        print()
     

def login():
    global user_recent
    try:
        while True:
            header = pf.figlet_format("PASTANI", font="slant")
            print(header)
            print("HALAMAN LOG IN")
            sebagai = q.select("Log in sebagai: ", choices=[
                "Petani",
                "Customer",
                "Admin",
                "Kembali",
            ]).ask()
            if sebagai == 'Petani':
                loginFunction('petani')
                halamanUtamaPetani()
                break
            elif sebagai == 'Customer':
                loginFunction('konsumen')
                halamanUtamaCustomer()
                break
            elif sebagai == 'Admin':
                loginFunction('admin')
                halamanUtamaAdmin()
                break
            elif sebagai == 'Kembali':
                break
            else:
                print("Masukkan input dengan benar!")
    except Exception as e:
        print("Terjadi Kesalahan pada halaman login: ",e)

def input_berat():
    berat = ''
    berat = kekosongan(berat, 'berat').strip().lower()
    if berat.endswith("kg"):
        return berat
    if berat.endswith("g") or berat.endswith("gram"):
        return berat
    return berat + "kg"

def tabelProdukTani():
    global pkUser_recent
    mycursor.execute(f"select id_petani from petani where username ilike '{user_recent}'")
    pkUser = mycursor.fetchone()[0]
    mycursor.execute(f"""select id_produk, nama_produk, harga_produk, stok_produk,
                     case when status_produk = true then 'aktif'
                     else 'tidak aktif' end as status_produk 
                      from produk_tani where id_petani = {pkUser}""")
    tabel = mycursor.fetchall()
    print("Berikut data produk\n")
    print(tabulate(tabel, headers= ("ID produk","nama produk", "harga", "stok", "status produk")))
    pkUser = pkUser_recent

def HasilTani():
    mycursor.execute(f"select id_petani from petani where username ilike '{user_recent}'")
    pkUser_recent = mycursor.fetchone()[0] #MENGINGAT PK USER
    try:
        while True:
            tabelProdukTani()
            print("OPSI")
            print("[1] Menambah produk baru hasil panen")
            print("[2] Menambah produk hasil panen yang sudah ada")
            print("[3] Menonaktifkan dan mengaktifkan produk hasil panen")
            print("[0] Kembali")
            pilihan = input("Pilihan (1-3):\n")
            if pilihan == '1':
                print("\nOPSI: [1] Menambah produk baru hasil panen")
                print("TEKAN 0 UNTUK KEMBALI")
                produk = ''
                produk = kekosongan(produk, 'produk')
                if produk == '0':
                    break
                berat = ''
                berat = input_berat()
                if berat == '0':
                    break
                harga = ''
                harga = int(kekosongan(harga, "harga"))
                if harga == '0':
                    break
                stok = ''
                stok = int(kekosongan(stok, 'stok'))
                if stok == '0':
                    break
                while True:
                    jenis = ''
                    print("jenis harus berisi sayuran/buah/bahan pokok")
                    jenis = kekosongan(jenis, "jenis").lower()
                    if jenis in kategori_valid:
                        break
                    else:
                        print("input tidak valid!")
                mycursor.execute(f"""select id_jenis_produk from jenis_produk
                            where jenis_produk ilike '{jenis}'""")
                pkJenis = mycursor.fetchone()[0]
                mycursor.execute(f"""insert into produk_tani(nama_produk, harga_produk, stok_produk, status_produk,id_petani,id_jenis_produk)
                                    values ('{produk} {berat}', '{harga}', {stok}, TRUE, {pkUser_recent}, {pkJenis})""")
                print("Data berhasil diupdate!")
                input("Tekan enter...")
                conn.commit()
            elif pilihan == '2':
                print("\nOPSI: [2] Menambah produk hasil panen yang sudah ada")
                print("""
SILAKAN PILIH OPSI DI BAWAH:
[1] Menambah stok
[2] Mengubah stok terbaru
[3] Mengubah harga produk
[0] Kembali
                      """)
                pilihan2 = input()
                if pilihan2 == '1': #MENAMBAH STOK
                    tabelProdukTani()
                    print("OPSI : [1] Menambah stok")
                    print("KETIK 0 UNTUK KEMBALI")
                    idProduk = None
                    print("Pilih id produk yang akan di tambah stoknya:")
                    while True:
                        try :
                            while True:
                                idProduk = int(kekosongan(idProduk, "id produk"))
                                if idProduk == 0:
                                    return
                                mycursor.execute(f"SELECT EXISTS (SELECT 1 FROM produk_tani WHERE id_produk = {idProduk} and id_petani = {pkUser_recent})")
                                cekIdProduk = mycursor.fetchone()[0]
                                if cekIdProduk == False:
                                    print("Data tidak ada")
                                elif cekIdProduk == True:
                                    print("Produk ada")
                                    break
                            break
                        except ValueError:
                            print("Input harus berupa angka integer! Coba lagi.")
                    tambahStok = ''
                    print("Masukkan jumlah produk: ")
                    while True:
                        try :
                            tambahStok = int(kekosongan(tambahStok, "stok"))
                            if tambahStok == 0:
                                return
                            break
                        except ValueError:
                            print("Input harus berupa angka integer! Coba lagi.")
                    mycursor.execute(f"""
                                    UPDATE produk_tani
                                    SET stok_produk = stok_produk + {tambahStok}
                                    WHERE id_produk = {idProduk};
                                     """)
                    input("""Data berhasil ditambahkan!
tekan enter untuk lanjut...""")
                    conn.commit()
                elif pilihan2 == '2':
                    tabelProdukTani()
                    print("OPSI : [2] Mengubah stok terbaru")
                    idProduk = None
                    print("Pilih id produk yang akan di rubah stoknya:")
                    while True:
                        try :
                            while True:
                                idProduk = int(kekosongan(idProduk, "id produk"))
                                if idProduk == 0:
                                    return
                                mycursor.execute(f"SELECT EXISTS (SELECT 1 FROM produk_tani WHERE id_produk = {idProduk} and id_petani = {pkUser_recent})")
                                cekIdProduk = mycursor.fetchone()[0]
                                if cekIdProduk == False:
                                    print("Data tidak ada")
                                elif cekIdProduk == True:
                                    print("Produk ada")
                                    break
                            break
                        except ValueError:
                            print("Input harus berupa angka integer! Coba lagi.\n")
                    perubahanStok = None
                    print("Masukkan jumlah produk: ")
                    while True:
                        try :
                            perubahanStok = int(kekosongan(perubahanStok, "stok"))
                            if perubahanStok == 0:
                                return
                            break
                        except ValueError:
                            print("Input harus berupa angka integer! Coba lagi.")
                    mycursor.execute(f"""
                                    UPDATE produk_tani
                                    SET stok_produk = {perubahanStok}
                                    WHERE id_produk = {idProduk};
                                        """)
                    input("""Data berhasil ditambahkan!
tekan enter untuk lanjut...""")
                    conn.commit()
                elif pilihan2 == '3': #MERUBAH HARGAAA
                    tabelProdukTani()
                    print("OPSI : [3] Mengubah harga produk")
                    idProduk = None
                    print("Pilih id produk yang akan diubah harganya:")
                    while True:
                        try :
                            while True:
                                idProduk = int(kekosongan(idProduk, "id produk"))
                                if idProduk == 0:
                                    return
                                mycursor.execute(f"SELECT EXISTS (SELECT 1 FROM produk_tani WHERE id_produk = {idProduk} and id_petani = {pkUser_recent})")
                                cekIdProduk = mycursor.fetchone()[0]
                                if cekIdProduk == False:
                                    print("Data tidak ada")
                                elif cekIdProduk == True:
                                    print("Produk ada")
                                    break
                            break
                        except ValueError:
                            print("Input harus berupa angka integer! Coba lagi.\n")
                    perubahanHarga = None
                    print("Masukkan harga produk: ")
                    while True:
                        try :
                            perubahanHarga = int(kekosongan(perubahanHarga, "harga"))
                            if perubahanHarga == 0:
                                return
                            break
                        except ValueError:
                            print("Input harus berupa angka integer! Coba lagi.")
                    mycursor.execute(f"""
                                    UPDATE produk_tani
                                    SET harga_produk = {perubahanHarga}
                                    WHERE id_produk = {idProduk};
                                        """)
                    input("""Data berhasil ditambahkan!
tekan enter untuk lanjut...""")
                    conn.commit()
                elif pilihan2 == '0':
                    input("kembali ke menu 'mengubah hasil produk panen'...\nTekan ENTER untuk melanjutkan...")
                else :
                    print("tolong masukkan input dengan benar!")
                    input("tekan ENTER untuk melanjutkan...")

            elif pilihan == '3':
                print("OPSI: [3] Menonaktifkan dan mengaktifkan produk hasil panen")
                print("\nPilih opsi berikut: ")
                print("[1] Menonaktifkan produk")
                print("[2] Mengaktifkan produk")
                print("[0] Kembali")
                while True:
                    pilihanHapus = input()
                    if pilihanHapus == '1':
                        idProduk = None
                        print("berikut data produk tani: ")
                        tabelProdukTani()
                        print("[1] Menonaktifkan produk tani\n")
                        print("pilih id produk yang akan dinonaktifkan: ")
                        while True:
                            try :
                                while True:
                                    idProduk = int(kekosongan(idProduk, "id produk"))
                                    if idProduk == 0:
                                        return
                                    mycursor.execute(f"SELECT EXISTS (SELECT 1 FROM produk_tani WHERE id_produk = {idProduk} and id_petani = {pkUser_recent})")
                                    cekIdProduk = mycursor.fetchone()[0]
                                    if cekIdProduk == False:
                                        print("Data tidak ada")
                                    elif cekIdProduk == True:
                                        print("Produk ada")
                                        break
                                break
                            except ValueError:
                                print("Input harus berupa angka integer! Coba lagi.\n")
                        mycursor.execute(f"""
                                        UPDATE produk_tani
                                        SET status_produk = FALSE
                                        WHERE id_produk = {idProduk};
                                        """)
                        conn.commit()
                        print("produk berhasil dinonaktifkan!")
                        input("Tekan ENTER untuk kembali...")
                        break
                    elif pilihanHapus == '2':
                        idProduk = None
                        print("berikut data produk tani: ")
                        tabelProdukTani()
                        print("[2] Mengaktifkan produk tani\n")
                        print("pilih id produk yang akan diaktifkan: ")
                        while True:
                            try :
                                while True:
                                    idProduk = int(kekosongan(idProduk, "id produk"))
                                    if idProduk == 0:
                                        return
                                    mycursor.execute(f"SELECT EXISTS (SELECT 1 FROM produk_tani WHERE id_produk = {idProduk} and id_petani = {pkUser_recent})")
                                    cekIdProduk = mycursor.fetchone()[0]
                                    if cekIdProduk == False:
                                        print("Data tidak ada")
                                    elif cekIdProduk == True:
                                        print("Produk ada")
                                        break
                                break
                            except ValueError:
                                print("Input harus berupa angka integer! Coba lagi.\n")
                        mycursor.execute(f"""
                                        UPDATE produk_tani
                                        SET status_produk = TRUE
                                        WHERE id_produk = {idProduk};
                                        """)
                        print("produk berhasil diaktifkan!")
                        conn.commit()
                        input("Tekan ENTER untuk kembali...")
                        break
                    elif pilihanHapus == '0':
                        input("Tekan ENTER untuk kembali ke menu kelola hasil tani...")
                        break
                    else:
                        print("tolong masukkan input dengan benar!")
                        input("tekan ENTER untuk melanjutkan...")
            
            elif pilihan == '0':
                break
            else :
                print("tolong masukkan input dengan benar!")
                input("tekan ENTER untuk melanjutkan...")
    except Exception as e:
        print("Terjadi kesalahan", e)
        

def halamanUtamaPetani():
    if pkUser_recent == None:
        return
    mycursor.execute(f"select status_petani from petani where id_petani = {pkUser_recent}")
    akses = mycursor.fetchone()[0]
    if akses == False:
        print("Akun belum diaktifkan oleh admin.")
        input("\nTekan ENTER untuk melanjutkan...")
    elif akses == True:
        while True:
            header = pf.figlet_format("PASTANI", font="slant")
            print(header)
            print("HALAMAN UTAMA PETANI")
            print(f"Kamu login sebagai: {user_recent}")
            print(f"ID Anda: {pkUser_recent}")
            pilihanUtamaPetani = q.select("\nPilih Menu:",
                            choices=[
                                "[1] Kelola data hasil tani",
                                "[2] Lihat & Kelola Pesanan",
                                "[3] Laporan Transaksi",
                                "[4] Edit Profile",
                                "[0] Log out"
                                    ]).ask()
            if pilihanUtamaPetani == '[1] Kelola data hasil tani':
                HasilTani()
            elif pilihanUtamaPetani == '[2] Lihat & Kelola Pesanan':
                KelolaPesananTani()
            elif pilihanUtamaPetani == '[3] Laporan Transaksi':
                laporanPetani()
            elif pilihanUtamaPetani == "[4] Edit Profile":
                edit_profile('petani')
            elif pilihanUtamaPetani == '[0] Log out':
                break
            else :
                print("tolong masukkan input dengan benar!")

def main():
    while True:
        print("SELAMAT DATANG DI")
        tulisan = "PASTANI"
        tulisanbagus = pf.figlet_format(tulisan, font="slant")
        print(Fore.GREEN + tulisanbagus)
        # print("1. LOG IN")
        # print("2. SIGN UP")
        # print("0. KELUAR")
        pilihan = q.select("Menu: ", choices=[
            "LOG IN",
            "SIGN up",
            "KELUAR"
        ]).ask()

        if pilihan == 'KELUAR':
            mycursor.close()
            conn.close()
            print("Koneksi ke PostgreSQL ditutup.")
            print("SELESAI")
            break
        elif pilihan == 'LOG IN':
            login()
        elif pilihan == 'SIGN up':
            signup()


#KERJAANKU ATAS NAMA RANI
def dashboardglobal():
    global pkUser_recent
    while True:
        header = pf.figlet_format("PASTANI", font="slant")
        print(header)
        print("HALAMAN UTAMA ADMIN")
        print(f"Kamu login sebagai: {user_recent}")
        print(f"ID Anda: {pkUser_recent}")
        print("\nMENU : ")
        print("[1] Total (petani, konsumen, produk, transaksi)")
        print("[2] Jumlah stok barang")
        print("[3] jumlah transaksi berhasil/gagal")
        print("[0] Log out")
        pilihan = input()
        if pilihan == '1':
            total()
            input("Tekan ENTER untuk melanjutkan...")
        elif pilihan == '2':
            totalStokBarang()
            input("Tekan ENTER untuk melanjutkan...")
        elif pilihan == '3':
            jumlahTransaksi()
            input("Tekan ENTER untuk melanjutkan...")
        elif pilihan== '0':
            break
        else :
            print("tolong masukkan input dengan benar!")

            

def total():

    print("=== TOTAL ===\n")

    # 1. Total 
    mycursor.execute("SELECT COUNT(*) FROM petani")
    total_petani = mycursor.fetchone()[0]

    mycursor.execute("SELECT COUNT(*) FROM konsumen")
    total_konsumen = mycursor.fetchone()[0]

    mycursor.execute("SELECT COUNT(*) FROM produk_tani")
    total_produk = mycursor.fetchone()[0]

    mycursor.execute("SELECT COUNT(*) FROM transaksi")
    total_transaksi = mycursor.fetchone()[0]

    print(f"Total Petani        : {total_petani}")
    print(f"Total Konsumen      : {total_konsumen}")
    print(f"Total Produk        : {total_produk}")
    print(f"Total Transaksi     : {total_transaksi}")

def totalStokBarang():
    mycursor.execute("SELECT COALESCE(SUM(stok_produk), 0) FROM produk_tani")
    total_stok = mycursor.fetchone()[0]
    print("=== TOTAL STOK BARANG ===\n")
    print(f"Total Stok Barang   : {total_stok}")

def jumlahTransaksi():
    mycursor.execute("SELECT COUNT(*) FROM transaksi WHERE id_status_transaksi = 1")
    transaksi_berhasil = mycursor.fetchone()[0]
    mycursor.execute("SELECT COUNT(*) FROM transaksi WHERE id_status_transaksi = 3")
    transaksi_gagal = mycursor.fetchone()[0]
    print("=== TOTAL TRANSAKSI GAGAL/BERHASIL ===\n")
    print(f"Transaksi Berhasil  : {transaksi_berhasil}")
    print(f"Transaksi Gagal     : {transaksi_gagal}")



def ManajemenPengguna():
    global pkUser_recent
    while True:
        header = pf.figlet_format("PASTANI", font="slant")
        print(header)
        print("HALAMAN UTAMA MANAJEMEN PENGGUNA")
        print(f"Kamu login sebagai: {user_recent}")
        print(f"ID Anda: {pkUser_recent}")
        print("\nMENU : ")
        print("[1] Melihat Daftar Semua Pengguna")
        print("[2] Verifikasi Akun Pengguna")
        print("[0] Kembali")
        pilihan = input()
        if pilihan == '1':
            DaftarSemuaPengguna()
            input("Tekan ENTER untuk melanjutkan...")
        elif pilihan == '2':
            VerifikasiAkunPetani()
            input("Tekan ENTER untuk melanjutkan...")
        elif pilihan== '0':
            break
        else :
            print("tolong masukkan input dengan benar!")

def VerifikasiAkunPetani():
    while True:
        print("\n=== VERIFIKASI AKUN PETANI ===")
        mycursor.execute("""
                        select id_petani, username, nama_petani, nomor_telepon, email, status_petani
                        FROM petani WHERE status_petani = FALSE
                        """)
        hasil = mycursor.fetchall()
        print(tabulate(hasil, headers=("id petani", "username", "nama petani","nomor telepon", "email","status")))
        while True:
            try:
                while True:
                    idp = ''
                    print("\nMasukkan ID Petani untuk diverifikasi: ")
                    idp = int(kekosongan(idp, 'id petani'))
                    mycursor.execute(f"""
                                    SELECT EXISTS (SELECT 1 FROM petani
                                    WHERE id_petani = {idp} AND status_petani = FALSE)
                                    """)
                    cek = mycursor.fetchone()[0]
                    if not cek:
                        print("ID tidak ditemukan atau sudah diverifikasi.")
                    elif cek:
                        print("ID ditemukan!")
                        break
                break
            except ValueError:
                print("Input tidak valid!")
                input("Tekan ENTER untuk melanjutkan...")
        break
    while True:
        print("===== PILIHAN =====\n")
        print("[1] Aktifkan akun petani")
        print("[2] Hapus akun petani")
        print("[0] Kembali")
        aksi = input("Masukkan pilihan: ")
        if aksi == "1":
            mycursor.execute(f"""
                            UPDATE petani
                            SET status_petani = TRUE
                            WHERE id_petani = {idp}
                            """)
            mycursor.execute(f"UPDATE petani SET id_admin = {pkUser_recent} where id_petani = {idp}")
            conn.commit()
            print("Akun petani berhasil disetujui dan diaktifkan!")
            break
        elif aksi == "2":
            mycursor.execute(f"""
                DELETE FROM petani
                WHERE id_petani = {idp}
            """)
            conn.commit()
            print("Akun petani berhasil ditolak dan dihapus.")
            break
        elif aksi == '0':
            input("Tekan ENTER untuk kembali...")
            break
        else:
            print("Pilihan tidak valid!")


def DaftarSemuaPengguna():
    while True:
        print("=== DAFTAR SEMUA PENGGUNA===\n")
        print("1. Petani")
        print("2. Konsumen")
        print("0. Kembali")
        pilihan = input("Pilih filter (1/2/3): ")
        if pilihan == '1':
            mycursor.execute("""
                            select p.nama_petani, p.username, 
                            case when p.status_petani = true then 'aktif'
                            else 'tidak aktif' end as status_produk,
                            p.nomor_telepon,p.email, a.nama_jalan,d.nama_desa
							, k.nama_kecamatan
                            from Petani p join alamat a
                            using(id_alamat) join desa d 
							using (id_desa) join kecamatan k
							using (id_kecamatan)
                            """)
            tabel = mycursor.fetchall()
            print(tabulate(tabel, headers= ('nama petani', 'username','status akun','nomor telepon', 'email', 'nama jalan', 'nama desa', 'nama kecamatan' ), tablefmt="pretty"))
        elif pilihan == '2' :
            mycursor.execute("""
                        select k. username, k. nama_konsumen, k. nomor_telepon, k. email, 
						a. nama_jalan,d.nama_desa, kc.nama_kecamatan 
						from konsumen k join alamat a
                        using (id_alamat) join desa d 
						using (id_desa) join kecamatan kc
						using (id_kecamatan)
                        """)
            tabel = mycursor.fetchall()
            print(tabulate(tabel, headers= ('nama konsumen', 'username', 'nomor telepon', 'email', 'nama jalan', 'nama desa', 'nama kecamatan'), tablefmt="pretty"))
        elif pilihan == '0':
            print("Kembali")
            break
        else:
            print("Tolong masukkan input dengan benar!")
        
def halamanUtamaAdmin():
    if pkUser_recent == None:
        return
    while True:
        print("\n=== HALAMAN UTAMA ADMIN ===\n")
        print(f"Kamu login sebagai: {user_recent}")
        print(f"ID Anda: {pkUser_recent}")
        pilihan = q.select("MENU: ", choices=[
            "1. Dashboard Global",
            "2. Manajamen Pengguna",
            "3. Manajemen Produk",
            "4. Pemantauan Transaksi",
            "5. Kelola Distribusi",
            "0. Keluar"
        ]).ask()
        if pilihan == '1. Dashboard Global':
            dashboardglobal()
        elif pilihan == '2. Manajamen Pengguna':
            ManajemenPengguna()
        elif pilihan == '3. Manajemen Produk':
            ManajemenProduk()
            print()#Manajemen produk
        elif pilihan == '4. Pemantauan Transaksi':
            PemantauanTransaksi()
            print()#Pemantauan Transaksi
        elif pilihan == '5. Kelola Distribusi':
            distribusiAdmin()
        elif pilihan == '0. Keluar':
            input("Tekan ENTER untuk melanjutkan...")
            break
        else :
            print("Tolong masukkan input dengan benar!")

def PemantauanTransaksi():
    mycursor.execute("""select t.id_transaksi, t.tanggal_transaksi, k.nama_konsumen,
                    (dt.Quantity* pt.harga_produk),pt.nama_produk,pt.harga_produk, dt.quantity,
                    p.nama_petani, st.status_transaksi
                    from transaksi t join konsumen k
                    using(id_konsumen)
                    join detail_transaksi dt 
                    using(id_transaksi)
                    join produk_tani pt
                    using (id_produk)
                    join petani p
                    using(id_petani)
                    join status_transaksi st
                    using(id_status_transaksi)
                    order by t.tanggal_transaksi DESC
                    """)
    tabel= mycursor.fetchall()

    print(tabulate(tabel, headers= ("ID Transaksi","Tanggal Transaksi", "Nama Konsumen", "Total_Transaksi", "Nama Produk" ,"Harga Produk","Quantity","Nama Petani", "Status Transaksi"
    ), tablefmt="pretty"))
    input("Tekan ENTER untuk melanjutkan..")

def ManajemenProduk():
    mycursor.execute("""select p.nama_petani, pt.id_produk,pt. nama_produk, pt. harga_produk
                    , pt.stok_produk, jp.jenis_produk, pt.status_produk
                    from petani p join produk_tani pt
                    using(id_petani)
                    join jenis_produk jp
                    using(id_jenis_produk)
                    where pt.status_produk = 'True'
                    order by p.nama_petani""")
    tabel= mycursor.fetchall()
    print(tabulate(tabel, headers= ("Nama Petani", "Id Produk", "Nama Produk", "Harga Produk", "Stok Produk", "Jenis Produk" ,
                                    "Status Produk"), tablefmt='pretty'))
    print("\n--- OPSI ADMIN ---")
    print("1. Hapus Produk Bermasalah")
    print("0. Kembali ke Menu Admin")

    opsi_admin= input("pilih aksi?")
    if opsi_admin=='1':
        while True:
            try:
                id_hapus = int(input("\nMasukkan ID Produk yang ingin dihapus (0 untuk batal): "))
                if id_hapus == 0:
                    print("Batal menghapus.")
                    break
                id_hapus = int(id_hapus)
                cek=(f"""SELECT p.nama_petani, pt. nama_produk 
                        FROM petani p join produk_tani pt
                        using(id_petani)
                        WHERE pt.id_produk = {id_hapus}""")
                mycursor.execute(cek)
                data_target = mycursor.fetchone()
                if not data_target:
                    print(" ID Produk tidak ditemukan! Silakan cek kembali tabel di atas!")
                    continue
                id_petani_target = data_target[0]
                nama_produk_target = data_target[1]
                print(f"Produk terpilih: {nama_produk_target}")
                yakin = input(f"Apakah Anda yakin ingin MENGHAPUS PERMANEN produk '{nama_produk_target}'? (y/n): ").lower()
                if yakin == 'y':
                    hapus_sql = f"DELETE FROM produk_tani WHERE id_produk = {id_hapus}"
                    mycursor.execute(hapus_sql)
                    print("Produk berhasil dihapus!")
                    break
                else:
                    print("Penghapusan dibatalkan.")
                    break
            except ValueError:
                print("⚠️ Input ID harus berupa angka!")
            finally :
                input("Tekan ENTER untuk melanjutkan...")
    

#ada perubahan 26/11/2025
def halamanUtamaCustomer():
    global pkUser_recent
    if pkUser_recent == None:
        return
    PK_Keranjang()
    while True:
        header = pf.figlet_format("PASTANI", font="slant")
        print(header)
        print("----------------HALAMAN UTAMA CUSTOMER----------------")
        print(f"Kamu login sebagai: {user_recent}")
        print(f"ID Anda: {pkUser_recent}")
        print(f"ID keranjang Anda: {pkKeranjang_recent}")
        pilihan = q.select("MENU: ", choices=[
            "Lihat daftar dan detail produk",
            "Cari Produk",
            "Checkout & pembayaran",
            "Lihat riwayat pemesanan",
            "Konfirmasi pesanan",
            "Laporan pembelian",
            "Edit Profile",
            "Log out"
        ]).ask()
        if pilihan == 'Lihat daftar dan detail produk':
            while True:
                mycursor.execute("""
                                select pt.id_produk, pt.nama_produk, 'Rp. ' || pt.harga_produk, 
                                pt.stok_produk, p.id_petani, p.nama_petani, jp.jenis_produk
                                from produk_tani pt
                                join petani p using (id_petani)
                                join jenis_produk jp using (id_jenis_produk)
                                where pt.status_produk = true order by pt.id_petani
                                """)
                tabel = mycursor.fetchall()
                print(tabulate(tabel, headers= ("ID produk","nama produk", "harga", "stok","id petani", "nama petani" ,"jenis produk"), tablefmt="pretty"))
                yatidak = input("ingin lanjut ke keranjang? (y/n)")
                if yatidak == 'y':
                    keranjang()
                    input("Tekan ENTER untuk melanjutkan..")
                    break
                elif yatidak == 'n':
                    break
                else :
                    input("Tolong masukkan input dengan benar!")


        #ada perubahan 26/11/2025
        elif pilihan == 'Edit Profile':
            edit_profile('konsumen')
        elif pilihan == 'Cari Produk':
            cariProduk()
        # Tiwi
        elif pilihan =='Lihat riwayat pemesanan':
            lihatRiwayatPemesanan()
        elif pilihan == 'Checkout & pembayaran':
            while True:
                tabelKeranjang()
                pilihEdit = q.select("\n", choices=[
                    "Edit stok keranjang",
                    "Checkout",
                    "Kembali"
                ]).ask()
                if pilihEdit == "Edit stok keranjang":
                    updateStokKeranjang()
                    break
                elif pilihEdit == "Checkout":
                    chekoutTEST()
                    break
                elif pilihEdit == "Kembali":
                    break
        elif pilihan =="Laporan pembelian":
            laporan_pembelian()
        elif pilihan == "Konfirmasi pesanan":
            KonfirmasiPesanan()
        elif pilihan == "Log out":
            break

def updateStokKeranjang():
    global pkKeranjang_recent
    
    while True:
        print("\n=== Ubah Jumlah Produk Dalam Keranjang ===\n")
        mycursor.execute(f"""
            SELECT dk.id_detail_keranjang, pt.nama_produk,
                   dk.jumlah_produk, pt.stok_produk, pt.id_produk
            FROM detail_keranjang dk
            JOIN produk_tani pt USING(id_produk)
            WHERE dk.id_keranjang = {pkKeranjang_recent} order by dk.id_detail_keranjang
        """)
        tabel = mycursor.fetchall()
        print(tabulate(tabel, headers=("ID Keranjang", "Produk", "Jumlah di Keranjang", "Stok Tersedia", "ID Produk"), tablefmt="pretty"))

        while True:
            try:
                idDetail = input("Masukkan ID Keranjang yang ingin diubah (0 untuk batal): ")
                if idDetail == '0':
                    return 
            except ValueError:
                print("Tolong masukkan ID berupa angka!")

            mycursor.execute(f"""
                select exists (SELECT 1
                FROM detail_keranjang dk
                JOIN produk_tani pt USING(id_produk)
                WHERE id_detail_keranjang = {idDetail} and id_keranjang = {pkKeranjang_recent})
            """)
            cek = mycursor.fetchone()[0]
            if cek == False:
                print("ID detail tidak ditemukan!")
                continue
            if cek == True:
                break

        mycursor.execute(f"""
            SELECT dk.jumlah_produk, pt.stok_produk, pt.id_produk
            FROM detail_keranjang dk
            JOIN produk_tani pt USING(id_produk)
            WHERE id_detail_keranjang = {idDetail} and id_keranjang = {pkKeranjang_recent}
        """)
        row = mycursor.fetchone()
        
        jumlahSekarang, stokTersedia, idProduk = row
        print(f"Jumlah saat ini : {jumlahSekarang}")
        print(f"Stok tersedia   : {stokTersedia}")

        print("\n[1] Tambah jumlah\n[2] Kurangi jumlah\n[0] Batal")
        pilih = input("Pilihan: ")

        if pilih == '1': #KURANG ERROR HANDLING----------------------------------------------------------------------------------------
            tambah = int(input("Tambah berapa? "))
            if jumlahSekarang + tambah > stokTersedia:
                print("Tidak dapat menambah karena melebihi stok!")
            else:
                mycursor.execute(f"""
                    UPDATE detail_keranjang
                    SET jumlah_produk = jumlah_produk + {tambah}
                    WHERE id_detail_keranjang = {idDetail};

                    UPDATE produk_tani
                    SET stok_produk = stok_produk - {tambah}
                    where id_produk = {idProduk}
                """)

                conn.commit()
                print("Jumlah berhasil ditambahkan!")

        elif pilih == '2':
            kurang = int(input("Kurangi berapa? "))
            if jumlahSekarang - kurang <= 0:
                mycursor.execute(f"""
                    DELETE FROM detail_keranjang
                    WHERE id_detail_keranjang = {idDetail}
                """)
                conn.commit()
                print("Produk dihapus dari keranjang karena jumlah menjadi 0!")
            else:
                mycursor.execute(f"""
                    UPDATE detail_keranjang
                    SET jumlah_produk = jumlah_produk - {kurang}
                    WHERE id_detail_keranjang = {idDetail};

                    UPDATE produk_tani
                    SET stok_produk = stok_produk + {kurang}
                    where id_produk = {idProduk}
                """)
                conn.commit()
                print("Jumlah berhasil dikurangi!")

        else:
            break
        
        input("Tekan ENTER untuk lanjut...")


def cariProduk():
    while True:
        mycursor.execute("""
                        select pt.id_produk, pt.nama_produk, pt.harga_produk, 
                        pt.stok_produk, p.id_petani, p.nama_petani, jp.jenis_produk
                        from produk_tani pt
                        join petani p using (id_petani)
                        join jenis_produk jp using (id_jenis_produk)
                        where pt.status_produk = true
                        """)
        tabel = mycursor.fetchall()
        print(tabulate(tabel, headers= ("ID produk","nama produk", "harga", "stok","id petani", "nama petani" ,"jenis produk"), tablefmt="pretty"))
        cariProduk = ''
        print("Masukkan nama produk(angka 0 untuk kembali): ")
        cariProduk = kekosongan(cariProduk,  "Produk yang dicari")
        if cariProduk == '0':
            break
        mycursor.execute(f"""
                        select pt.id_produk, pt.nama_produk, pt.harga_produk, 
                        pt.stok_produk,p.id_petani, p.nama_petani, jp.jenis_produk
                        from produk_tani pt
                        join petani p using (id_petani)
                        join jenis_produk jp using (id_jenis_produk)
                        where pt.nama_produk ilike '%{cariProduk}%' AND pt.status_produk = TRUE
                        """)
        tabel = mycursor.fetchall()
        print(tabulate(tabel, headers= ("ID produk","nama produk", "harga", "stok", "id petani","nama petani" ,"jenis produk"), tablefmt="pretty"))
        yatidak = input("ingin lanjut ke keranjang? (y/n)")
        if yatidak == 'y':
            keranjang()
            input("Tekan ENTER untuk melanjutkan..")
            break
        elif yatidak == 'n':
            break
        else :
            input("Tolong masukkan input dengan benar!")
        input("Tekan ENTER untuk melanjutkan...")

def lihatRiwayatPemesanan():
    while True:
        mycursor.execute(f"select exists(select 1 from transaksi where id_konsumen = {pkUser_recent})")
        riwayat = mycursor.fetchone()[0]
        if riwayat == False:
            print("Belum ada pesanan yang dibuat.")
            input("Tekan ENTER untuk kembali...")
        elif riwayat == True:
            mycursor.execute(f"""
                    select t.id_transaksi, t.tanggal_transaksi, pt.nama_produk, dt.quantity,
                    'Rp. ' || pt.harga_produk ,'Rp. ' || (dt.Quantity* pt.harga_produk) total_transaksi,p. nama_petani,
                    st.status_transaksi, t.tanggal_kirim, t.tanggal_terima, sp.status_pengiriman
                    from transaksi t join detail_transaksi dt
                    using(id_transaksi) join produk_tani pt
                    using(id_produk) join petani p
                    using (id_petani) join status_transaksi st
                    using (id_status_transaksi) left join status_pengiriman sp
                    using (id_status_pengiriman)
                    where id_konsumen = {pkUser_recent} and (t.id_status_pengirman = 4 or t.id_status_pengiriman = 3)
                    order by id_transaksi asc
                    """)
            tabel = mycursor.fetchall()
            print(tabulate (tabel, headers= ["Id Transaksi", "Tanggal Transaksi", "Nama Produk", "Quantity", "Harga", "Total Transaksi","Nama Petani" ,"Status Transaksi", "Tanggal Kirim", "Tangga Terima", "Status Pengiriman"], tablefmt="pretty"))
            
            detail = q.select("MENU: ", choices=[
                "1. Lihat total transaksi",
                "2. Keluar"
            ]).ask()
            
            if detail == "1. Lihat total transaksi":
                mycursor.execute(f"""
                                select t.id_transaksi, t.tanggal_transaksi, 'Rp. ' ||
                                SUM(dt.Quantity* pt.harga_produk + 15000) total_transaksi,
                                st.status_transaksi, sp.status_pengiriman
                                from transaksi t join detail_transaksi dt
                                using(id_transaksi) join produk_tani pt
                                using(id_produk) join petani p
                                using (id_petani) join status_transaksi st
                                using (id_status_transaksi) left join status_pengiriman sp
                                using (id_status_pengiriman)
                                where id_konsumen = {pkUser_recent}
                                group by t.id_transaksi, t.tanggal_transaksi, st.status_transaksi, sp.status_pengiriman
                                order by id_transaksi asc
                                """)
                tabeltotal = mycursor.fetchall()
                print(tabulate(tabeltotal, headers=("ID Transaksi","Tanggal Transaksi","Total Transaksi + ongkir", "Status Transaksi","Status Pengiriman"), tablefmt="pretty"))
                input("Tekan ENTER untuk melanjutkan...")
            elif detail == "2. Keluar":
                break


def PK_Keranjang():
    global pkKeranjang_recent
    mycursor.execute(f"select id_keranjang from keranjang where id_konsumen = {pkUser_recent}")
    pkKeranjang_recent = mycursor.fetchone()[0]

def tabelKeranjang():
        mycursor.execute(f"""select pt.id_petani, p.nama_petani, pt.nama_produk, dk.jumlah_produk, (jumlah_produk * pt.harga_produk)
                            from detail_keranjang dk
                            join keranjang k using(id_keranjang)
                            join produk_tani pt using(id_produk)
                            join petani p using (id_petani)
                            where k.id_konsumen = {pkUser_recent}
                            """)
        tabel = mycursor.fetchall()
        print(tabulate(tabel, headers=("id petani", "nama petani", "nama produk", "jumlah", "total harga"), tablefmt="pretty"))


def keranjang():
    while True:
        print("Mau beli produk dari id petani berapa? ")
        idPetani = None
        idProduk = None
        while True:
            try :
                while True:
                    idPetani = int(kekosongan(idPetani, "id petani"))
                    mycursor.execute(f"SELECT EXISTS (SELECT 1 FROM produk_tani WHERE id_petani = {idPetani})")
                    cekIdPetani = mycursor.fetchone()[0]
                    if cekIdPetani == False:
                        print("Data tidak ada")
                    elif cekIdPetani == True:
                        print("Id petani tersedia")
                        break
                break
            except ValueError:
                print("Input harus berupa angka integer! Coba lagi.\n")
        mycursor.execute(f"""
                        select pt.id_produk, pt.nama_produk, pt.harga_produk, 
                        pt.stok_produk, p.nama_petani, jp.jenis_produk
                        from produk_tani pt
                        join petani p using (id_petani)
                        join jenis_produk jp using (id_jenis_produk)
                        where id_petani = {idPetani} and status_produk = true order by pt.id_produk
                            """)
        tabel = mycursor.fetchall()
        print(tabulate(tabel, headers= ("ID produk","nama produk", "harga", "stok", "nama petani" ,"jenis produk"), tablefmt="pretty"))
        print(f"Produk dengan id petani : {idPetani}")
        while True:
            try :
                while True:
                    idProduk = int(kekosongan(idProduk, "id produk"))
                    mycursor.execute(f"SELECT EXISTS (SELECT 1 FROM produk_tani WHERE id_produk = {idProduk})")
                    cekIdProduk = mycursor.fetchone()[0]
                    if cekIdProduk == False:
                        print("Data tidak ada")
                    elif cekIdProduk == True:
                        print("Produk ada")
                        break
                break
            except ValueError:
                print("Input harus berupa angka integer! Coba lagi.\n")
        mycursor.execute(f"SELECT nama_produk, stok_produk, harga_produk FROM produk_tani WHERE id_produk = {idProduk}")
        data_produk = mycursor.fetchone()
        nama_produk = data_produk[0]
        stok_produk = data_produk[1]
        harga_produk = data_produk[2]
        jumlah_beli = None
        while True:
            try:
                print(f"\nStok {nama_produk} tersedia {stok_produk}")
                jumlah_beli=int( input("Masukkan jumlah produk yang ingin anda beli = "))
                if jumlah_beli <= 0:
                    print("Jumlah beli harus lebih dari 0!")
                elif jumlah_beli > stok_produk:
                    print(f"Stok produk tidak mencukupi! Maksimal pembelian adalah {stok_produk}.")
                else:
                    break
            except ValueError:
                print("Input harus berupa angka integer! Coba lagi.\n")
        try:
            # Cek dulu apakah produk ini sudah ada di keranjang user tersebut?
            cek_keranjang_sql = f"""SELECT dk.id_detail_keranjang, dk.jumlah_produk FROM detail_keranjang dk
                                    join keranjang k using (id_keranjang)
                                    WHERE id_konsumen = {pkUser_recent} AND id_produk = {idProduk}
                                    """
            mycursor.execute(cek_keranjang_sql)
            item_ada = mycursor.fetchone()

            #Mengurangi stok di database
            mycursor.execute(f"""
                            UPDATE produk_tani SET stok_produk = stok_produk - {jumlah_beli} WHERE id_produk = {idProduk}     
                            """)
            if item_ada:
                # Jika sudah ada, update jumlahnya (tambah dengan yg baru)
                id_keranjang_lama = item_ada[0]
                jumlah_lama = item_ada[1]
                jumlah_baru = jumlah_lama + jumlah_beli
                

                # Validasi lagi agar total di keranjang tidak melebihi stok
                if jumlah_baru > stok_produk:
                    print(f"Gagal! Anda sudah punya {jumlah_lama} di keranjang. Ditambah {jumlah_beli} melebihi stok.")
                else:
                    update_sql = f"UPDATE detail_keranjang SET jumlah_produk = {jumlah_baru} WHERE id_detail_keranjang = {id_keranjang_lama}"
                    mycursor.execute(update_sql)
                    print(f"Berhasil memperbarui jumlah {nama_produk} di keranjang!")

            else:
                # Jika belum ada, lakukan INSERT baru
                # Sesuaikan nama kolom tabel 'keranjang' dengan database kamu
                insert_sql = f"""
                    INSERT INTO detail_keranjang (id_produk, jumlah_produk, id_keranjang) 
                    VALUES ({idProduk}, {jumlah_beli}, {pkKeranjang_recent})
                """
                mycursor.execute(insert_sql)
                print(f"Berhasil menambahkan {nama_produk} ke keranjang!")

            # PENTING: Simpan perubahan
            conn.commit()
            print("Berikut keranjang anda: ")
            tabelKeranjang()
        except Exception as e:
            print("Terjadi kesalahan saat menyimpan ke keranjang: ", e)

        # Tanya apakah ingin belanja lagi atau selesai
        lanjut = input("\nIngin membeli produk lain? (y/n): ").lower()
        if lanjut != 'y':
            print("Kembali ke menu utama...")
            break
    

def laporan_pembelian():
    tabel = f"""
SELECT t.id_transaksi, t.tanggal_transaksi, pt.nama_produk, (dt.quantity * pt.harga_produk),dt.quantity, st.status_transaksi, sp.status_pengiriman
from detail_transaksi dt
join transaksi t using (id_transaksi)
join produk_tani pt using (id_produk)
join status_transaksi st using (id_status_transaksi)
join status_pengiriman sp using (id_status_pengiriman)
where t.id_konsumen = {pkUser_recent} and t.id_status_pengiriman = 4
"""
    cektabel = f"""
select exists(SELECT 1
from detail_transaksi dt
join transaksi t using (id_transaksi)
join konsumen k using (id_konsumen)
where k.id_konsumen = {pkUser_recent})
"""
    mycursor.execute(cektabel)
    cektabel2=mycursor.fetchone()[0]
    if cektabel2 == True:
        mycursor.execute(tabel) 
        tampilkan =mycursor.fetchall()
        print(tabulate(tampilkan, headers=("ID Transaksi","tanggal transaksi", "nama produk","harga total","jumlah barang","status transaksi", "status pengiriman"), tablefmt="pretty"))
        input("Tekan ENTER untuk melanjutkan")
    elif cektabel2 == False:
        print("Tidak ada riwayat transaksi")
        input("Tekan ENTER untuk melanjutkan")       
        


def dashboardglobal():
    global pkUser_recent
    while True:
        header = pf.figlet_format("PASTANI", font="slant")
        print(header)
        print("HALAMAN UTAMA ADMIN")
        print(f"Kamu login sebagai: {user_recent}")
        print(f"ID Anda: {pkUser_recent}")
        print("\nMENU : ")
        print("[1] Total (petani, konsumen, produk, transaksi)")
        print("[2] Jumlah stok barang")
        print("[3] jumlah transaksi berhasil/gagal")
        print("[0] Kembali")
        pilihan = input()
        if pilihan == '1':
            total()
            input("Tekan ENTER untuk melanjutkan...")
        elif pilihan == '2':
            totalStokBarang()
            input("Tekan ENTER untuk melanjutkan...")
        elif pilihan == '3':
            jumlahTransaksi()
            input("Tekan ENTER untuk melanjutkan...")
        elif pilihan== '0':
            break
        else :
            print("tolong masukkan input dengan benar!")

            

def total():

    print("=== TOTAL ===\n")

    # 1. Total 
    mycursor.execute("SELECT COUNT(*) FROM petani")
    total_petani = mycursor.fetchone()[0]

    mycursor.execute("SELECT COUNT(*) FROM konsumen")
    total_konsumen = mycursor.fetchone()[0]

    mycursor.execute("SELECT COUNT(*) FROM produk_tani")
    total_produk = mycursor.fetchone()[0]

    mycursor.execute("SELECT COUNT(*) FROM transaksi")
    total_transaksi = mycursor.fetchone()[0]

    print(f"Total Petani        : {total_petani}")
    print(f"Total Konsumen      : {total_konsumen}")
    print(f"Total Produk        : {total_produk}")
    print(f"Total Transaksi     : {total_transaksi}")

def totalStokBarang():
    mycursor.execute("SELECT COALESCE(SUM(stok_produk), 0) FROM produk_tani")
    total_stok = mycursor.fetchone()[0]
    print("=== TOTAL STOK BARANG ===\n")
    print(f"Total Stok Barang   : {total_stok}")

def jumlahTransaksi():
    mycursor.execute("SELECT COUNT(*) FROM transaksi WHERE id_status_transaksi = 1")
    transaksi_berhasil = mycursor.fetchone()[0]
    mycursor.execute("SELECT COUNT(*) FROM transaksi WHERE id_status_transaksi = 3")
    transaksi_gagal = mycursor.fetchone()[0]
    print("=== TOTAL TRANSAKSI GAGAL/BERHASIL ===\n")
    print(f"Transaksi Berhasil  : {transaksi_berhasil}")
    print(f"Transaksi Gagal     : {transaksi_gagal}")
        
def ResetPK():
    mycursor.execute("select setval('desa_id_desa_seq', (SELECT MAX(id_desa) from desa))")  
    mycursor.execute("select setval('kecamatan_id_kecamatan_seq', (SELECT MAX(id_kecamatan) from kecamatan))")
    mycursor.execute("select setval('petani_id_petani_seq', (SELECT MAX(id_petani) from petani))")
    mycursor.execute("select setval('alamat_id_alamat_seq', (SELECT MAX(id_alamat) from alamat))")
    mycursor.execute("select setval('konsumen_id_konsumen_seq', (SELECT MAX(id_konsumen) from konsumen))")
    mycursor.execute("select setval('produk_tani_id_produk_seq', (SELECT MAX(id_produk) from produk_tani))")
    mycursor.execute("select setval('keranjang_id_keranjang_seq', (SELECT MAX(id_keranjang) from keranjang))")
    mycursor.execute("select setval('detail_keranjang_id_detail_keranjang_seq', (SELECT MAX(id_detail_keranjang) from detail_keranjang))")
    mycursor.execute("select setval('detail_transaksi_id_detail_transaksi_seq', (SELECT MAX(id_detail_transaksi) from detail_transaksi))")
    mycursor.execute("select setval('status_pengiriman_id_status_pengiriman_seq', (select MAX(id_status_pengiriman) from status_pengiriman))")

#tambahan dari Marsha 27/11/2025 11:22
def KelolaPesananTani():
    try:
        headernya = pf.figlet_format("PASTANI", font="slant")
        print(Fore.GREEN + headernya)
        print("OPSI : [2] Lihat & Kelola Pesanan\n")

        print("Berikut pesanan yang masuk: ")
        mycursor.execute(f"""
                        select t.id_transaksi, k.nama_konsumen, a.nama_jalan, d.nama_desa, kec.nama_kecamatan, pt.nama_produk, dt.quantity, (dt.quantity * pt.harga_produk) as subtotal,
                        case when t.diantar = true then 'iya'
                        else 'tidak' end as diantar, sp.status_pengiriman
                        from detail_transaksi dt
                        join transaksi t using (id_transaksi)
                        join produk_tani pt using (id_produk)
                        join konsumen k using (id_konsumen)
                        join alamat a using (id_alamat)
                        join desa d using (id_desa)
                        left join status_pengiriman sp using (id_status_pengiriman)
                        join kecamatan kec using (id_kecamatan)
                        where pt.id_petani = {pkUser_recent} AND (t.id_status_pengiriman IS DISTINCT FROM 4)
                        """)
        tabel = mycursor.fetchall()
        print(tabulate(tabel, headers=("ID Transaksi","Nama Konsumen","Alamat","Desa","Kecamatan","Produk","Jumlah","Subtotal", "Diantar", "Pengiriman"), tablefmt="pretty"))
        while True:
            while True:
                try:
                    idTransaksi = None
                    print("Silahkan pilih id transaksi yang akan dikonfirmasi/dibatalkan pemesanan nya (tekan 0 untuk kembali): ")
                    idTransaksi = int(kekosongan(idTransaksi, "ID Transaksi"))
                    mycursor.execute(f"select id_konsumen from transaksi where id_transaksi = {idTransaksi}")
                    idCust = mycursor.fetchone()[0]
                    break
                except ValueError:
                    print("Tolong masukkan input dengan benar!")
            if idTransaksi == 0:
                break
            query =f"""
                    select t.id_transaksi , k.id_konsumen, k.nama_konsumen, a.nama_jalan, d.nama_desa, kec.nama_kecamatan, pt.nama_produk, dt.quantity, (dt.quantity * pt.harga_produk) as subtotal, t.diantar
                    from detail_transaksi dt
                    join transaksi t using (id_transaksi)
                    join produk_tani pt using (id_produk)
                    join konsumen k using (id_konsumen)
                    join alamat a using (id_alamat)
                    join desa d using (id_desa)
                    join kecamatan kec using (id_kecamatan)
                    where k.id_konsumen = {idCust} and pt.id_petani = {pkUser_recent} and t.id_transaksi = {idTransaksi}
                    """
            mycursor.execute(query)
            AdaGAK = mycursor.fetchone()
            if AdaGAK == None:
                print("ID belum pernah melakukan transaksi kepada Anda!")
            elif AdaGAK != None:
                print("ID konsumen tersedia!\n")
                milih = q.select("Pilih Menu:",
                            choices=[
                                "[1] Terima Pesanan",
                                "[2] Tolak Pesanan",
                                "[0] Keluar"
                                    ]).ask()
                if milih == "[1] Terima Pesanan":
                    mycursor.execute(f"""select t.diantar from transaksi t 
                                     join detail_transaksi dt using (id_transaksi)
                                     join produk_tani pt using (id_produk)
                                     where t.id_konsumen = {idCust} and pt.id_petani = {pkUser_recent} and t.id_transaksi = {idTransaksi}""")
                    diantar = mycursor.fetchone()[0]                     #ERROR DI SINI MARRRR 1/12/2025
                    if diantar == True:
                        mycursor.execute(f"""
                                        UPDATE transaksi SET tanggal_kirim = now() where id_transaksi = {idTransaksi};
                                        UPDATE transaksi SET id_status_pengiriman = 1 where id_transaksi = {idTransaksi};
                                        UPDATE transaksi SET id_status_transaksi = 1 where id_transaksi = {idTransaksi};
                                        """)
                        mycursor.execute(query)
                        dataAlamat = mycursor.fetchone()
                        print("Segera antar ke lokasi admin")
                        input("Tekan ENTER untuk melanjutkan...")
                        conn.commit()
                        break
                    elif diantar == False:
                        mycursor.execute(f"""
                                        UPDATE transaksi SET tanggal_kirim = NULL where id_transaksi = {idTransaksi};
                                        UPDATE transaksi SET id_status_pengiriman = 5 where id_transaksi = {idTransaksi};
                                        UPDATE transaksi SET id_status_transaksi = 1 where id_transaksi = {idTransaksi};
                                        """)
                        mycursor.execute(query)
                        print(f"Pesanan diterima! Customer akan segera datang.")
                        input("Tekan ENTER untuk melanjutkan...")
                        conn.commit()
                        break
                elif milih == "[2] Tolak Pesanan":
                    mycursor.execute(f"""
                                    UPDATE transaksi SET id_status_pengiriman = 3 where id_transaksi = {idTransaksi};
                                    UPDATE transaksi SET id_status_transaksi = 3 where id_transaksi = {idTransaksi};
                                    """)
                    input("Pesanan berhasil dibatalkan. Tekan ENTER untuk melanjutkan...\n")
                    print() #belum
                    break
                elif milih == "[0] Keluar":
                    break
        conn.commit()
    except Exception as e:
        print("Kelola pesanan tani: ", e)

def edit_profile(role):
    while True:
        print(Fore.CYAN +80*"=")
        print(Fore.GREEN+pf.figlet_format("EDIT PROFILE", font="slant"))
        print(Fore.CYAN +80*"=")
        mycursor.execute(f"""
                        select {role}.id_{role}, {role}.nama_{role}, {role}.username, {role}.password_{role}, {role}.email, {role}.nomor_telepon, a.nama_jalan, {role}.id_alamat from {role}
                        join alamat a using (id_alamat) where id_{role} = {pkUser_recent}
                        """)
        data = mycursor.fetchone()
        nama = data[1]
        usernameRole = data[2]
        passwordRole = data[3]
        emailRole = data[4]
        nomorTelp = data[5]
        alamats = data[6]
        idAlamat = data[7]
        pilihan =  q.select("MENU EDIT PROFILE:",
                                choices=[
                                    f"Nama: {nama}",
                                    f"Username: {usernameRole}",
                                    f"Password: {passwordRole}",
                                    f"Email: {emailRole}",
                                    f"Nomor Telepon: {nomorTelp}",
                                    f"Alamat: {alamats}",
                                    "Kembali"
                                        ]).ask()
        
        if pilihan == f"Nama: {nama}":
            while True:
                namabaru = ''
                print("Masukkan perubahan nama(ketik 0 untuk batal): ")
                namabaru = kekosongan(namabaru, "nama")
                if namabaru == '0':
                    break
                mycursor.execute(f"UPDATE {role} SET nama_{role} = '{namabaru}' where id_{role} = {pkUser_recent}")
                conn.commit()
                break
        elif pilihan == f"Username: {usernameRole}":
            while True:
                try:
                    usernamebaru = ''
                    print("Masukkan perubahan username(ketik 0 untuk batal): ")
                    usernamebaru = kekosongan(usernamebaru, "username")
                    if usernamebaru == '0':
                        break
                    mycursor.execute(f"UPDATE {role} SET username = '{usernamebaru}' where id_{role} = {pkUser_recent}")
                    conn.commit()
                    break
                except Exception as e:
                    input("Terjadi kesalahan atau username telah digunakan. Coba lagi...")
        elif pilihan == f"Password: {passwordRole}":
            while True:
                passwordbaru = ''
                print("Masukkan perubahan password(ketik 0 untuk batal): ")
                passwordbaru = kekosongan(passwordbaru, "password")
                if passwordbaru == '0':
                    break
                mycursor.execute(f"UPDATE {role} SET password_{role} = '{passwordbaru}' where id_{role} = {pkUser_recent}")
                conn.commit()
                break
        elif pilihan == f"Email: {emailRole}":
            while True:
                try:
                    emailbaru = ''
                    print("Masukkan perubahan email(ketik 0 untuk batal): ")
                    emailbaru = kekosongan(emailbaru, "email")
                    if emailbaru == '0':
                        break
                    mycursor.execute(f"UPDATE {role} SET email = '{emailbaru}' where id_{role} = {pkUser_recent}")
                    conn.commit()
                    break
                except Exception as e:
                    input("Terjadi kesalahan atau email telah digunakan. Coba lagi...")
        elif pilihan == f"Nomor Telepon: {nomorTelp}":
            while True:
                try:
                    nomorbaru = ''
                    print("Masukkan perubahan nomor telepon(ketik 0 untuk batal): ")
                    nomorbaru = kekosongan(nomorbaru, "nomor telepon")
                    if nomorbaru == '0':
                        break
                    mycursor.execute(f"UPDATE {role} SET nomor_telepon = '{nomorbaru}' where id_{role} = {pkUser_recent}")
                    conn.commit()
                    break
                except Exception as e:
                    input("Terjadi kesalahan atau nomor telepon telah digunakan. Coba lagi...")
        elif pilihan == f"Alamat: {alamats}":
            while True:
                try:
                    alamatbaru = ''
                    print("Masukkan perubahan alamat(ketik 0 untuk batal): ")
                    alamatbaru = kekosongan(alamatbaru, "alamat")
                    mycursor.execute(f"select exists(select 1 from alamat where nama_jalan = '{alamatbaru}')")
                    cekalamatnya = mycursor.fetchone()[0]
                    if cekalamatnya == True:
                        print("Maaf alamat telah digunakan")
                    elif cekalamatnya == False:
                        if alamatbaru == '0':
                            break
                        mycursor.execute(f"UPDATE alamat SET nama_jalan = '{alamatbaru}' where id_alamat = {idAlamat}")
                        conn.commit()
                        break
                except Exception as e:
                    input("Terjadi kesalahan. Coba lagi...")
        elif pilihan == "Kembali":
            break

def KonfirmasiPesanan(): 
    while True:
        print("\n=== KONFIRMASI PESANAN DITERIMA ===")
        mycursor.execute(f"""
                         select exists(select 1 from transaksi t
                         where t.id_konsumen = {pkUser_recent}
                         and (t.id_status_pengiriman = 6 or t.id_status_pengiriman = 5))
                        """)
        ada = mycursor.fetchone()[0]
        if ada == False:
            print("Tidak ada pesanan yang dikirim.")
            input("Tekan ENTER untuk kembali...")
            break
        elif ada == True:
            mycursor.execute(f"""
            SELECT 
                t.id_transaksi,
                t.tanggal_transaksi,
                pt.nama_produk,
                dt.quantity,
                pt.harga_produk,
                (dt.quantity * pt.harga_produk) AS total_transaksi,
                p.nama_petani,
                st.status_transaksi,
                t.tanggal_kirim,
                t.tanggal_terima,
                sp.status_pengiriman
            FROM transaksi t
            JOIN detail_transaksi dt USING(id_transaksi)
            JOIN produk_tani pt USING(id_produk)
            JOIN petani p USING(id_petani)
            JOIN status_transaksi st USING(id_status_transaksi)
            LEFT JOIN status_pengiriman sp USING(id_status_pengiriman)
            WHERE t.id_konsumen = {pkUser_recent}
            AND (t.id_status_pengiriman = 6 or t.id_status_pengiriman = 5)
            ORDER BY t.tanggal_transaksi DESC
            """)
            tabel = mycursor.fetchall()
            print(tabulate(tabel, headers=("id transaksi", "tanggal_transaksi","nama produk","jumlah","harga","total transaksi","nama petani","status transaksi","tanggal kirim","tanggal terima","status pengiriman"), tablefmt="pretty"))
            idtrans = ''
            print("Masukkan ID transaksi yang akan dikonfirmasi(ketik 0 untuk kembali)")
            idtrans = kekosongan(idtrans, "ID Transaksi")
            if idtrans == '0':
                break
            mycursor.execute(f"select id_transaksi from transaksi where id_konsumen = {pkUser_recent} and id_transaksi = {idtrans} and (id_status_pengiriman = 6 or id_status_pengiriman = 5)")
            cektransaksi = mycursor.fetchone()
            if cektransaksi == None:
                input("tidak ada pesanan yang valid untuk dikonfirmasi.\nTekan ENTER untuk melanjutkan")
            elif cektransaksi != None:
                mycursor.execute("select id_status_pengiriman from transaksi")
                status_pengiriman = mycursor.fetchone()[0]
                mycursor.execute(f"""
                                UPDATE transaksi SET id_status_pengiriman = 4 where id_transaksi = {idtrans};
                                UPDATE transaksi SET tanggal_terima = now() where id_transaksi = {idtrans}
                                """)
                #LANJOT INI MARRRRR
                input("Pesanan telah dikonfirmasi! pesanan selesai.")
                conn.commit()
                break
    conn.commit()

def distribusiAdmin():
    while True:
        print("===== DISTRIBUSI ADMIN =====\n")
        mycursor.execute("""
                        
                        select t.id_transaksi, k.nama_konsumen, ak.nama_jalan, dk.nama_desa, kk.nama_kecamatan, 
                        p.nama_petani, ap.nama_jalan, dp.nama_desa, kp.nama_kecamatan, sp.status_pengiriman
                        from detail_transaksi dt
                        join transaksi t using (id_transaksi)
                        join produk_tani pt using (id_produk)
                        join konsumen k using (id_konsumen)
                        join petani p using (id_petani)
                        join alamat ak on k.id_alamat = ak.id_alamat
                        join alamat ap on p.id_alamat = ap.id_alamat
                        join desa dk on ak.id_desa = dk.id_desa
                        join desa dp on ap.id_desa = dp.id_desa
                        join kecamatan kk on dk.id_kecamatan = kk.id_kecamatan
                        join kecamatan kp on dp.id_kecamatan = kp.id_kecamatan
                        left join status_pengiriman sp using (id_status_pengiriman)
                        where t.diantar = TRUE and (t.id_status_pengiriman = 1 or t.id_status_pengiriman = 7 or t.id_status_pengiriman = 6)

                        """)
        tabeldistribusi = mycursor.fetchall()
        print(tabulate(tabeldistribusi, headers=("ID Transaksi", "Nama Konsumen","Jalan",
                                                 "Desa","Kecamatan","Nama Petani","Jalan","Desa","Kecamatan",
                                                 "Status Pengiriman"), tablefmt="pretty"))

        pilihan = q.select("MENU: ", choices=[
            "1. Menerima pesanan",
            "2. Mengirim pesanan",
            "0. Keluar"
        ]).ask()

        if pilihan == "1. Menerima pesanan":
            mycursor.execute("""
                            
                            select t.id_transaksi, p.nama_petani, k.nama_konsumen, ak.nama_jalan, dk.nama_desa, kk.nama_kecamatan, 
                            p.nama_petani, ap.nama_jalan, dp.nama_desa, kp.nama_kecamatan, sp.status_pengiriman
                            from detail_transaksi dt
                            join transaksi t using (id_transaksi)
                            join produk_tani pt using (id_produk)
                            join konsumen k using (id_konsumen)
                            join petani p using (id_petani)
                            join alamat ak on k.id_alamat = ak.id_alamat
                            join alamat ap on p.id_alamat = ap.id_alamat
                            join desa dk on ak.id_desa = dk.id_desa
                            join desa dp on ap.id_desa = dp.id_desa
                            join kecamatan kk on dk.id_kecamatan = kk.id_kecamatan
                            join kecamatan kp on dp.id_kecamatan = kp.id_kecamatan
                            left join status_pengiriman sp using (id_status_pengiriman)
                            where t.diantar = TRUE and t.id_status_pengiriman = 1

                            """)
            tabeldistribusi = mycursor.fetchall()
            print(tabulate(tabeldistribusi, headers=("ID Transaksi", "Nama Petani" ,"Nama Konsumen","Jalan","Desa","Kecamatan",
                                                     "Nama Petani","Jalan","Desa","Kecamatan","Status Pengiriman"), tablefmt="pretty"))
            
            print("ID Transaksi berapa yang akan diterima? (0 untuk kembali) ")
            ID_transaksi = ''
            ID_transaksi = kekosongan(ID_transaksi, "ID Transaksi")
            if ID_transaksi == '0':
                return
            mycursor.execute(f"""select t.id_transaksi 
                             from transaksi t
                             where t.id_transaksi = {ID_transaksi} and t.id_status_pengiriman = 1
                             """)
            cektabel = mycursor.fetchone()
            if cektabel == None:
                print("tidak ada pesanan yang masuk!")
                input("Tekan ENTER untuk melanjutkan...")
            elif cektabel != None:
                mycursor.execute(f"UPDATE transaksi SET id_status_pengiriman = 7 where id_transaksi = {ID_transaksi}")
                conn.commit()
                print("Data berhasil diupdate!")
                input("Tekan ENTER untuk melanjutkan...")
                break
        elif pilihan == "2. Mengirim pesanan":
            mycursor.execute("""
                            
                            select t.id_transaksi, p.nama_petani, k.nama_konsumen, ak.nama_jalan, dk.nama_desa, kk.nama_kecamatan, 
                            p.nama_petani, ap.nama_jalan, dp.nama_desa, kp.nama_kecamatan, sp.status_pengiriman
                            from detail_transaksi dt
                            join transaksi t using (id_transaksi)
                            join produk_tani pt using (id_produk)
                            join konsumen k using (id_konsumen)
                            join petani p using (id_petani)
                            join alamat ak on k.id_alamat = ak.id_alamat
                            join alamat ap on p.id_alamat = ap.id_alamat
                            join desa dk on ak.id_desa = dk.id_desa
                            join desa dp on ap.id_desa = dp.id_desa
                            join kecamatan kk on dk.id_kecamatan = kk.id_kecamatan
                            join kecamatan kp on dp.id_kecamatan = kp.id_kecamatan
                            left join status_pengiriman sp using (id_status_pengiriman)
                            where t.diantar = TRUE and t.id_status_pengiriman = 7

                            """)
            tabeldistribusi = mycursor.fetchall()
            print(tabulate(tabeldistribusi, headers=("ID Transaksi", "Nama Petani" ,"Nama Konsumen","Jalan","Desa",
                                                     "Kecamatan","Nama Petani","Jalan","Desa","Kecamatan","Status Pengiriman"), 
                                                     tablefmt="pretty"))
            
            print("ID Transaksi berapa yang akan diantar? (0 untuk kembali)")
            ID_transaksi = ''
            ID_transaksi = kekosongan(ID_transaksi, "ID Transaksi")
            if ID_transaksi == '0':
                return
            mycursor.execute(f"""select t.id_transaksi 
                             from transaksi t
                             where t.id_transaksi = {ID_transaksi} and t.id_status_pengiriman = 7
                             """)
            cektabel = mycursor.fetchone()
            if cektabel == None:
                print("tidak ada pesanan yang masuk!")
                input("Tekan ENTER untuk melanjutkan...")
            elif cektabel != None:
                mycursor.execute(f"UPDATE transaksi SET id_status_pengiriman = 6 where id_transaksi = {ID_transaksi}")
                print("Data berhasil diupdate! silahkan antar kepada konsumen")
                conn.commit()
                input("Tekan ENTER untuk melanjutkan...")
                break
        elif pilihan == "0. Keluar":
            input("Tekan ENTER untuk melanjutkan..")
            break
                



def chekoutTEST(): 
    try:
        while True:
            print("\n--- PROSES CHECKOUT ---")
            mycursor.execute(f"""select dk.id_detail_keranjang, pt.nama_produk, dk.jumlah_produk, (jumlah_produk * pt.harga_produk) harganya, pt.id_petani ,p.nama_petani,
                                a.nama_jalan || ', ' || d.nama_desa || ', ' || kec.nama_kecamatan
                                from detail_keranjang dk
                                join keranjang k using(id_keranjang)
                                join produk_tani pt using(id_produk)
                                join petani p using (id_petani)
                                join alamat a using (id_alamat)
                                join desa d using (id_desa)
                                join kecamatan kec using(id_kecamatan)
                                where k.id_konsumen = {pkUser_recent}
                                """)
            tabel = mycursor.fetchall()
            print(tabulate(tabel, headers=("ID Keranjang","nama produk", "jumlah", "total harga","ID Petani", "Nama Petani", "Alamat Lengkap"), tablefmt="pretty"))
            pilihan = input("Apakah mau dicheckout? (y/n) ").lower()
            
            if pilihan == 'n':
                input("Anda akan kembali ke menu utama...")
                conn.commit()
                break
            elif pilihan == 'y':
                while True:
                    while True:
                        pilihPetani = ''
                        print("Masukkan ID Petani yang akan dicheckout(0 untuk kembali ke menu): ")
                        pilihPetani = kekosongan(pilihPetani, "ID Petani")
                        if pilihPetani == '0':
                            return
                        mycursor.execute(f"""select dk.id_detail_keranjang, pt.nama_produk, dk.jumlah_produk, (jumlah_produk * pt.harga_produk) harganya, pt.id_petani, p.nama_petani,
                                            a.nama_jalan || ', ' || d.nama_desa || ', ' || kec.nama_kecamatan
                                            from detail_keranjang dk
                                            join keranjang k using(id_keranjang)
                                            join produk_tani pt using(id_produk)
                                            join petani p using (id_petani)
                                            join alamat a using (id_alamat)
                                            join desa d using (id_desa)
                                            join kecamatan kec using(id_kecamatan)
                                            where k.id_konsumen = {pkUser_recent} AND pt.id_petani = {pilihPetani}
                                            """)
                        tabelfilter = mycursor.fetchall()
                        print(tabulate(tabelfilter, headers=("ID Keranjang","nama produk", "jumlah", "total harga","ID Petani", "Nama Petani", "Alamat Lengkap"), tablefmt="pretty"))

                        mycursor.execute(f"""select pt.id_petani
                                            from detail_keranjang dk
                                            join keranjang k using(id_keranjang)
                                            join produk_tani pt using(id_produk)
                                            join petani p using (id_petani)
                                            where k.id_konsumen = {pkUser_recent} AND pt.id_petani = {pilihPetani}
                                            """)
                        cekIdpetani_padaKeranjang = mycursor.fetchone()
                        if cekIdpetani_padaKeranjang == None:
                            input("ID Petani tidak tersedia pada keranjang yang telah difilter!")
                        elif cekIdpetani_padaKeranjang != None:
                            break

                    while True:
                        pilihCekOut = ''
                        print("Masukkan ID Keranjang yang akan di check out(0 untuk kembali ke menu, pisahkan dengan spasi):")
                        pilihCekOut = kekosongan(pilihCekOut, "ID Keranjang").split()
                        listcekOut = []
                        for x in pilihCekOut:
                            listcekOut.append(int(x))


                        listDetail = ""
                        for i in range(len(listcekOut)):
                            listDetail += str(listcekOut[i])
                            if i != len(listcekOut) - 1:
                                listDetail += ","  

                        if pilihCekOut == '0':
                            return

                        mycursor.execute(f"""select dk.id_detail_keranjang
                                            from detail_keranjang dk
                                            join keranjang k using(id_keranjang)
                                            join produk_tani pt using(id_produk)
                                            join petani p using (id_petani)
                                            where k.id_konsumen = {pkUser_recent} AND dk.id_detail_keranjang IN ({listDetail}) AND pt.id_petani = {pilihPetani}
                                            """)
                        cekID_KERANJANG = mycursor.fetchmany(len(listcekOut))
                        if len(cekID_KERANJANG) < len(listcekOut):
                            print("Terdapat data yang tidak ada")
                        else :
                            if cekID_KERANJANG == None:
                                input("tidak ada ID Keranjang pada petani tersebut! coba lagi...")
                            elif cekID_KERANJANG != None:
                                break
                        

                    list_detail = []
                    for x in pilihCekOut:
                        list_detail.append(int(x))             # ubah string menjadi integer
                                        
                    query_detail = ""
                    for i in range(len(list_detail)):
                        query_detail += str(list_detail[i])
                        if i != len(list_detail) - 1:
                            query_detail += ","                   # PELAJARI LAGI MAR

                    mycursor.execute(f"""
                        SELECT SUM(dk.jumlah_produk * pt.harga_produk)
                        FROM detail_keranjang dk
                        JOIN produk_tani pt USING(id_produk)
                        WHERE dk.id_detail_keranjang IN ({query_detail})
                    """)
                    totalHarga = mycursor.fetchone()[0]

                    
                    mycursor.execute(f"""
                    SELECT dk.id_produk, dk.jumlah_produk
                    FROM detail_keranjang dk
                    WHERE dk.id_detail_keranjang IN ({query_detail})
                """)
                    produkDipilih = mycursor.fetchall()

                    print(f"Harga total yang perlu dibayar sebesar(beserta ongkir seharga Rp. 15.000): Rp. {totalHarga + 15000}")

                    mycursor.execute(f"""
                                    insert into 
                                    transaksi(tanggal_transaksi, id_status_transaksi, id_konsumen, id_metode_pembayaran, diantar)
                                    values (now(), 2, {pkUser_recent}, 1, FALSE) returning id_transaksi
                                    """)
                    idTransaksi = mycursor.fetchone()[0]

                    mycursor.execute(f"""
                    SELECT dk.id_produk, dk.jumlah_produk
                    FROM detail_keranjang dk
                    JOIN produk_tani pt USING(id_produk)
                    WHERE pt.id_petani IN ({query_detail})
                """)
                    produkCheckout = mycursor.fetchall()

                    for item in produkDipilih:
                        idproduk = item[0]
                        jumlah_produk = item[1]
                        mycursor.execute(f"""
                            INSERT INTO detail_transaksi (id_transaksi, id_produk, quantity)
                            VALUES ({idTransaksi}, {idproduk}, {jumlah_produk})
                        """)

                    diantar = q.select("MENU pengantaran: ", choices=[
                        "Barang diantar petani ke rumah anda",
                        "Barang dijemput customer"
                    ]).ask()

                    if diantar == 'Barang diantar petani ke rumah anda':
                        mycursor.execute(f"UPDATE transaksi SET diantar = TRUE where id_transaksi = {idTransaksi}")

                    for item in produkCheckout:
                        id_produk = item[0]
                        jumlah = item[1]
                        mycursor.execute(f"""
                            INSERT INTO detail_transaksi (id_transaksi, id_produk, quantity)
                            VALUES ({idTransaksi}, {id_produk}, {jumlah})
                        """)

                    mycursor.execute(f"""
                        DELETE FROM detail_keranjang
                        WHERE id_detail_keranjang IN ({query_detail})
                    """)
                    conn.commit()
                    # tabel1 = mycursor.fetchall()
                    # print(tabulate(tabel1, headers=("id petani","nama petani", "nama produk", "jumlah", "total harga"), tablefmt="pretty"))
                    conn.commit()
                    print("Transaksi telah dibuat!")
                    while True:
                        adalagi = input("Apakah ada lagi? (y/n)").lower()
                        if adalagi == 'y':
                            input("Tekan ENTER untuk lanjuts")
                            mycursor.execute(f"""select dk.id_detail_keranjang, pt.nama_produk, dk.jumlah_produk, (jumlah_produk * pt.harga_produk) harganya, pt.id_petani ,p.nama_petani,
                                                a.nama_jalan || ', ' || d.nama_desa || ', ' || kec.nama_kecamatan
                                                from detail_keranjang dk
                                                join keranjang k using(id_keranjang)
                                                join produk_tani pt using(id_produk)
                                                join petani p using (id_petani)
                                                join alamat a using (id_alamat)
                                                join desa d using (id_desa)
                                                join kecamatan kec using(id_kecamatan)
                                                where k.id_konsumen = {pkUser_recent}
                                                """)
                            tabel = mycursor.fetchall()
                            print(tabulate(tabel, headers=("ID Keranjang","nama produk", "jumlah", "total harga","ID Petani", "Nama Petani", "Alamat Lengkap"), tablefmt="pretty"))
                            break
                        if adalagi == 'n':
                            input("Anda akan kembali ke menu utama...")
                            return
                        else:
                            print("Tolong masukkan input dengan benar!")
                    conn.commit()

    except Exception as e:
        print("Ada yang salah ini Mar: ", e)

def laporanPetani():
    print("====== LAPORAN TRANSAKSI ======")
    mycursor.execute(f"""
                    SELECT t.id_transaksi, t.tanggal_transaksi, pt.nama_produk, (dt.quantity * pt.harga_produk),dt.quantity, st.status_transaksi, sp.status_pengiriman
                    from detail_transaksi dt
                    join transaksi t using (id_transaksi)
                    join produk_tani pt using (id_produk)
                    join status_transaksi st using (id_status_transaksi)
                    join status_pengiriman sp using (id_status_pengiriman)
                    where pt.id_petani = {pkUser_recent}
                     """)
    tampilkan = mycursor.fetchall()
    print(tabulate(tampilkan, headers=("ID Transaksi","tanggal transaksi", "nama produk","harga total","jumlah barang","status transaksi", "status pengiriman"), tablefmt="pretty"))
    input("Tekan ENTER untuk kembali...")

    

ResetPK()
main()