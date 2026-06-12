; *** Inno Setup Thai messages ***
; Encoding: UTF-8 with BOM

[LangOptions]
LanguageName=ภาษาไทย
LanguageID=$041E
LanguageCodePage=0

[Messages]

; *** Application titles
SetupAppTitle=ติดตั้ง
SetupWindowTitle=ติดตั้ง - %1
UninstallAppTitle=ถอนการติดตั้ง
UninstallAppFullTitle=%1 - ถอนการติดตั้ง

; *** Misc. common
InformationTitle=ข้อมูล
ConfirmTitle=ยืนยัน
ErrorTitle=ข้อผิดพลาด

; *** SetupLdr messages
SetupLdrStartupMessage=โปรแกรมนี้จะติดตั้ง %1 ลงในคอมพิวเตอร์ของคุณ คุณต้องการดำเนินการต่อหรือไม่?
LdrCannotCreateTemp=ไม่สามารถสร้างไฟล์ชั่วคราวได้ การติดตั้งถูกยกเลิก
LdrCannotExecTemp=ไม่สามารถรันไฟล์ในโฟลเดอร์ชั่วคราวได้ การติดตั้งถูกยกเลิก
HelpTextNote=

; *** Startup error messages
LastErrorMessage=%1.%n%nข้อผิดพลาด %2: %3
SetupFileMissing=ไม่พบไฟล์ %1 ในโฟลเดอร์ติดตั้ง โปรดแก้ไขปัญหาหรือรับสำเนาโปรแกรมใหม่
SetupFileCorrupt=ไฟล์ติดตั้งเสียหาย โปรดรับสำเนาโปรแกรมใหม่
SetupFileCorruptOrWrongVer=ไฟล์ติดตั้งเสียหายหรือไม่เข้ากับตัวติดตั้งนี้ โปรดแก้ไขปัญหาหรือรับสำเนาโปรแกรมใหม่
InvalidParameter=มีการส่งพารามิเตอร์ไม่ถูกต้องผ่านบรรทัดคำสั่ง:%n%n%1
SetupAlreadyRunning=กำลังรันตัวติดตั้งอยู่แล้ว
WindowsVersionNotSupported=โปรแกรมนี้ไม่รองรับเวอร์ชัน Windows ที่คุณใช้อยู่
WindowsServicePackRequired=โปรแกรมนี้ต้องการ %1 Service Pack %2 หรือใหม่กว่า
NotOnThisPlatform=โปรแกรมนี้ไม่รองรับการทำงานบน %1
OnlyOnThisPlatform=โปรแกรมนี้ต้องทำงานบน %1
OnlyOnTheseArchitectures=โปรแกรมนี้สามารถติดตั้งได้บน Windows ที่ออกแบบสำหรับสถาปัตยกรรมโปรเซสเซอร์ต่อไปนี้:%n%n%1
WinVersionTooLowError=โปรแกรมนี้ต้องการ %1 เวอร์ชัน %2 หรือใหม่กว่า
WinVersionTooHighError=โปรแกรมนี้ไม่สามารถติดตั้งบน %1 เวอร์ชัน %2 หรือใหม่กว่า
AdminPrivilegesRequired=คุณต้องเข้าสู่ระบบในฐานะผู้ดูแลระบบเมื่อติดตั้งโปรแกรมนี้
PowerUserPrivilegesRequired=คุณต้องเข้าสู่ระบบในฐานะผู้ดูแลระบบหรือสมาชิกกลุ่ม Power Users เมื่อติดตั้งโปรแกรมนี้
SetupAppRunningError=ตัวติดตั้งตรวจพบว่า %1 กำลังทำงานอยู่%n%nโปรดปิดทุกอินสแตนซ์ก่อน แล้วคลิก ตกลง เพื่อดำเนินการต่อ หรือ ยกเลิก เพื่อออก
UninstallAppRunningError=โปรแกรมถอนการติดตั้งตรวจพบว่า %1 กำลังทำงานอยู่%n%nโปรดปิดทุกอินสแตนซ์ก่อน แล้วคลิก ตกลง เพื่อดำเนินการต่อ หรือ ยกเลิก เพื่อออก

