import h5py
import numpy as np
from ras_commander import init_ras_project

PROJE_YOLU = r"C:\Users\dmz-admin\HCU\HEC-RAS_Projects\Finkenwerder-new\Finkenwerder.prj"

def taşkın_alanı_analizi():
    print("--- 2D Taşkın Alanı (Mesh) Analizi Başlıyor ---")
    try:
        my_prj = init_ras_project(PROJE_YOLU)
        df = my_prj.results_df

        hedef_plan = df[df['plan_title'] == '1962-plan']
        if hedef_plan.empty:
            print("1962-plan bulunamadı!")
            return

        hdf_yolu = hedef_plan.iloc[0]['hdf_path']
        print(f"İncelenen Dosya: {hdf_yolu}\n")

        with h5py.File(hdf_yolu, 'r') as hdf:
            # 2D Hücre merkezlerinin koordinatlarını (X, Y) bulalım
            cell_coords_path = "/Geometry/2D Flow Areas/Perimeter 1/Cells Center Coordinate"
            
            # Unsteady kısmında 2D sonuçların olduğu tipik yol (Su Seviyesi)
            wsel_path = "/Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/2D Flow Areas/Perimeter 1/Water Surface"
            
            # Eğer WSEL tablosu Base Output'ta değilse Summary Output içinde maksimum derinlikler olabilir
            max_wsel_error_path = "/Results/Unsteady/Output/Output Blocks/Base Output/Summary Output/2D Flow Areas/Perimeter 1/Cell Maximum Water Surface Error"

            if cell_coords_path in hdf:
                coords = hdf[cell_coords_path][()]
                toplam_hucre = len(coords)
                print(f"✅ Perimeter 1 alanında toplam {toplam_hucre} adet 2D hücre bulundu.")

                # Eğer Unsteady zaman serisinde Su Seviyesi (WSEL) varsa
                if wsel_path in hdf:
                    wsel_data = hdf[wsel_path][()]
                    # axis=0 ile her hücrenin maksimum su seviyesini alıyoruz
                    max_wsel = np.max(wsel_data, axis=0) 
                    
                    # En yüksek su seviyesine sahip hücrenin indeksini bulalım
                    max_index = np.argmax(max_wsel)
                    max_deger = max_wsel[max_index]
                    max_coord = coords[max_index]
                    
                    print(f"\n🌊 TAŞKIN RİSKİ RAPORU (Maksimum Su Seviyesi):")
                    print(f"En Yüksek Su Seviyesi: {max_deger:.2f} m")
                    print(f"Bu Seviyenin Görüldüğü Koordinat (X, Y): {max_coord[0]:.2f}, {max_coord[1]:.2f}")
                    print(f"Hücre Numarası: {max_index}")
                    
                # Eğer zaman serisi yoksa ama Summary Output'ta hata tolerans verisi varsa
                elif max_wsel_error_path in hdf:
                    print("\n⚠️ Not: Zaman serisi (Time Series) WSEL verisi bulunamadı, ancak hücre hata verileri mevcut.")
                    print("Bu durum, HEC-RAS'ın ayarlarında '2D Flow Area' çıktılarının HDF'ye yazdırılmasının kapatılmış olabileceğini gösterir.")
                else:
                    print("\n⚠️ 2D Sonuç tablosu bulunamadı. Lütfen HEC-RAS'ta 'Unsteady Computation Options' altından 2D alan çıktılarının açık olduğundan emin olun.")

            else:
                 print("Perimeter 1 hücre koordinatları bulunamadı.")

    except Exception as e:
         print(f"Hata detayı: {e}")

if __name__ == "__main__":
    taşkın_alanı_analizi()