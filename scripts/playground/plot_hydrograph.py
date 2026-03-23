import h5py
from ras_commander import init_ras_project

PROJE_YOLU = r"C:\Users\dmz-admin\HCU\HEC-RAS_Projects\Finkenwerder-new\Finkenwerder.prj"

def hedef_plani_incele():
    print("--- 1962-plan İçin Sonuçlar Aranıyor ---")
    try:
        my_prj = init_ras_project(PROJE_YOLU)
        df = my_prj.results_df

        # Sadece '1962-plan' isimli satırı filtreleyelim
        hedef_plan = df[df['plan_title'] == '1962-plan']

        if hedef_plan.empty:
            print("Hata: '1962-plan' isimli plan tablodan bulunamadı!")
            return

        # Planın HDF yolunu alalım (Muhtemelen p04.hdf olacak)
        hdf_yolu = hedef_plan.iloc[0]['hdf_path']
        print(f"Seçilen Plan: 1962-plan")
        print(f"İncelenen Dosya: {hdf_yolu}\n")

        # HDF dosyasının içine girelim
        with h5py.File(hdf_yolu, 'r') as hdf:
            # En kritik kontrol: Dosyada 'Results' klasörü var mı?
            if 'Results' in hdf:
                print("🎉 HARİKA HABER: Bu planda simülasyon sonuçları (Results) mevcut!")
                
                bulunan_yollar = []
                # Sadece Results klasörünün içini tarayalım
                def bul_fonksiyonu(isim, nesne):
                    if isinstance(nesne, h5py.Dataset) and ('Time' in isim or 'Flow' in isim or 'Water Surface' in isim):
                        bulunan_yollar.append(isim)
                
                hdf['Results'].visititems(bul_fonksiyonu)
                
                print("\nBULUNAN SONUÇ VERİLERİ (Zaman, Akış ve Su Seviyesi):")
                for yol in bulunan_yollar[:20]: # Ekran dolmasın diye ilk 20'yi yazdıralım
                    print(f"/Results/{yol}")
                    
            else:
                print("⚠️ Maalesef bu planda da sadece 'Geometry' var. /Results klasörü bulunamadı.")
                print("Bu durum, simülasyonun (Compute) henüz çalıştırılmadığını veya yarıda kesildiğini gösterir.")

    except Exception as e:
        print(f"Hata detayı: {e}")

if __name__ == "__main__":
    hedef_plani_incele()