; *** Startup questions
PrivilegesRequiredOverrideTitle=เลือกโหมดการติดตั้ง
PrivilegesRequiredOverrideInstruction=เลือกโหมดการติดตั้ง
PrivilegesRequiredOverrideText1=%1 สามารถติดตั้งสำหรับผู้ใช้ทุกคน (ต้องการสิทธิ์ผู้ดูแล) หรือสำหรับคุณเท่านั้น
PrivilegesRequiredOverrideText2=%1 สามารถติดตั้งสำหรับคุณเท่านั้น หรือสำหรับผู้ใช้ทุกคน (ต้องการสิทธิ์ผู้ดูแล)
PrivilegesRequiredOverrideAllUsers=ติดตั้งสำหรับ&ผู้ใช้ทุกคน
PrivilegesRequiredOverrideAllUsersRecommended=ติดตั้งสำหรับ&ผู้ใช้ทุกคน (แนะนำ)
PrivilegesRequiredOverrideCurrentUser=ติดตั้งสำหรับ&ฉันเท่านั้น
PrivilegesRequiredOverrideCurrentUserRecommended=ติดตั้งสำหรับ&ฉันเท่านั้น (แนะนำ)

; *** Misc. errors
ErrorCreatingDir=ตัวติดตั้งไม่สามารถสร้างโฟลเดอร์ "%1"
ErrorTooManyFilesInDir=ไม่สามารถสร้างไฟล์ในโฟลเดอร์ "%1" เนื่องจากมีไฟล์มากเกินไป

; *** Setup common messages
ExitSetupTitle=ออกจากตัวติดตั้ง
ExitSetupMessage=การติดตั้งยังไม่สมบูรณ์ หากออกตอนนี้ โปรแกรมจะไม่ได้รับการติดตั้ง%n%nคุณสามารถรันตัวติดตั้งอีกครั้งในภายหลัง%n%nออกจากตัวติดตั้ง?
AboutSetupMenuItem=&เกี่ยวกับตัวติดตั้ง...
AboutSetupTitle=เกี่ยวกับตัวติดตั้ง
AboutSetupMessage=%1 เวอร์ชัน %2%n%3%n%n%1 หน้าหลัก:%n%4
AboutSetupNote=
TranslatorNote=

; *** Buttons
ButtonBack=< &ย้อนกลับ
ButtonNext=&ถัดไป >
ButtonInstall=&ติดตั้ง
ButtonOK=ตกลง
ButtonCancel=ยกเลิก
ButtonYes=&ใช่
ButtonYesToAll=ใช่&ทั้งหมด
ButtonNo=&ไม่
ButtonNoToAll=ไ&ม่ทั้งหมด
ButtonFinish=&เสร็จสิ้น
ButtonBrowse=&เรียกดู...
ButtonWizardBrowse=เ&รียกดู...
ButtonNewFolder=&สร้างโฟลเดอร์ใหม่

; *** "Select Language" dialog messages
SelectLanguageTitle=เลือกภาษา
SelectLanguageLabel=เลือกภาษาที่ใช้ระหว่างการติดตั้ง

; *** Common wizard text
ClickNext=คลิก ถัดไป เพื่อดำเนินการต่อ หรือ ยกเลิก เพื่อออกจากตัวติดตั้ง
BeveledLabel=
BrowseDialogTitle=เรียกดูโฟลเดอร์
BrowseDialogLabel=เลือกโฟลเดอร์จากรายการด้านล่าง แล้วคลิก ตกลง
NewFolderName=โฟลเดอร์ใหม่

; *** "Welcome" wizard page
WelcomeLabel1=ยินดีต้อนรับสู่วิซาร์ดติดตั้ง [name]
WelcomeLabel2=โปรแกรมนี้จะติดตั้ง [name/ver] ลงในคอมพิวเตอร์ของคุณ%n%nแนะนำให้ปิดแอปพลิเคชันอื่นทั้งหมดก่อนดำเนินการต่อ

