import os
import subprocess
import time
from ras_commander import init_ras_project

HEC_RAS_EXE = r"C:\Program Files (x86)\HEC\HEC-RAS\6.6\Ras.exe"
PROJE_YOLU = r"C:\Users\dmz-admin\HCU\HEC-RAS_Projects\Finkenwerder-new\Finkenwerder.prj"
PLAN_ISMI = "1962-plan"

def CLI_motorunu_atesle():
    print("--- HEC-RAS Native Komut Satırı (CLI) Motoru Başlatılıyor ---")
    
    try:
        my_prj = init_ras_project(PROJE_YOLU)
        df_plans = my_prj.plan_df
        
        # Sütun adlarını yazdıralım ki ne aradığımızı bilelim (Sorun giderici - Debug)
        print("Bulunan Sütunlar:", df_plans.columns.tolist())
        
        title_col = next((col for col in ['plan_title', 'plan_name', 'title', 'Plan Title', 'Name'] if col in df_plans.columns), None)
        if not title_col:
            print(f"Hata: Plan adını ('{PLAN_ISMI}') arayacak uygun bir sütun bulunamadı!")
            return
            
        hedef_plan = df_plans[df_plans[title_col] == PLAN_ISMI]
        
        if hedef_plan.empty:
            print(f"Hata: {PLAN_ISMI} projede bulunamadı.")
            return
            
        # Plan dosya uzantısını (örn: '.p04' veya sadece 'p04') barındıran sütunu bul
        # Farklı versiyonlarda isim değiştiği için listeyi geniş tutuyoruz
        plan_col = next((col for col in ['plan_file', 'plan_number', 'plan_id', 'Plan File', 'plan', 'extension'] if col in hedef_plan.columns), None)
        
        if not plan_col:
            print(f"❌ Hata: Plan dosyası bilgisini (plan_col) tutan sütun bulunamadı.")
            print(f"Lütfen yukarıda yazdırılan 'Bulunan Sütunlar' listesinden hangisinin uzantıyı (örn. 'p04') tuttuğuna bakın.")
            return

        plan_file_id = str(hedef_plan.iloc[0][plan_col])
        
        if plan_file_id.startswith('.'):
             plan_file_id = "p" + plan_file_id[1:].zfill(2)
        elif plan_file_id.isdigit():
             plan_file_id = "p" + plan_file_id.zfill(2)
             
        proje_kisa_adi = os.path.basename(PROJE_YOLU).split('.')[0]
        plan_yolu = os.path.join(os.path.dirname(PROJE_YOLU), f"{proje_kisa_adi}.{plan_file_id}")
        
        print(f"📁 Proje: {os.path.basename(PROJE_YOLU)}")
        print(f"🎯 Plan Dosyası: {os.path.basename(plan_yolu)}")
        
        if not os.path.exists(plan_yolu):
            print(f"❌ Hata: Plan dosyası fiziksel olarak bulunamadı -> {plan_yolu}")
            return
            
        print(f"\n🚀 {PLAN_ISMI} motor tarafından hesaplanıyor... Lütfen bekleyin.")
        print(f"(Bu pencere işlem bitene kadar bekleyecektir)")
        
        baslangic_zamani = time.time()
        
  # 2. HEC-RAS'ın katı kurallarına göre (Zorunlu tırnak işaretleriyle) komutu tek bir metin (string) olarak hazırlıyoruz
        komut_metni = f'"{HEC_RAS_EXE}" "{PROJE_YOLU}" "{plan_yolu}" -c'
        
        print(f"Gönderilen Komut: {komut_metni}")
        
        # 3. Komutu çalıştır (shell=True ile metni doğrudan CMD'ye atıyoruz ki Python tırnaklarımızı silmesin)
        islem = subprocess.run(komut_metni, capture_output=True, text=True, shell=True)
        
        islem = subprocess.run(komut, capture_output=True, text=True)
        
        sure = (time.time() - baslangic_zamani) / 60
        print(f"\n🎉 HESAPLAMA TAMAMLANDI! (Süre: {sure:.2f} dakika)")
        
        if islem.stdout:
            print("HEC-RAS Mesajı:", islem.stdout.strip())
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"💥 Motor çalıştırılırken hata: {e}")

if __name__ == "__main__":
    CLI_motorunu_atesle()