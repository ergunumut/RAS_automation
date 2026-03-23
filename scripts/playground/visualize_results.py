import matplotlib.pyplot as plt
import pandas as pd
from ras_commander import init_ras_project

PROJE_YOLU = r"C:\Users\dmz-admin\HCU\HEC-RAS_Projects\Finkenwerder-new\Finkenwerder.prj"

def sonuclari_gorsellestir():
    print("--- Veriler Grafiğe Dönüştürülüyor ---")
    try:
        my_prj = init_ras_project(PROJE_YOLU)
        df = my_prj.results_df

        if df.empty:
            print("Görselleştirecek veri bulunamadı!")
            return

        # Grafik hazırlığı
        plans = df['plan_title']
        start_vols = df['vol_starting']
        end_vols = df['vol_ending']

        x = range(len(plans))
        width = 0.35

        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Başlangıç ve Bitiş barları
        bar1 = ax.bar([i - width/2 for i in x], start_vols, width, label='Başlangıç Hacmi (m³)', color='#3498db')
        bar2 = ax.bar([i + width/2 for i in x], end_vols, width, label='Bitiş Hacmi (m³)', color='#e67e22')

        # Estetik dokunuşlar
        ax.set_ylabel('Hacim (m³)')
        ax.set_title('HEC-RAS Planları Hacim Karşılaştırması')
        ax.set_xticks(x)
        ax.set_xticklabels(plans)
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Değerleri barların üzerine yazalım
        ax.bar_label(bar1, padding=3, fmt='%.0f')
        ax.bar_label(bar2, padding=3, fmt='%.0f')

        plt.tight_layout()
        
        # Grafiği results klasörüne kaydet
        output_path = "results/hacim_kiyasi.png"
        plt.savefig(output_path)
        print(f"Grafik başarıyla kaydedildi: {output_path}")
        
        # Grafiği ekranda göster
        plt.show()

    except Exception as e:
        print(f"Görselleştirme hatası: {e}")

if __name__ == "__main__":
    sonuclari_gorsellestir()