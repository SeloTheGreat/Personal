hi

# IGNORE BELOW

Robotik alanında en sık kullanılan bileşenlerden biri sensörlerdir. Sensörler, çevresel olaylarının 
sonucundan yada sürecinden oluşan tepkileri dijital veriye dönüştürürler, ve bu dijital veriler kod ortamımızda kullanılabilir.

Bu metin mikro-denetleyici olarak standart bir Arduino UNO modeli kullanacaktır.

Bu metin özellikle iki sensör hakkındadır, bu sensörler
- Sıcaklık Sensörü
- Nem Sensörü

Başlamak için bu iki tür sensörden ayrıca bahsedilecek ve sonradan ikisini birleştiren bir uygulamaya bakacağız.

*Sıcaklık Sensörü*
Sıcaklık sensörleri, adındaki gibi, ortamdaki sıcaklık değerini analog bir sinyale dönüştürerek belirli bir pinden dışarıya doğru aktarır.

Bu metin sıcaklık sensörü olarak TMP36 sıcaklık ölçü sensörünü kullanacaktır.

Bu sensörde üç pin bulunur: Güç, vout (value out / veri çıkış) ve toprak pinleridir; güç pini güç kaynağına bağlanır, vout pini analog sinyali okuyacağımız girişe bağlanır, ve toprak pini topraklayan bir akıma yönlendirilir.
TMP36 sıcaklık değişimlerine bağlı olarak elektriksel özellikleri tutarlı bir şekilde değişen bir yarıiletken malzeme içerir. Sıcaklık değiştikçe merkez pindeki (vout pin) sinyal de değişir, bu sinyal standart 5 volt a bağlıyken ortam sıcaklığına bağlı olarak 0 ile 1023 (standart arduino analog sinyal çözünürlüğü, yani 10 bit) arasında sürekli bir değere sahiptir.
Mikro-denetleyicide kullanacağımız kütüphaneler bu sinyali °C veya °F olarak insan anlaşılabilir bir değere dönüştürebilir.

[ŞEMA]

Kod:
void setup() {
Serial.begin(9600);
}

void loop() {
int sicaklik = analogRead(A0);
Serial.println(sicaklik);
delay(500);
}

Bu uygulama mikro-denetleyici ile TMP36 sensörünün algıladığı ortam sıcaklığını seri port aracılığı ile çıktıya  yazdırır.