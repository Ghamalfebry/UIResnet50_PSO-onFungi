import streamlit as st
import os
import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------------------------
# Fungsi Utility untuk Menghitung dan Menampilkan Gambar
# ---------------------------------------------

def load_mushroom_images(data_dir="data/mushrooms"):
    """
    Mengembalikan dictionary dengan kunci nama kelas (jenis jamur)
    dan nilai list berisi path gambar.
    """
    classes = {}
    for class_name in os.listdir(data_dir):
        class_path = os.path.join(data_dir, class_name)
        if os.path.isdir(class_path):
            image_files = [
                os.path.join(class_path, f)
                for f in os.listdir(class_path)
                if f.lower().endswith((".png", ".jpg", ".jpeg"))
            ]
            classes[class_name] = image_files
    return classes


def plot_class_counts(class_dict):
    """
    Membuat bar chart jumlah citra per kelas jamur.
    """
    counts = {cls: len(imgs) for cls, imgs in class_dict.items()}
    df = pd.DataFrame.from_dict(counts, orient="index", columns=["Jumlah"])
    df = df.sort_values(by="Jumlah", ascending=False)

    fig, ax = plt.subplots()
    df.plot(kind="bar", legend=False, ax=ax)
    ax.set_title("Jumlah Citra per Kelas Jamur")
    ax.set_ylabel("Jumlah Citra")
    ax.set_xlabel("Kelas Jamur")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    return fig


