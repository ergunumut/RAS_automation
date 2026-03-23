import os
import shutil
import pandas as pd
from ras_commander import init_ras_project

PROJE_YOLU = r"C:\Users\dmz-admin\HCU\HEC-RAS_Projects\Finkenwerder-new\Finkenwerder.prj"

def deger_ekle_ve_formatla(orijinal_satir, eklenecek_deger):
    """
    HEC-RAS'ın 8 karakterlik sütun formatını bozmadan sayılara değer ekler.
    """
    yeni_satir = ""
    # HEC-RAS satırları genellikle 80 karakter uzunluğundadır ve 10 adet 8 karakterlik bloğa bölünmüştür.
    # Ancak bazen daha kısa olabilir. Biz her 8 karakterlik bloğu (chunk) okuyacağız.
    chunk_size = 8
    
    # Satırı 8 karakterlik parçalara böl
    chunks = [orijinal_satir[i:i+chunk_size] for i in range(0, len(orijinal_satir), chunk_size)]
    
    for chunk in chunks:
        if not chunk.strip(): # Eğer boşluksa aynen bırak
            yeni_satir += chunk
            continue
            
        try:
            # Metni sayıya çevir ve değeri ekle
            sayi = float(chunk.strip())
            yeni_sayi = sayi + eklenecek_deger
            
            # Sayıyı HEC-RAS'ın sevdiği gibi sağa dayalı 8 karakter olacak şekilde formatla
            # Virgülden sonra en fazla 3 veya 4 hane bırakmaya çalışalım
            formatli_sayi = f"{yeni_sayi:8.3f}".rstrip('0').rstrip('.')
            if len(formatli_sayi) < 8:
                 formatli_sayi = formatli_sayi.rjust(8)
            elif len(formatli_sayi) > 8:
                 # Çok büyükse bilimsel format yerine keserek sığdırmaya çalış (riskli ama HEC-RAS genelde kabul eder)
                 formatli_sayi = f"{yeni_sayi:8.2f}"
                 
            yeni_satir += formatli_sayi
            
        except ValueError:
            # Sayı değilse (örneğin yanlış hizalama varsa) aynen bırak
            yeni_satir += chunk
            
    return yeni_satir + "\n"

def stage_hydrograph_guncelle(dosya_yolu, artis_m):
    print(f"\nDosya manipüle ediliyor: {dosya_yolu}")
    print(f"Stage Hydrograph değerlerine {artis_m}m ekleniyor...")
    
    with open(dosya_yolu, 'r', encoding='utf-8') as f:
        satirlar = f.readlines()
        
    yeni_satirlar = []
    degistirilecek_satir_sayisi = 0
    okuma_modu = False
    
    for satir in satirlar:
        if satir.startswith("Stage Hydrograph="):
            yeni_satirlar.append(satir)
            # Kaç adet veri okunacağını bul
            try:
                veri_sayisi = int(satir.split('=')[1].strip())
                # Her satırda 10 değer varsa, kaç satır okunacağını hesapla
                import math
                degistirilecek_satir_sayisi = math.ceil(veri_sayisi / 10.0)
                okuma_modu = True
                continue
            except:
                okuma_modu = False
                
        if okuma_modu and degistirilecek_satir_sayisi > 0:
            # Sayı satırındayız, değeri ekle
            temiz_satir = satir.rstrip('\n') # Satır sonu karakterini şimdilik al
            islenmis_satir = deger_ekle_ve_formatla(temiz_satir, artis_m)
            yeni_satirlar.append(islenmis_satir)
            degistirilecek_satir_sayisi -= 1
            if degistirilecek_satir_sayisi == 0:
                okuma_modu = False # Bu hidrograf bloğu bitti
        else:
            yeni_satirlar.append(satir)
            
    # Dosyayı yeni verilerle kaydet
    with open(dosya_yolu, 'w', encoding='utf-8') as f:
        f.writelines(yeni_satirlar)
        
    print("✅ Dosya başarıyla güncellendi!")

def senaryo_olustur(dyke_artis_m=0.0, su_seviyesi_artis_m=0.5):
    """
    Dijital İkiz'den gelecek parametrelerle yeni bir HEC-RAS senaryosu oluşturur.
    """
    print(f"--- Dijital İkiz Senaryo Üreticisi Başlatıldı ---")
    print(f"Gelen Parametreler: Su Seviyesi Artışı = +{su_seviyesi_artis_m}m, Set Yükseltmesi = +{dyke_artis_m}m\n")
    
    try:
        my_prj = init_ras_project(PROJE_YOLU)
        
        if not hasattr(my_prj, 'plan_df') or my_prj.plan_df.empty:
            print("Plan bilgileri yüklenemedi!")
            return

        df_plans = my_prj.plan_df
        title_col = next((col for col in ['plan_title', 'plan_name', 'title', 'Plan Title', 'Name'] if col in df_plans.columns), None)
        
        if not title_col:
            print(f"Hata: Plan adını tutan sütun bulunamadı.")
            return

        base_plan = df_plans[df_plans[title_col] == '1962-plan']
        if base_plan.empty:
            print(f"Referans '1962-plan' bulunamadı!")
            return
            
        flow_col = next((col for col in ['flow_file', 'unsteady_file', 'steady_file', 'Flow File', 'flow_id'] if col in base_plan.columns), None)
        if not flow_col:
            print(f"Hata: Flow dosyası bilgisi bulunamadı.")
            return
            
        base_flow_id = str(base_plan.iloc[0][flow_col])
        
        if base_flow_id.isdigit():
             base_flow_id = "u" + base_flow_id.zfill(2)
        elif base_flow_id.startswith('.'):
             base_flow_id = "u" + base_flow_id[1:].zfill(2)
        elif base_flow_id.startswith('p') or base_flow_id.startswith('g'):
             base_flow_id = "u" + base_flow_id[1:].zfill(2)
             
        proje_klasoru = os.path.dirname(PROJE_YOLU)
        proje_kisa_adi = os.path.basename(PROJE_YOLU).split('.')[0]
        
        base_flow_yolu = os.path.join(proje_klasoru, f"{proje_kisa_adi}.{base_flow_id}")
        
        yeni_flow_id = "u99"
        yeni_flow_yolu = os.path.join(proje_klasoru, f"{proje_kisa_adi}.{yeni_flow_id}")
        
        print(f"Referans Akış Dosyası: {base_flow_yolu}")
        print(f"Yeni Senaryo Dosyası: {yeni_flow_yolu}")
        
        if os.path.exists(base_flow_yolu):
            shutil.copy2(base_flow_yolu, yeni_flow_yolu)
            print("✅ Ana akış dosyası klonlandı.")
            
            # Klonlanan dosyayı güncelle
            stage_hydrograph_guncelle(yeni_flow_yolu, su_seviyesi_artis_m)
            
            print("✅ Senaryo oluşturma işlemi tamamlandı!")
        else:
            print(f"❌ Base akış dosyası bulunamadı: {base_flow_yolu}")

    except Exception as e:
        print(f"Senaryo oluşturulurken hata: {e}")

if __name__ == "__main__":
    senaryo_olustur(dyke_artis_m=0.0, su_seviyesi_artis_m=1.2)