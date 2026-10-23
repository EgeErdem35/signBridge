# SB-16 - AUTSL Dataset Access Request

**Jira:** [SB-16](https://el-dili.atlassian.net/browse/SB-16)  
**Project:** SignBridge-TR, Yaşar University Software Engineering senior project  
**Record date:** 21 October 2026  
**Status:** Request sent; developer response received; archive download and extraction not yet verified.

## Access method and sources

The official [Ankara University AUTSL page](https://cvml.ankara.edu.tr/datasets/) identifies the dataset and contact route and links to the [ChaLearn access page](https://chalearnlap.cvc.uab.es/dataset/40/description/). The dataset paper is O. M. Sincan and H. Y. Keleş, "AUTSL: A Large Scale Multi-Modal Turkish Sign Language Dataset and Baseline Methods," IEEE Access, 2020 ([paper](https://arxiv.org/abs/2008.00932)).

An initial request to hkeles@ankara.edu.tr failed with an undeliverable-address notice. The request was then sent to Hacer Yalım Keleş at the current Hacettepe address listed on the [department faculty page](https://cs.hacettepe.edu.tr/_sub_pages/faculty_members_tr.html). A separate request to co-author Özge Mercanoğlu Sincan was also sent on 20 October 2026 at 22:05, as shown in the supplied email thread.

## Sending and review record

| Field | Record |
|---|---|
| Sender | Ceren Bilgenoğlu, 23070006053@stu.yasar.edu.tr |
| Recipient | Hacer Yalım Keleş, hacerkeles@cs.hacettepe.edu.tr |
| Sent | 20 October 2026, 22:02 (time displayed in the sender's mailbox, Türkiye) |
| CC | Dr. Öğr. Üyesi Kazım Erdoğdu, kazim.erdogdu@yasar.edu.tr |
| Subject | AUTSL Veri Setine Akademik Erişim Talebi — Yaşar Üniversitesi SignBridge-TR |
| Pre-send review | Ceren confirmed that all teammates reviewed and approved the draft before sending. Individual approval timestamps are not recorded here. |
| Advisor permission | Ceren confirmed permission to mention the advisor and include him in CC. This is not recorded as separate advisor approval of the email wording. |
| Evidence | Sent-email screenshot supplied by Ceren; response email thread supplied privately; team-review confirmation supplied by Ceren. |

## Sent request text (Turkish)

Sayın Hacer Hocam,

AUTSL veri setine ilişkin erişim talebimizi, Ankara Üniversitesi AUTSL sayfasında belirtilen hkeles@ankara.edu.tr adresine ilettik; ancak adresin bulunamadığına dair teslim edilememe bildirimi aldık. Bu nedenle talebimizi Hacettepe Üniversitesi sayfanızda yer alan güncel e-posta adresiniz üzerinden paylaşmak istedik. Ben Yaşar Üniversitesi Yazılım Mühendisliği öğrencisi Ceren Bilgenoğlu. Altı kişilik ekibimizle, Dr. Öğr. Üyesi Kazım Erdoğdu danışmanlığında yürüttüğümüz SignBridge-TR bitirme projemiz kapsamında, geliştirdiğiniz AUTSL veri setinden yararlanmak istiyoruz.

Projemiz, Türk İşaret Dili ile Türkçe metin ve ses arasında iki yönlü iletişimi destekleyen, erişilebilir ve tarayıcı tabanlı bir prototip geliştirmeyi amaçlamaktadır. İşaret tanıma bileşeninde, videolardan MediaPipe ile çıkaracağımız el, yüz ve vücut işaret noktaları üzerinde tanıma modellerini eğitmeyi ve işaretçiden bağımsız olarak değerlendirmeyi planlıyoruz. İlk sürümün kapsamı, tekil ve kısa duraklamalarla ayrılmış işaretlerle sınırlıdır.

Ankara Üniversitesi AUTSL sayfasını ve buradan yönlendirilen ChaLearn erişim sayfasını inceledik. Eğitim, doğrulama ve test verilerine güncel erişim yöntemi, gerekiyorsa arşiv şifrelerinin temini ve tamamlamamız gereken başvuru işlemleri konusunda bizi yönlendirebilir misiniz? Gerekli bir kullanım sözleşmesi, başvuru formu veya danışman onayı bulunuyorsa bunları sağlamaktan memnuniyet duyarız.

Veri setini yalnızca akademik ve ticari olmayan amaçlarla kullanmayı, ilgili yayınlara uygun biçimde atıf yapmayı ve kullanım koşullarına uymayı taahhüt ediyoruz. Veri setini veya çıkarılan işaret noktalarını açık izin olmadan yeniden dağıtmayacağız. Çıkarılan işaret noktalarının kullanımı için ayrıca geçerli koşullar varsa bunları da öğrenmek isteriz.

Proje danışmanımız:  
Dr. Öğr. Üyesi Kazım Erdoğdu  
Yaşar Üniversitesi  
kazim.erdogdu@yasar.edu.tr

Gerekli görmeniz hâlinde proje önerimizi ve ek bilgileri paylaşabiliriz. Talebimizi farklı bir kişiye veya birime iletmemiz gerekiyorsa yönlendirmenizi rica ederiz.

Zamanınız ve desteğiniz için teşekkür ederim.

Saygılarımla,  
Ceren Bilgenoğlu  
Yaşar Üniversitesi — Yazılım Mühendisliği  
SignBridge-TR Proje Ekibi Adına

*Transcribed from the sent text provided by Ceren; formatting normalised. The screenshot confirms the recipient, CC name, subject, sending time and visible opening.*

## Response and access verification

On 21 October 2026 around midday (as reported by Ceren), Hacer Yalım Keleş replied with training, validation and test download links, label/class-mapping links and archive passwords, plus extraction instructions.

A limited connectivity check from the assistant's execution environment returned HTTP 206 and the first 1,024 bytes of the class-mapping CSV (server-reported total: 4,063 bytes). Sample requests to the training, validation and test archives timed out. These timeouts do not establish that the links are broken. Full archive download, password-based extraction, completeness and dataset contents have not been verified.

No claim is made that additional redistribution permissions were granted. Use remains subject to the dataset's applicable terms and proper citation. Any redistribution of derived landmarks requires checking the terms or obtaining explicit permission.

## Follow-up

- Verify archive download and extraction from the team's environment.
- Audit labels, sign classes and signer-independent splits before training.
- Retain the original correspondence and access credentials privately with the team.
- Record subsequent verification results separately; coordinate the proposal status with SB-18.

Passwords, private download URLs, raw response correspondence and dataset files are intentionally excluded from this repository.
