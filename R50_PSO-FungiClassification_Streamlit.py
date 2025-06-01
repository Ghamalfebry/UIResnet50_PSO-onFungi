import streamlit as st
import os
import random

# ---------------------------------------------
# Fungsi Utility untuk Mengambil dan Menampilkan Gushurts
# ---------------------------------------------

def get_mushroom_classes(data_dir="Data"):
    """
    Mengembalikan dictionary dengan kunci nama kelas (nama folder dalam Data/)
    dan nilai list berisi path semua file gambar di dalam folder tersebut.
    """
    classes = {}
    if not os.path.isdir(data_dir):
        return classes

    for class_name in sorted(os.listdir(data_dir)):
        class_path = os.path.join(data_dir, class_name)
        if os.path.isdir(class_path):
            image_files = [
                os.path.join(class_path, f)
                for f in os.listdir(class_path)
                if f.lower().endswith((".png", ".jpg", ".jpeg"))
            ]
            if image_files:
                classes[class_name] = image_files
    return classes


def display_three_random_per_class(class_dict):
    """
    Untuk setiap kelas dalam class_dict, pilih 3 gambar secara acak (jika tersedia)
    dan tampilkan side-by-side dengan Streamlit columns.
    """
    for cls, img_paths in class_dict.items():
        st.markdown(f"**Jenis Jamur: {cls}**")
        # Jika jumlah gambar kurang dari 3, tampilkan semua; jika lebih, random 3
        if len(img_paths) <= 3:
            chosen = img_paths
        else:
            chosen = random.sample(img_paths, 3)

        cols = st.columns(len(chosen))
        for i, img_path in enumerate(chosen):
            with cols[i]:
                st.image(img_path, use_column_width=True)
        st.markdown("---")


# ---------------------------------------------
# Aplikasi Streamlit
# ---------------------------------------------

st.title("𝐀𝐩𝐥𝐢𝐤𝐚𝐬𝐢 𝐏𝐞𝐧𝐠𝐨𝐥𝐚𝐡𝐚𝐧 𝐂𝐢𝐭𝐫𝐚 𝐉𝐚𝐦𝐮𝐫")
st.markdown(
    """
    Selamat datang!  
    Gunakan sidebar untuk menavigasi halaman Data, Pra-Pemrosesan, Flowchart, dan Hasil.
    """
)

# Sidebar: Menu Utama
menu = st.sidebar.selectbox(
    "📂 Menu Utama",
    ["Data", "Pra-Pemrosesan", "Flowchart Algoritma", "Hasil"]
)

# ---------------------------------------------
# Menu: Data
# ---------------------------------------------
if menu == "Data":
    st.header("1. Data")
    submenu_data = st.sidebar.selectbox(
        "Pilih Submenu Data",
        ["Gambar Jamur", "Grafik Jumlah Citra"]
    )

    # Submenu: Gambar Jamur
    if submenu_data == "Gambar Jamur":
        st.subheader("1.1 Gambar Jamur")
        st.markdown(
            """
            Dalam folder `Data/`, terdapat 9 subfolder (kelas jamur).  
            Masing-masing kelas akan menampilkan 3 contoh citra secara acak.
            """
        )
        mushroom_classes = get_mushroom_classes("Data")
        if not mushroom_classes:
            st.warning("Folder `Data/` tidak ditemukan atau kosong.")
        else:
            display_three_random_per_class(mushroom_classes)

    # Submenu: Grafik Jumlah Citra
    elif submenu_data == "Grafik Jumlah Citra":
        st.subheader("1.2 Grafik Jumlah Citra per Kelas")
        st.markdown(
            """
            Berikut grafik jumlah citra per kelas (pre-generated).
            """
        )
        graph_path = os.path.join("Assets", "dataMushroom.jpg")
        if os.path.exists(graph_path):
            st.image(graph_path, caption="Grafik Jumlah Citra per Kelas", use_column_width=True)
        else:
            st.warning("File `Assets/dataMushroom.jpg` tidak ditemukan.")


