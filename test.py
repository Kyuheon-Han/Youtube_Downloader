import qrcode

def make_qr(data, filename="qrcode.png"):
    img = qrcode.make(data)
    img.save(filename)
    print(f"QR코드가 {filename}로 저장되었습니다.")

if __name__ == "__main__":
    text = input("QR코드로 만들 내용을 입력하세요: ")
    make_qr(text)