; *** "Password" wizard page
WizardPassword=รหัสผ่าน
PasswordLabel1=การติดตั้งนี้ป้องกันด้วยรหัสผ่าน
PasswordLabel3=โปรดใส่รหัสผ่าน แล้วคลิก ถัดไป รหัสผ่านคำนึงถึงตัวพิมพ์เล็กและใหญ่
PasswordEditLabel=&รหัสผ่าน:
IncorrectPassword=รหัสผ่านที่คุณกรอกไม่ถูกต้อง โปรดลองใหม่

; *** "License Agreement" wizard page
WizardLicense=ข้อตกลงการอนุญาตใช้งาน
LicenseLabel=โปรดอ่านข้อมูลสำคัญต่อไปนี้ก่อนดำเนินการต่อ
LicenseLabel3=โปรดอ่านข้อตกลงการอนุญาตใช้งานต่อไปนี้ คุณต้องยอมรับข้อตกลงนี้ก่อนดำเนินการต่อ
LicenseAccepted=ฉัน&ยอมรับข้อตกลง
LicenseNotAccepted=ฉัน&ไม่ยอมรับข้อตกลง

; *** "Information" wizard pages
WizardInfoBefore=ข้อมูล
InfoBeforeLabel=โปรดอ่านข้อมูลสำคัญต่อไปนี้ก่อนดำเนินการต่อ
InfoBeforeClickLabel=เมื่ออ่านครบแล้ว คลิก ถัดไป เพื่อดำเนินการต่อ
WizardInfoAfter=ข้อมูล
InfoAfterLabel=โปรดอ่านข้อมูลสำคัญต่อไปนี้ก่อนดำเนินการต่อ
InfoAfterClickLabel=เมื่ออ่านครบแล้ว คลิก ถัดไป เพื่อดำเนินการต่อ

; *** "User Information" wizard page
WizardUserInfo=ข้อมูลผู้ใช้
UserInfoDesc=โปรดกรอกข้อมูลของคุณ
UserInfoName=&ชื่อผู้ใช้:
UserInfoOrg=&องค์กร:
UserInfoSerial=&รหัสสินค้า:
UserInfoNameRequired=คุณต้องกรอกชื่อ

; *** "Select Destination Location" wizard page
WizardSelectDir=เลือกโฟลเดอร์ติดตั้ง
SelectDirDesc=คุณต้องการติดตั้ง [name] ที่ใด?
SelectDirLabel3=ตัวติดตั้งจะติดตั้ง [name] ลงในโฟลเดอร์ต่อไปนี้
SelectDirBrowseLabel=คลิก ถัดไป เพื่อดำเนินการต่อ หรือคลิก เรียกดู เพื่อเลือกโฟลเดอร์อื่น
DiskSpaceGBLabel=ต้องการพื้นที่ว่างอย่างน้อย [gb] GB
DiskSpaceMBLabel=ต้องการพื้นที่ว่างอย่างน้อย [mb] MB
CannotInstallToNetworkDrive=ไม่สามารถติดตั้งไปยังไดรฟ์เครือข่ายได้
CannotInstallToUNCPath=ไม่สามารถติดตั้งไปยังพาธ UNC ได้
InvalidPath=คุณต้องระบุพาธแบบเต็มพร้อมตัวอักษรไดรฟ์ เช่น:%n%nC:\APP%n%nหรือพาธ UNC ในรูปแบบ:%n%n\\server\share
InvalidDrive=ไดรฟ์หรือแชร์ที่คุณเลือกไม่มีอยู่หรือเข้าถึงไม่ได้ โปรดเลือกใหม่
DiskSpaceWarningTitle=พื้นที่ดิสก์ไม่เพียงพอ
DiskSpaceWarning=ตัวติดตั้งต้องการพื้นที่ว่างอย่างน้อย %1 KB แต่ไดรฟ์ที่เลือกมีพื้นที่ว่างเพียง %2 KB%n%nคุณต้องการดำเนินการต่อหรือไม่?
DirNameTooLong=ชื่อโฟลเดอร์หรือพาธยาวเกินไป
InvalidDirName=ชื่อโฟลเดอร์ไม่ถูกต้อง
BadDirName32=ชื่อโฟลเดอร์ต้องไม่มีอักขระต่อไปนี้:%n%n%1
DirExistsTitle=โฟลเดอร์มีอยู่แล้ว
DirExists=โฟลเดอร์:%n%n%1%n%nมีอยู่แล้ว คุณต้องการติดตั้งลงในโฟลเดอร์นี้หรือไม่?
DirDoesntExistTitle=ไม่พบโฟลเดอร์
DirDoesntExist=ไม่พบโฟลเดอร์:%n%n%1%n%nคุณต้องการสร้างโฟลเดอร์นี้หรือไม่?

