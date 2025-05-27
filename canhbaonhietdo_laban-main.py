from microbit import *
import music

# Ngưỡng cảnh báo
TEMP_THRESHOLD = 30  # Độ C
LIGHT_THRESHOLD = 150  # Thang 0-255

# Icon cảnh báo
WARNING_ICON = Image("99999:"
                     "90009:"
                     "90009:"
                     "90009:"
                     "99999")

# Trạng thái
mode = 0  # 0: Menu, 1: Alert, 2: Compass
alert_active = False

def get_compass_display(heading):
    # Xác định hướng chính xác để hiển thị chữ
    if 337.5 <= heading < 360 or 0 <= heading < 22.5:
        return "N"
    elif 67.5 <= heading < 112.5:
        return "E"
    elif 157.5 <= heading < 202.5:
        return "S"
    elif 247.5 <= heading < 292.5:
        return "W"
    
    # Hiển thị đồng hồ (pixel sáng cho 8 hướng)
    display.clear()
    if 337.5 <= heading < 360 or 0 <= heading < 22.5:
        display.set_pixel(2, 0, 9)  # Bắc
    elif 22.5 <= heading < 67.5:
        display.set_pixel(3, 1, 9)  # Đông-Bắc
    elif 67.5 <= heading < 112.5:
        display.set_pixel(4, 2, 9)  # Đông
    elif 112.5 <= heading < 157.5:
        display.set_pixel(3, 3, 9)  # Đông-Nam
    elif 157.5 <= heading < 202.5:
        display.set_pixel(2, 4, 9)  # Nam
    elif 202.5 <= heading < 247.5:
        display.set_pixel(1, 3, 9)  # Tây-Nam
    elif 247.5 <= heading < 292.5:
        display.set_pixel(0, 2, 9)  # Tây
    elif 292.5 <= heading < 337.5:
        display.set_pixel(1, 1, 9)  # Tây-Bắc
    return None  # Không hiển thị chữ nếu không đúng hướng

while True:
    if mode == 0:  # Menu
        display.scroll("A: Alert B: Compass", delay=100, wait=False)
        if button_a.is_pressed():
            mode = 1
            alert_active = False
            music.stop()
            display.clear()
            sleep(200)
        elif button_b.is_pressed():
            mode = 2
            compass.calibrate()
            display.clear()
            sleep(200)
        sleep(50)
        continue
    
    if mode == 1:  # Chế độ cảnh báo
        # Đọc cảm biến
        temp = temperature()
        light = display.read_light_level()
        
        # Kích hoạt cảnh báo nếu vượt ngưỡng
        if (temp > TEMP_THRESHOLD or light > LIGHT_THRESHOLD) and not alert_active:
            alert_active = True
        
        if alert_active:
            # Cảnh báo: Icon chớp tắt và âm thanh liên tục
            display.show(WARNING_ICON)
            music.play(['C5:2'], wait=False)
            sleep(300)
            display.clear()
            sleep(300)
            
            # Nút A: Tắt cảnh báo
            if button_a.is_pressed():
                alert_active = False
                music.stop()
                display.clear()
                sleep(200)
            # Nút B: Chuyển sang la bàn
            elif button_b.is_pressed():
                mode = 2
                alert_active = False
                music.stop()
                compass.calibrate()
                display.clear()
                sleep(200)
        else:
            # Bình thường: Hiển thị thông tin
            display.clear()
            display.scroll("T:" + str(temp) + "C L:" + str(light), delay=100)
            
            # Nút B: Chuyển sang la bàn
            if button_b.is_pressed():
                mode = 2
                compass.calibrate()
                display.clear()
                sleep(200)
        
        sleep(1000)
        continue
    
    if mode == 2:  # Chế độ la bàn
        # Hiển thị hướng kiểu đồng hồ hoặc chữ
        heading = compass.heading()
        display_value = get_compass_display(heading)
        if display_value:
            display.show(display_value)
        
        # Nút A: Hiệu chỉnh la bàn
        if button_a.is_pressed():
            compass.calibrate()
            display.clear()
            sleep(200)
        # Nút B: Chuyển sang cảnh báo
        elif button_b.is_pressed():
            mode = 1
            alert_active = False
            music.stop()
            display.clear()
            sleep(200)
        
        sleep(500)  # Cập nhật la bàn mỗi 0.5 giây