# WebScraping (with Mobile App)

![mobil](https://github.com/user-attachments/assets/a83ba0dd-5b03-49e8-a2a4-00ae57fc9ee4)

Python Selenium modulünü kullanarak Google Trends websitesinden çektiğimiz verileri yine aynı python sayfasında otomatik olarak Firebase Realtime Database'e ye kaydedip daha sonra bu verileri Android Studio IDE'si ile bir mobil uygulamaya dönüştürdüğümüz bir Web Scraping projesi.



##	GİRİŞ
 Bu proje kapsamında, Google Trends'te listelenen günün en çok aranan kelimelerini Python ve Selenium kütüphanesi kullanarak web scraping yöntemiyle çekmek, ardından bu verileri yine aynı Python projesinde Firebase Realtime Database'e kaydetmek amaçlanmaktadır. Projenin devamında, Android Studio'da Java ve XML kullanarak bu verilerin mobil uygulama üzerinde listelenmesi hedeflenmiştir. Listelenen haberlere tıklandığında ilgili habere giderek, güncel arama trendlerini anlık olarak takip etmek ve bu verileri mobil platformlarda erişilebilir hale getirmek için kullanılabilir.
 
## Projeyi Çalıştırmak İçin Gereksinimler
Chrome tarayıcınız ile uyumlu ChromeDriver'ı indirip, yolunu doğru vermeniz.
Kendi FirebaseRealtime database admin(veritabanına erişimi yetkliendirme) dosyasınızı indirerek ilgili phyton kodu satırına doğru yolu vermeniz.

## Projenin Çalıştırılma Videosu
[Videoyu İzleyin](https://www.youtube.com/watch?v=ua9dStmtMPM)


## MATERYAL YÖNTEM
Bu projede kullanılan başlıca yöntem ve araçlar aşağıda sıralanmıştır:
⦁	Python: Web scraping ve veri işleme için kullanılan programlama dili.
⦁	Firebase: Gerçek zamanlı veri tabanı olarak kullanmak için Google veritabanı.
⦁	Android Studio: Android uygulama geliştirme ortamı için IDE.
⦁	Java ve XML: Android uygulama geliştirme için kullanılan programlama dilleri.

## KODLARIN AKIŞI VE AÇIKLAMALARI

İlk olarak, Google Trends’ten verileri çekmek için Selenium modülünü kullandık;
 
```python
chrome_path = "C:\\Users\\DevNyxen\\Desktop\\chromedriver.exe" 
options = Options()
options.headless = True  # Arka planda çalıştırma
service = Service(chrome_path)
driver = webdriver.Chrome(service=service, options=options)

# URL'ye git
url = "https://trends.google.com/trends/trendingsearches/daily?geo=TR&hl=tr"
driver.get(url)

# Sayfanın tam olarak yüklenmesini beklemek için biraz bekleme
time.sleep(5)
```

Yukarıdaki kodlarda önce Selenium’un çalışacağı Chrome Driver yolunu belirttik.  ‘headless’ modunda Chrome tarayıcısını başlattık. Devamında Chrome Driver servisi ve Selenium Web Driver’ı başlatılıyor.

 Firebase tarafında ise firebase_admin modulünü ve gerekli sınıfları import ediyoruz. Kimlik doğrulama için veritabanından oluşturup indirdiğimiz Json dosyamızı da bildiriyoruz. Inıtıalize_app ile Firebase uygulamasını başlatıyoruz ve veritabanı URL’sini veriyoruz. Son olarak daha sonra elde edeceğimiz datayı yollayacağımız ref değişkenini tanımlayıp tablo başlık adını da belirliyoruz.


```python
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("C:\\Users\\DevNyxen\\Desktop\\trendsearchtr-firebase-adminsdk-9j74s-d1e111b880.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://trendsearchtr-default-rtdb.firebaseio.com/'
})

ref = db.reference('/trending_searches')
```

Servisler ve sürücüler başlatıldıktan sonra Selenium’un gitmesi gereken URL’i belirtip ‘driver.get’ komutu ile URL’e gitmesini sağlıyoruz. Sayfanın tam olarak yüklenmesi için 5 saniyelik bir bekleme süresi veriyoruz. Son satırda ise bize lazım olan div öğesini CLASS adından buluyoruz.


```python
url = "https://trends.google.com/trends/trendingsearches/daily?geo=TR&hl=tr"
driver.get(url)

# Sayfanın tam olarak yüklenmesini beklemek için biraz bekleme
time.sleep(5)

 
div = driver.find_element(By.CLASS_NAME, "feed-list-wrapper")
```

Bulduğumuz div öğesinin içinden önce md-list-block sınıfına sahip tüm öğeleri daha sonra her md_list içindeki feed-item etiketine sahip öğeleri buluyoruz. 

```python
md_lists = div.find_elements(By.CLASS_NAME, "md-list-block")

    for md_list in md_lists:
         # Her feed-item öğesini bul
        feed_items = md_list.find_elements(By.TAG_NAME, "feed-item")

        for feed_item in feed_items:
```

Her feed_item için, çeşitli verileri (index, title, image_url, news_detail_text, new_source, search_count, share_url) find_element ve find_elements yöntemleri ile çekiyoruz.

```python
index = int(feed_item.find_element(By.CLASS_NAME, "index").text.strip())
                title = feed_item.find_element(By.CLASS_NAME, "title").text.strip()
                image_url = feed_item.find_element(By.CSS_SELECTOR, ".feed-item-image-wrapper img").get_attribute("src")
                    
                news_detail_elem = feed_item.find_element(By.CLASS_NAME, "details-bottom")
                news_detail_text = news_detail_elem.text.strip()
                    
                new_source = feed_item.find_element(By.CLASS_NAME, "image-text").text.strip() if feed_item.find_element(By.CLASS_NAME, "image-text") else None

                search_count_elem = feed_item.find_element(By.CLASS_NAME, "search-count-title")
                search_count = search_count_elem.text.strip()
                    
                share_url_elem = feed_item.find_element(By.CLASS_NAME, "image-link-wrapper")
                share_url = share_url_elem.find_element(By.TAG_NAME,"a").get_attribute("ng-href")
```


Tüm bu elde edilen verileri;

```python
        data = {
                    "number": index,
                    "title": title,
                    "image_url": image_url,
                    "search_count": search_count,
                    "new_details":  news_detail_text,
                    "new_source": new_source,
                    "share_url": share_url
                }
                ref.push(data)
```

Data sözlüğünde topluyoruz ve daha önce tanımladığımız veritabanı ref değişkenimize ref.push methodu ile bu bilgileri Firebase Realtime Database’e  gönderiyoruz.
Artık verilerimiz veritabanımızda hazır bir şekilde bekliyor. Geriye kalan Android tarafında bu verileri kullanıcının rahatça takip edebileceği şekilde listelemek.

### Android Studio ile Veri Gösterimi
Android Studio da Firebase kurulumlarını yaptıktan sonra ihtiyacımıza göre bir Model hazırladık.
Modeli Recyclerview öğemizle iliştirerek her bir Recyclerview itemi için hazırladığımız tasarıma gelen verileri Adapter aracılığı ile yerleştirdik.


```java
 public void getTrendSearchs(){
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        DatabaseReference tasksRef = database.getReference("trending_searches/");
        tasksRef.addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                itemList.clear();
                if (dataSnapshot.getChildrenCount() == 0){

                }else{
                    for (DataSnapshot snapshot : dataSnapshot.getChildren()) {
                        // Firebase'den verileri TodoItem nesnelerine dönüştürün ve listeye ekleyin.
                        Searchs searchsItem = snapshot.getValue(Searchs.class);
                        itemList.add(searchsItem);
                    }
                    adapter.setItemList(itemList);
                }
            }

            @Override
            public void onCancelled(DatabaseError databaseError) {
                Log.e("Firebase", "Veri çekme işlemi başarısız: " + databaseError.getMessage());
            }
        });

    }
```


Veritabanı yolumuzu belirtip tek seferlik bir çekme işlemi methodu olan addListenerForSingleValueEvent ile veritabanımızdan verileri çekiyoruz. Gelen veriyi Search modelimizin bir örneğine eşitleyip liste içerisine atıyoruz. Her bir veri için bu işlemi for döngüsü içerisinde tekrar ediyoruz. Liste içerisinde artık modelimizdeki değişken değerlerini almış itemler tasarımdaki elemanlarla eşleştirilmek üzere hazırda bekliyor.


```java
    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        Searchs item = itemList.get(position);
        holder.numberTextView.setText(String.valueOf(item.getNumber()));
        holder.titleTextView.setText(item.getTitle());
        holder.contentTextView.setText(item.getNew_details());
        holder.readCountTextView.setText(item.getSearch_count());

        String img_url = item.getImage_url();
        new DownloadImageTask(holder.news_imageView).execute(img_url);

        String new_url = item.getShare_url();
        holder.cardView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                listener.onItemClick(new_url);
            }
        });

    }
```


Adapterimiz ile de liste içerisindeki her bir itemi Modeldeki ilgili değişkenden çekerek Xml de hazırladığımız tasarımın ilgili elemana atıyoruz. 


## SONUÇLAR VE DEĞERLENDİRME

Proje sonucunda, Google Trends'ten çekilen günlük en popüler arama kelimeleri başarılı bir şekilde Firebase Realtime Database'e kaydedilmiş ve bu veriler Android uygulaması üzerinde gerçek zamanlı olarak listelenmiştir. Bu süreç, web scraping, veri tabanı yönetimi ve mobil uygulama geliştirme konularında değerli deneyimler kazandırmıştır.
Projenin temel kazanımları şunlardır:

⦁	Google Trends verilerini otomatik olarak çekebilme.

⦁	Çekilen verileri gerçek zamanlı olarak Firebase'e kaydedebilme.

⦁	Verileri mobil uygulama üzerinde gerçek zamanlı olarak görüntüleyebilme.

⦁	Python, Selenium, Firebase, Java ve XML gibi çeşitli teknolojilerin entegrasyonunu gerçekleştirme.

Bu proje, veri analizi ve mobil uygulama geliştirme alanlarında yapılacak daha geniş çaplı çalışmalar için bir temel oluşturmaktadır.