; *** "Select Components" wizard page
WizardSelectComponents=เลือกส่วนประกอบ
SelectComponentsDesc=ส่วนประกอบใดที่ควรติดตั้ง?
SelectComponentsLabel2=เลือกส่วนประกอบที่ต้องการติดตั้ง แล้วยกเลิกการเลือกส่วนที่ไม่ต้องการ คลิก ถัดไป เมื่อพร้อม
FullInstallation=ติดตั้งทั้งหมด
CompactInstallation=ติดตั้งแบบย่อ
CustomInstallation=ติดตั้งแบบกำหนดเอง
NoUninstallWarningTitle=พบส่วนประกอบที่ติดตั้งแล้ว
NoUninstallWarning=ตัวติดตั้งตรวจพบว่าส่วนประกอบต่อไปนี้ติดตั้งแล้ว:%n%n%1%n%nการยกเลิกการเลือกจะไม่ถอนการติดตั้ง%n%nคุณต้องการดำเนินการต่อหรือไม่?
ComponentSize1=%1 KB
ComponentSize2=%1 MB
ComponentsDiskSpaceGBLabel=การเลือกปัจจุบันต้องการพื้นที่อย่างน้อย [gb] GB
ComponentsDiskSpaceMBLabel=การเลือกปัจจุบันต้องการพื้นที่อย่างน้อย [mb] MB

; *** "Select Additional Tasks" wizard page
WizardSelectTasks=งานเพิ่มเติม
SelectTasksDesc=งานเพิ่มเติมใดที่ควรดำเนินการ?
SelectTasksLabel2=เลือกงานเพิ่มเติมที่ต้องการระหว่างการติดตั้ง [name] แล้วคลิก ถัดไป

; *** "Select Start Menu Folder" wizard page
WizardSelectProgramGroup=เลือกโฟลเดอร์เมนู Start
SelectStartMenuFolderDesc=ตัวติดตั้งจะสร้างทางลัดในโฟลเดอร์ใด?
SelectStartMenuFolderLabel3=ตัวติดตั้งจะสร้างทางลัดในโฟลเดอร์เมนู Start ต่อไปนี้
SelectStartMenuFolderBrowseLabel=คลิก ถัดไป เพื่อดำเนินการต่อ หรือ เรียกดู เพื่อเลือกโฟลเดอร์อื่น
MustEnterGroupName=คุณต้องกรอกชื่อโฟลเดอร์
GroupNameTooLong=ชื่อโฟลเดอร์หรือพาธยาวเกินไป
InvalidGroupName=ชื่อโฟลเดอร์ไม่ถูกต้อง
BadGroupName=ชื่อโฟลเดอร์ต้องไม่มีอักขระต่อไปนี้:%n%n%1
NoProgramGroupCheck2=&ไม่สร้างโฟลเดอร์ในเมนู Start

; *** "Ready to Install" wizard page
WizardReady=พร้อมติดตั้ง
ReadyLabel1=ตัวติดตั้งพร้อมติดตั้ง [name] ลงในคอมพิวเตอร์ของคุณแล้ว
ReadyLabel2a=คลิก ติดตั้ง เพื่อดำเนินการต่อ หรือ ย้อนกลับ เพื่อตรวจสอบหรือเปลี่ยนแปลงการตั้งค่า
ReadyLabel2b=คลิก ติดตั้ง เพื่อดำเนินการต่อ
ReadyMemoUserInfo=ข้อมูลผู้ใช้:
ReadyMemoDir=โฟลเดอร์ปลายทาง:
ReadyMemoType=ประเภทการติดตั้ง:
ReadyMemoComponents=ส่วนประกอบที่เลือก:
ReadyMemoGroup=โฟลเดอร์เมนู Start:
ReadyMemoTasks=งานเพิ่มเติม:

