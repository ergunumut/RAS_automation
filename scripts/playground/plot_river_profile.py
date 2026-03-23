import h5py
import numpy as np # Maksimum değerleri bulmak için numpy ekledik
import matplotlib.pyplot as plt
from ras_commander import init_ras_project

PROJE_YOLU = r"C:\Users\dmz-admin\HCU\HEC-RAS_Projects\Finkenwerder-new\Finkenwerder.prj"

def nehir_profili_ciz():
    print("--- River Elbe Maksimum Profil Analizi Başlıyor ---")
    try:
        my_prj = init_ras_project(PROJE_YOLU)
        df = my_prj.results_df

        hedef_plan = df[df['plan_title'] == '1962-plan']
        if hedef_plan.empty:
            print("1962-plan bulunamadı!")
            return

        hdf_yolu = hedef_plan.iloc[0]['hdf_path']

        with h5py.File(hdf_yolu, 'r') as hdf:
            flow_path = '/Results/Post Process/Steady/Output/Output Blocks/Base Output/Post Process/Post Process Profiles/Cross Sections/Flow'
            ws_path = '/Results/Post Process/Steady/Output/Output Blocks/Base Output/Post Process/Post Process Profiles/Cross Sections/Water Surface'
            
            if all(p in hdf for p in [flow_path, ws_path]):
                # Verileri okuyalım (Bu veriler 2 boyutlu bir matris şeklindedir: [zaman_adımı, kesit_no])
                flows_raw = hdf[flow_path][()]
                water_surfaces_raw = hdf[ws_path][()]
                
                # Her bir kesit (sütun) için MAKSİMUM değerleri bulalım (axis=0 sütunlar boyunca maksimumu alır)
                max_flows = np.max(flows_raw, axis=0)
                max_water_surfaces = np.max(water_surfaces_raw, axis=0)
                
                # İstasyonları ayarlayalım
                stations = range(len(max_flows))

                # Grafiği Çizelim
                fig, ax1 = plt.subplots(figsize=(12, 6))

                # Sol Eksen: Maksimum Su Seviyesi
                color = 'tab:blue'
                ax1.set_xlabel('Kesit Sırası / İstasyon (Akış Yönü)')
                ax1.set_ylabel('Maksimum Su Seviyesi (m)', color=color)
                # Artık sadece tek bir çizgi (maksimum profil) çizecek
                ax1.plot(stations, max_water_surfaces, color=color, linewidth=2, label="Max Su Seviyesi")
                ax1.tick_params(axis='y', labelcolor=color)

                # Sağ Eksen: Maksimum Debi
                ax2 = ax1.twinx()  
                color = 'tab:red'
                ax2.set_ylabel('Maksimum Debi (m³/s)', color=color)
                # Artık sadece tek bir çizgi (maksimum profil) çizecek
                ax2.plot(stations, max_flows, color=color, linewidth=2, linestyle='--', label="Max Debi")
                ax2.tick_params(axis='y', labelcolor=color)

                # Ortak Ayarlar
                plt.title('River Elbe: Maksimum Su Seviyesi ve Debi Profili (1962 Senaryosu)')
                ax1.grid(True, linestyle=':', alpha=0.7)
                
                lines_1, labels_1 = ax1.get_legend_handles_labels()
                lines_2, labels_2 = ax2.get_legend_handles_labels()
                ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')

                fig.tight_layout()
                
                output_path = "results/elbe_max_profili.png"
                plt.savefig(output_path)
                print(f"Profil grafiği başarıyla kaydedildi: {output_path}")
                plt.show()

            else:
                print("İstenen Flow veya Water Surface tabloları bulunamadı.")

    except Exception as e:
        print(f"Grafik çiziminde hata: {e}")

if __name__ == "__main__":
    nehir_profili_ciz()