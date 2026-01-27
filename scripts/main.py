from ras_commander import init_ras_project

PROJE_YOLU = r"C:\Users\dmz-admin\HCU\HEC-RAS_Projects\Finkenwerder-new\Finkenwerder.prj"

def plan_ozeti_cikar():
    print("--- Finkenwerder Proje Analizi ---")
    try:
        my_prj = init_ras_project(PROJE_YOLU)
        df = my_prj.results_df

        if not df.empty:
            # Sadece istediğimiz sütunları seçip yazdıralım
            for index, row in df.iterrows():
                print(f"\n> PLAN: {row['plan_title']} (No: {row['plan_number']})")
                print(f"  Durum: {'HDF Dosyası Mevcut' if row['hdf_exists'] else 'HDF Bulunamadı'}")
                print(f"  Simülasyon Süresi: {row['simulation_duration_hours']} saat")
                print(f"  Hacim Hatası: %{row['vol_error_percent']:.6f}")
                
                # Başlangıç ve Bitiş Hacimleri (Su dengesi kontrolü)
                fark = row['vol_ending'] - row['vol_starting']
                print(f"  Net Hacim Değişimi: {fark:.2f} m3")
        else:
            print("Sonuç tablosu boş!")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    plan_ozeti_cikar()