; *** TDownloadWizardPage wizard page
DownloadingLabel2=กำลังดาวน์โหลดไฟล์...
ButtonStopDownload=&หยุดดาวน์โหลด
StopDownload=คุณต้องการหยุดการดาวน์โหลดหรือไม่?
ErrorDownloadAborted=การดาวน์โหลดถูกยกเลิก
ErrorDownloadFailed=การดาวน์โหลดล้มเหลว: %1 %2
ErrorDownloadSizeFailed=ไม่สามารถรับขนาดได้: %1 %2
ErrorProgress=ความคืบหน้าไม่ถูกต้อง: %1 จาก %2
ErrorFileSize=ขนาดไฟล์ไม่ถูกต้อง: คาดหวัง %1 พบ %2

; *** TExtractionWizardPage wizard page
ExtractingLabel=กำลังแตกไฟล์...
ButtonStopExtraction=&หยุดการแตกไฟล์
StopExtraction=คุณต้องการหยุดการแตกไฟล์หรือไม่?
ErrorExtractionAborted=การแตกไฟล์ถูกยกเลิก
ErrorExtractionFailed=การแตกไฟล์ล้มเหลว: %1

; *** Archive extraction failure details
ArchiveIncorrectPassword=รหัสผ่านไม่ถูกต้อง
ArchiveIsCorrupted=ไฟล์อาร์ไคฟ์เสียหาย
ArchiveUnsupportedFormat=รูปแบบอาร์ไคฟ์ไม่รองรับ

; *** "Preparing to Install" wizard page
WizardPreparing=กำลังเตรียมการติดตั้ง
PreparingDesc=กำลังเตรียมติดตั้ง [name] ลงในคอมพิวเตอร์ของคุณ
PreviousInstallNotCompleted=การติดตั้งหรือถอนการติดตั้งครั้งก่อนไม่สมบูรณ์ คุณต้องรีสตาร์ทคอมพิวเตอร์ก่อน%n%nหลังรีสตาร์ท ให้รันตัวติดตั้งอีกครั้งเพื่อติดตั้ง [name] ให้สมบูรณ์
CannotContinue=ไม่สามารถดำเนินการต่อได้ โปรดคลิก ยกเลิก เพื่อออก
ApplicationsFound=แอปพลิเคชันต่อไปนี้กำลังใช้ไฟล์ที่ต้องอัปเดต แนะนำให้อนุญาตตัวติดตั้งปิดแอปพลิเคชันเหล่านี้โดยอัตโนมัติ
ApplicationsFound2=แอปพลิเคชันต่อไปนี้กำลังใช้ไฟล์ที่ต้องอัปเดต แนะนำให้อนุญาตตัวติดตั้งปิดแอปพลิเคชันเหล่านี้โดยอัตโนมัติ หลังติดตั้งเสร็จ ตัวติดตั้งจะพยายามรีสตาร์ทแอปพลิเคชัน
CloseApplications=&ปิดแอปพลิเคชันโดยอัตโนมัติ
DontCloseApplications=&ไม่ปิดแอปพลิเคชัน
ErrorCloseApplications=ตัวติดตั้งไม่สามารถปิดแอปพลิเคชันทั้งหมดได้โดยอัตโนมัติ แนะนำให้ปิดแอปพลิเคชันที่ใช้ไฟล์ที่ต้องอัปเดตก่อนดำเนินการต่อ
PrepareToInstallNeedsRestart=ตัวติดตั้งต้องรีสตาร์ทระบบ หลังรีสตาร์ทให้รันตัวติดตั้งอีกครั้งเพื่อติดตั้ง [name] ให้สมบูรณ์%n%nคุณต้องการรีสตาร์ทตอนนี้หรือไม่?

; *** "Installing" wizard page
WizardInstalling=กำลังติดตั้ง
InstallingLabel=โปรดรอขณะติดตั้ง [name] ลงในคอมพิวเตอร์ของคุณ

; *** "Setup Completed" wizard page
FinishedHeadingLabel=เสร็