def display_before_after(original_dir="data/sample/original", processed_dir="data/sample/processed"):
    """
    Menampilkan contoh perbandingan sebelum dan sesudah pra-pemrosesan.
    Asumsikan struktur folder memiliki gambar dengan nama yang sama di kedua folder.
    """
    original_files = sorted(
        [f for f in os.listdir(original_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    )
    processed_files = sorted(
        [f for f in os.listdir(processed_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    )

    st.subheader("Perbandingan Gambar: Before vs After")
    for orig_name, proc_name in zip(original_files, processed_files):
        orig_path = os.path.join(original_dir, orig_name)
        proc_path = os.path.join(processed_dir, proc_name)
        cols = st.columns(2)
        with cols[0]:
            st.image(orig_path, caption=f"Original: {orig_name}", use_column_width=True)
        with cols[1]:
            st.image(proc_path, caption=f"Processed: {proc_name}", use_column_width=True)


# ---------------------------------------------
# Streamlit App
# ---------------------------------------------

# Title Page
st.title("𝐀𝐩𝐥𝐢𝐤𝐚𝐬𝐢 𝐏𝐞𝐧𝐠𝐨𝐥𝐚𝐡𝐚𝐧 𝐂𝐢𝐭𝐫𝐚 𝐉𝐚𝐦𝐮𝐫")
st.markdown(
    """
    Selamat datang di aplikasi Streamlit untuk eksplorasi data citra jamur,
    pra-pemrosesan, visualisasi alur algoritma, dan evaluasi hasil klasifikasi.
    Gunakan menu di samping untuk menavigasi fitur-fitur aplikasi.
    """
)

# Sidebar Menu Utama
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
            Terdapat 9 jenis jamur dalam dataset. Pada setiap jenis, ditampilkan hingga 3 contoh citra.
            """
        )
        mushroom_classes = load_mushroom_images("data/mushrooms")  # Ganti path sesuai struktur katalog

        # Tampilkan 3 contoh gambar per kelas (jika tersedia)
        for cls, img_paths in mushroom_classes.items():
            st.markdown(f"**Jenis Jamur: {cls}**")
            thumbnails = img_paths[:3]  # ambil 3 gambar pertama
            cols = st.columns(len(thumbnails))
            for i, img_path in enumerate(thumbnails):
                with cols[i]:
                    st.image(img_path, use_column_width=True)
            st.markdown("---")

    # Submenu: Grafik Jumlah Citra
    elif submenu_data == "Grafik Jumlah Citra":
        st.subheader("1.2 Grafik Jumlah Citra per Kelas")
        st.markdown(
            """
            Bar chart berikut menunjukkan total jumlah citra pada masing-masing kelas jamur.
            """
        )
        mushroom_classes = load_mushroom_images("data/mushrooms")  # Ganti path sesuai struktur katalog
        fig = plot_class_counts(mushroom_classes)
        st.pyplot(fig)

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
            Di bagian ini, diperlihatkan contoh citra sebelum dan sesudah melalui tahapan pra-pemrosesan.
            Pastikan folder `data/sample/original` dan `data/sample/processed` berisi gambar dengan nama yang sama.
            """
        )
        display_before_after(
            original_dir="data/sample/original",
            processed_dir="data/sample/processed"
        )

    # Submenu: Metode
    elif submenu_pre == "Metode":
        st.subheader("2.2 Metode Pra-Pemrosesan")
        st.markdown(
            """
            Berikut adalah penjelasan singkat tentang metode-metode yang digunakan dalam pra-pemrosesan citra:

            **Augmentasi Citra**  
            Augmentasi citra adalah teknik yang efektif untuk memperkaya dan memperluas dataset tanpa harus mengumpulkan data baru.  
            Dengan meningkatkan variasi data, augmentasi membantu mencegah overfitting dan membuat model lebih andal serta mampu mengenali pola pada data yang belum pernah dilihat sebelumnya.  
            Teknik ini sangat berguna dalam pelatihan model klasifikasi citra agar lebih general dan akurat (Maulana et al., 2023).

            **Resize**  
            Resize adalah proses mengubah dimensi gambar agar seragam. Misalnya, citra berukuran acak dapat diubah menjadi ukuran tetap seperti 32×32 piksel.  
            Langkah ini penting untuk menyamakan input ke dalam model CNN dan mengurangi kompleksitas komputasi (Supiyani et al., 2022).

            **Flip**  
            Teknik flip horizontal digunakan untuk membalik gambar secara lateral, menghasilkan citra baru yang memiliki pola cermin dari citra asli.  
            Teknik ini menambah variasi data dan membantu model dalam belajar pola dari berbagai arah tanpa mengubah makna semantik citra (Subkhi et al., 2024).

            **Rotation**  
            Rotasi citra digunakan untuk mengubah orientasi gambar pada sudut tertentu. Hal ini bertujuan agar model menjadi lebih tangguh terhadap perbedaan posisi objek dalam gambar saat pengujian (Subkhi et al., 2024).

            **Color Jitter**  
            Color jitter merupakan teknik augmentasi yang mengubah atribut visual citra seperti tingkat kecerahan (brightness), saturasi, kontras, dan rona warna (hue).  
            Tujuannya adalah untuk mensimulasikan variasi pencahayaan nyata, sehingga meningkatkan kemampuan generalisasi model (Lusen et al., 2024).

            **DataTensor**  
            Dalam konteks CNN, gambar diubah menjadi representasi tensor agar dapat diproses oleh jaringan saraf.  
            Tensor adalah struktur data multidimensi yang menyimpan informasi numerik dalam bentuk array, memungkinkan efisiensi dalam pemrosesan paralel di GPU (Lusen et al., 2024).

            **Normalisasi Data Citra**  
            Normalisasi adalah proses skala ulang nilai piksel citra, misalnya dari rentang 0–255 menjadi 0–1.  
            Ini dilakukan untuk mempercepat konvergensi selama pelatihan dan menghindari dominasi nilai besar yang dapat menyebabkan kesalahan numerik pada proses pembelajaran (Hendrik et al., 2024).
            """
        )

# ---------------------------------------------
# Menu: Flowchart Algoritma
# ---------------------------------------------
elif menu == "Flowchart Algoritma":
    st.header("3. Flowchart Algoritma")
    st.markdown(
        """
        Berikut adalah alur proses keseluruhan dari sistem klasifikasi citra jamur:
        1. **Pengumpulan Data**: Mengumpulkan dataset citra jamur.
        2. **Pra-Pemrosesan**: Melakukan augmentasi, resize, flip, rotasi, color jitter, konversi ke tensor, dan normalisasi.
        3. **Pelatihan Model**: Melatih model CNN menggunakan data yang telah diproses.
        4. **Evaluasi Model**: Menghitung metrik akurasi, confusion matrix, dll.
        5. **Prediksi**: Menerapkan model pada citra baru untuk klasifikasi.
        """
    )
    # Tampilkan flowchart (jika ada file image bernama flowchart.png di direktori project)
    flowchart_path = "assets/flowchart.png"
    if os.path.exists(flowchart_path):
        st.image(flowchart_path, caption="Flowchart Algoritma Klasifikasi Jamur", use_column_width=True)
    else:
        st.warning("File flowchart.png tidak ditemukan di folder assets/. Silakan tambahkan gambar flowchart di path tersebut.")

# ---------------------------------------------
# Menu: Hasil
# ---------------------------------------------
elif menu == "Hasil":
    st.header("4. Hasil")
    submenu_hasil = st.sidebar.selectbox(
        "Pilih Submenu Hasil",
        ["Grafik Hasil", "Evaluasi (Confusion Matrix)"]
    )

    # Submenu: Grafik Hasil
    if submenu_hasil == "Grafik Hasil":
        st.subheader("4.1 Grafik Hasil Pelatihan")
        st.markdown(
            """
            Berikut adalah contoh grafik hasil pelatihan model CNN:
            - Kurva Loss vs Epoch
            - Kurva Akurasi vs Epoch
            """
        )
        # Contoh placeholder: user dapat mengganti dengan hasil asli
        # Asumsikan ada file CSV 'training_metrics.csv' dengan kolom ['epoch','loss','accuracy']
        metrics_path = "data/results/training_metrics.csv"
        if os.path.exists(metrics_path):
            df_metrics = pd.read_csv(metrics_path)
            fig1, ax1 = plt.subplots()
            ax1.plot(df_metrics["epoch"], df_metrics["loss"], label="Loss")
            ax1.set_xlabel("Epoch")
            ax1.set_ylabel("Loss")
            ax1.set_title("Loss vs Epoch")
            ax1.legend()
            st.pyplot(fig1)

            fig2, ax2 = plt.subplots()
            ax2.plot(df_metrics["epoch"], df_metrics["accuracy"], label="Akurasi")
            ax2.set_xlabel("Epoch")
            ax2.set_ylabel("Akurasi")
            ax2.set_title("Akurasi vs Epoch")
            ax2.legend()
            st.pyplot(fig2)
        else:
            st.warning(
                "File training_metrics.csv tidak ditemukan di folder data/results/. "
                "Silakan tambahkan CSV hasil pelatihan untuk ditampilkan."
            )

    # Submenu: Evaluasi (Confusion Matrix)
    elif submenu_hasil == "Evaluasi (Confusion Matrix)":
        st.subheader("4.2 Confusion Matrix")
        st.markdown(
            """
            Confusion matrix berikut menunjukkan performa klasifikasi model pada data uji.
            """
        )
        # Contoh menampilkan confusion matrix dari file gambar
        cm_path = "data/results/confusion_matrix.png"
        if os.path.exists(cm_path):
            st.image(cm_path, caption="Confusion Matrix Model", use_column_width=True)
        else:
            st.warning(
                "File confusion_matrix.png tidak ditemukan di folder data/results/. "
                "Silakan tambahkan gambar confusion matrix untuk ditampilkan."
            )