# ---------------------------------------------
# Menu: Pra-Pemrosesan
# ---------------------------------------------
elif menu == "Pra-Pemrosesan":
    st.header("2. Pra-Pemrosesan")
    submenu_pre = st.sidebar.selectbox(
        "Pilih Submenu Pra-Pemrosesan",
        ["Before/After", "Metode"]
    )

    # Submenu: Before/After
    if submenu_pre == "Before/After":
        st.subheader("2.1 Perbandingan Sebelum dan Sesudah")
        st.markdown(
            """
            Tampilkan perbandingan citra sebelum dan sesudah pra-pemrosesan.  
            Pastikan folder `Data/Sample/Original/` dan `Data/Sample/Processed/` 
            berisi gambar dengan nama yang sama agar bisa dibandingkan.
            """
        )
        original_dir = os.path.join("Data", "Sample", "Original")
        processed_dir = os.path.join("Data", "Sample", "Processed")

        if not os.path.isdir(original_dir) or not os.path.isdir(processed_dir):
            st.warning("Folder `Data/Sample/Original/` atau `Data/Sample/Processed/` tidak ditemukan.")
        else:
            orig_files = sorted(
                [f for f in os.listdir(original_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
            )
            proc_files = sorted(
                [f for f in os.listdir(processed_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
            )
            if not orig_files or not proc_files:
                st.warning("Tidak ada gambar di `Data/Sample/Original/` atau `Data/Sample/Processed/`.")
            else:
                st.subheader("Perbandingan Contoh Gambar")
                for orig_name, proc_name in zip(orig_files, proc_files):
                    orig_path = os.path.join(original_dir, orig_name)
                    proc_path = os.path.join(processed_dir, proc_name)
                    cols = st.columns(2)
                    with cols[0]:
                        st.image(orig_path, caption=f"Original: {orig_name}", use_column_width=True)
                    with cols[1]:
                        st.image(proc_path, caption=f"Processed: {proc_name}", use_column_width=True)

    # Submenu: Metode
    elif submenu_pre == "Metode":
        st.subheader("2.2 Metode Pra-Pemrosesan")
        st.markdown(
            """
            **Augmentasi Citra**  
            Augmentasi citra adalah teknik yang efektif untuk memperkaya dan memperluas dataset tanpa harus mengumpulkan data baru.  
            Dengan meningkatkan variasi data, augmentasi membantu mencegah overfitting dan membuat model lebih andal.  
            (Maulana et al., 2023)

            **Resize**  
            Resize mengubah dimensi gambar agar seragam (misal 32×32 piksel), penting untuk menyamakan input ke model CNN.  
            (Supiyani et al., 2022)

            **Flip**  
            Flip horizontal membalik gambar secara lateral untuk menambah variasi data tanpa mengubah semantik.  
            (Subkhi et al., 2024)

            **Rotation**  
            Rotasi mengubah orientasi gambar pada sudut tertentu agar model lebih tangguh terhadap posisi objek.  
            (Subkhi et al., 2024)

            **Color Jitter**  
            Color jitter mengubah brightness, saturasi, kontras, dan hue untuk mensimulasikan variasi pencahayaan nyata.  
            (Lusen et al., 2024)

            **DataTensor**  
            Gambar diubah menjadi tensor (struktur array multidimensi) untuk diproses oleh CNN di GPU.  
            (Lusen et al., 2024)

            **Normalisasi Data Citra**  
            Normalisasi menskalakan nilai piksel (0–255 → 0–1) untuk mempercepat konvergensi dan mencegah kesalahan numerik.  
            (Hendrik et al., 2024)
            """
        )


# ---------------------------------------------
# Menu: Flowchart Algoritma
# ---------------------------------------------
elif menu == "Flowchart Algoritma":
    st.header("3. Flowchart Algoritma")
    st.markdown(
        """
        Berikut alur proses klasifikasi citra jamur:
        
        1. **Pengumpulan Data**: Ambil citra jamur dari folder `Data/`.  
        2. **Pra-Pemrosesan**: Augmentasi, resize, flip, rotasi, color jitter, konversi ke tensor, normalisasi.  
        3. **Pelatihan Model**: Melatih CNN menggunakan data terproses.  
        4. **Evaluasi Model**: Hitung akurasi, plot confusion matrix, dsb.  
        5. **Prediksi**: Gunakan model untuk mengklasifikasi citra baru.
        """
    )
    flowchart_path = os.path.join("Assets", "model_graph.png")
    if os.path.exists(flowchart_path):
        st.image(flowchart_path, caption="Flowchart Algoritma Klasifikasi", use_column_width=True)
    else:
        st.warning("File `Assets/model_graph.png` tidak ditemukan.")


# ---------------------------------------------
# Menu: Hasil
# ---------------------------------------------
elif menu == "Hasil":
    st.header("4. Hasil")
    submenu_hasil = st.sidebar.selectbox(
        "Pilih Submenu Hasil",
        ["Grafik Loss & Akurasi", "Evaluasi (Confusion Matrix)"]
    )

    # Submenu: Grafik Loss & Akurasi
    if submenu_hasil == "Grafik Loss & Akurasi":
        st.subheader("4.1 Grafik Loss & Akurasi Pelatihan")
        st.markdown(
            """
            Berikut grafik hasil pelatihan model CNN (pre-generated).
            """
        )
        graph_path = os.path.join("Assets", "graphLoss_accuration.jpg")
        if os.path.exists(graph_path):
            st.image(graph_path, caption="Grafik Loss vs Epoch & Akurasi vs Epoch", use_column_width=True)
        else:
            st.warning("File `Assets/graphLoss_accuration.jpg` tidak ditemukan.")

    # Submenu: Evaluasi (Confusion Matrix)
    elif submenu_hasil == "Evaluasi (Confusion Matrix)":
        st.subheader("4.2 Confusion Matrix")
        st.markdown(
            """
            Berikut confusion matrix pada data uji (pre-generated).
            """
        )
        cm_path = os.path.join("Assets", "cfMatrix.jpg")
        if os.path.exists(cm_path):
            st.image(cm_path, caption="Confusion Matrix", use_column_width=True)
        else:
            st.warning("File `Assets/cfMatrix.jpg` tidak ditemukan.")
