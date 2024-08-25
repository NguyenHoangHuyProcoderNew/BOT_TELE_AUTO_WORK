# Yêu cầu người dùng nhập thời gian key
def nhap_thoigian_key(message):
    bot_reply(user_id, "Vui lòng nhập thời gian của key\nChỉ được nhập dữ liệu là số nguyên và trong khoảng từ 1-365:")
    log_info(f"Người dùng {username} đã sử dụng lệnh /ios_user")
    log_info("Bot đang yêu cầu người dùng nhập thời gian của key")

    bot.register_next_step_handler(message, xuly_taokey_ios_user)

# Xử lý tạo key IOS User
def xuly_taokey_ios_user(message):
    global thoigian_key
    thoigian_key = int(message.text) # Chuyển dữ liệu mà nguồi dùng đã nhập thành số nguyên

    bot_reply(user_id, f"Tiến hành tạo: 01 key\nThiết bị: IOS\nServer: IOS USER\nThời gian sử dụng key: {thoigian_key} ngày")
    log_info(f"Người dùng đã yêu cầu tạo 1 key {thoigian_key} ngày")

    # Kiểm tra dữ liệu mà người dùng đã nhập
    if thoigian_key == 1:
        taokey_1ngay(message)
    elif thoigian_key == 7:
        taokey_7ngay(message)
    elif thoigian_key == 30:
        taokey_30ngay(message)
    elif thoigian_key == 365:
        taokey_365ngay(message)
    elif thoigian_key not in [1, 7, 30, 365]:
        taokey_thucong(message)
    else:
        return

# Tạo key 1 ngày
def taokey_1ngay(message):
    bot_reply(user_id, "Đang tạo key...")

    log_info("Khởi tạo chrome driver")
    driver = webdriver.Chrome(service=service, options=options)

    log_info("Tạo key bằng API có sẵn của web")
    driver.get('https://v3.ppapikey.xyz/pages/get-key?idgoi=128&email=nguyenhoanghuyprocoder@gmail.com&token=LOzCeWYL0Ffqj6o9w4zOWuY9NcbkyJ0zytzj8HzkQdCMTQ0ubBYz9R5K5MvxJjNDDWkNQBlo8idLJpZDjxyh7TAJ0BylLELdxRli&loaikey=1day&luotdung=1')

    # Kiểm tra xem có tạo key thành công hay không
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/button')))

        bot_reply(user_id, "Tạo key thành công")
        log_success("Tạo thành công 1 key")
    except TimeoutError:
        bot_reply(user_id, "Tạo key không thành công, xảy ra sự cố kết nối internet")
        log_info("Tạo key không thành công, xảy ra sự cố kết nối internet")

    # Lấy dữ liệu của phần tử chứa mã key
    try:
        # Đợi phần tử chứa key xuất hiện
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#keyDiv'))
        )
        
        # Lấy dữ liệu của phần tử chứa key
        lay_makey = driver.find_element(By.ID, 'keyDiv')

        # Chuyển dữ liệu của phần tử chứa key thành văn bản
        dulieu_makey = driver.execute_script("return arguments[0].textContent;", lay_makey).strip()   

        # Lọc bỏ những dữ liệu không cần thiết
        locdulieu_makey = json.loads(dulieu_makey)
        key_cuoicung = locdulieu_makey['key']
    except TimeoutException:
        bot_reply(user_id, "Không thể lấy dữ liệu của mã key, xảy ra sự cố kết nối internet")
        log_error("Không thể lấy dữ liệu của mã key, xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return

    # Gửi key đã tạo cho người dùng
    bot_reply(user_id, "Key của bạn là:")
    log_info("Gửi key đã tạo cho người dùng")

    bot_reply(user_id, f"{key_cuoicung}") # Gửi key đã tạo cho người dùng
    log_success("Gửi key cho người dùng thành công")

    log_info("Đóng trình duyệt chrome")
    driver.quit()

    log_info("Kết thúc tiến trình")
    return

# Tạo key 7 ngày
def taokey_7ngay(message):
    bot_reply(user_id, "Đang tạo key...")

    log_info("Khởi tạo chrome driver")
    driver = webdriver.Chrome(service=service, options=options)

    log_info("Tạo key bằng API có sẵn của web")
    driver.get('https://v3.ppapikey.xyz/pages/get-key?idgoi=128&email=nguyenhoanghuyprocoder@gmail.com&token=LOzCeWYL0Ffqj6o9w4zOWuY9NcbkyJ0zytzj8HzkQdCMTQ0ubBYz9R5K5MvxJjNDDWkNQBlo8idLJpZDjxyh7TAJ0BylLELdxRli&loaikey=7day&luotdung=1')

    # Kiểm tra xem có tạo key thành công hay không
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/button')))

        bot_reply(user_id, "Tạo key thành công")
        log_success("Tạo thành công 1 key")
    except TimeoutError:
        bot_reply(user_id, "Tạo key không thành công, xảy ra sự cố kết nối internet")
        log_info("Tạo key không thành công, xảy ra sự cố kết nối internet")

    # Lấy dữ liệu của phần tử chứa mã key
    try:
        # Đợi phần tử chứa key xuất hiện
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#keyDiv'))
        )
        
        # Lấy dữ liệu của phần tử chứa key
        lay_makey = driver.find_element(By.ID, 'keyDiv')

        # Chuyển dữ liệu của phần tử chứa key thành văn bản
        dulieu_makey = driver.execute_script("return arguments[0].textContent;", lay_makey).strip()   

        # Lọc bỏ những dữ liệu không cần thiết
        locdulieu_makey = json.loads(dulieu_makey)
        key_cuoicung = locdulieu_makey['key']
    except TimeoutException:
        bot_reply(user_id, "Không thể lấy dữ liệu của mã key, xảy ra sự cố kết nối internet")
        log_error("Không thể lấy dữ liệu của mã key, xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return

    # Gửi key đã tạo cho người dùng
    bot_reply(user_id, "Key của bạn là:")
    log_info("Gửi key đã tạo cho người dùng")

    bot_reply(user_id, f"{key_cuoicung}") # Gửi key đã tạo cho người dùng
    log_success("Gửi key cho người dùng thành công")

    log_info("Đóng trình duyệt chrome")
    driver.quit()

    log_info("Kết thúc tiến trình")
    return

def taokey_30ngay(message):
    bot_reply(user_id, "Đang tạo key...")

    log_info("Khởi tạo chrome driver")
    driver = webdriver.Chrome(service=service, options=options)

    log_info("Tạo key bằng API có sẵn của web")
    driver.get('https://v3.ppapikey.xyz/pages/get-key?idgoi=128&email=nguyenhoanghuyprocoder@gmail.com&token=LOzCeWYL0Ffqj6o9w4zOWuY9NcbkyJ0zytzj8HzkQdCMTQ0ubBYz9R5K5MvxJjNDDWkNQBlo8idLJpZDjxyh7TAJ0BylLELdxRli&loaikey=30day&luotdung=1')

    # Kiểm tra xem có tạo key thành công hay không
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/button')))

        bot_reply(user_id, "Tạo key thành công")
        log_success("Tạo thành công 1 key")
    except TimeoutError:
        bot_reply(user_id, "Tạo key không thành công, xảy ra sự cố kết nối internet")
        log_info("Tạo key không thành công, xảy ra sự cố kết nối internet")

    # Lấy dữ liệu của phần tử chứa mã key
    try:
        # Đợi phần tử chứa key xuất hiện
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#keyDiv'))
        )
        
        # Lấy dữ liệu của phần tử chứa key
        lay_makey = driver.find_element(By.ID, 'keyDiv')

        # Chuyển dữ liệu của phần tử chứa key thành văn bản
        dulieu_makey = driver.execute_script("return arguments[0].textContent;", lay_makey).strip()   

        # Lọc bỏ những dữ liệu không cần thiết
        locdulieu_makey = json.loads(dulieu_makey)
        key_cuoicung = locdulieu_makey['key']
    except TimeoutException:
        bot_reply(user_id, "Không thể lấy dữ liệu của mã key, xảy ra sự cố kết nối internet")
        log_error("Không thể lấy dữ liệu của mã key, xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return

    # Gửi key đã tạo cho người dùng
    bot_reply(user_id, "Key của bạn là:")
    log_info("Gửi key đã tạo cho người dùng")

    bot_reply(user_id, f"{key_cuoicung}") # Gửi key đã tạo cho người dùng
    log_success("Gửi key cho người dùng thành công")

    log_info("Đóng trình duyệt chrome")
    driver.quit()

    log_info("Kết thúc tiến trình")
    return

def taokey_365ngay(message):
    bot_reply(user_id, "Đang tạo key...")

    log_info("Khởi tạo chrome driver")
    driver = webdriver.Chrome(service=service, options=options)

    log_info("Tạo key bằng API có sẵn của web")
    driver.get('https://v3.ppapikey.xyz/pages/get-key?idgoi=128&email=nguyenhoanghuyprocoder@gmail.com&token=LOzCeWYL0Ffqj6o9w4zOWuY9NcbkyJ0zytzj8HzkQdCMTQ0ubBYz9R5K5MvxJjNDDWkNQBlo8idLJpZDjxyh7TAJ0BylLELdxRli&loaikey=365day&luotdung=1')

    # Kiểm tra xem có tạo key thành công hay không
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/button')))

        bot_reply(user_id, "Tạo key thành công")
        log_success("Tạo thành công 1 key")
    except TimeoutError:
        bot_reply(user_id, "Tạo key không thành công, xảy ra sự cố kết nối internet")
        log_info("Tạo key không thành công, xảy ra sự cố kết nối internet")

    # Lấy dữ liệu của phần tử chứa mã key
    try:
        # Đợi phần tử chứa key xuất hiện
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#keyDiv'))
        )
        
        # Lấy dữ liệu của phần tử chứa key
        lay_makey = driver.find_element(By.ID, 'keyDiv')

        # Chuyển dữ liệu của phần tử chứa key thành văn bản
        dulieu_makey = driver.execute_script("return arguments[0].textContent;", lay_makey).strip()   

        # Lọc bỏ những dữ liệu không cần thiết
        locdulieu_makey = json.loads(dulieu_makey)
        key_cuoicung = locdulieu_makey['key']
    except TimeoutException:
        bot_reply(user_id, "Không thể lấy dữ liệu của mã key, xảy ra sự cố kết nối internet")
        log_error("Không thể lấy dữ liệu của mã key, xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return

    # Gửi key đã tạo cho người dùng
    bot_reply(user_id, "Key của bạn là:")
    log_info("Gửi key đã tạo cho người dùng")

    bot_reply(user_id, f"{key_cuoicung}") # Gửi key đã tạo cho người dùng
    log_success("Gửi key cho người dùng thành công")

    log_info("Đóng trình duyệt chrome")
    driver.quit()

    log_info("Kết thúc tiến trình")
    return

def taokey_thucong(message):
    global thoigian_key
    thoigian_key = int(message.text) # Chuyển dữ liệu mà nguồi dùng đã nhập thành số nguyên

    bot_reply(user_id, "Mở trang web tạo key")
    log_info(f"Người dùng đã yêu cầu tạo 1 key {thoigian_key} ngày")

    log_info("Khởi tạo chrome driver")
    driver = webdriver.Chrome(service=service, options=options)

    log_info("Mở trang web tạo key")
    driver.get('https://new.ppapikey.xyz/pagesMain/auth-login')

    # Kiểm tra xem có mở trang web tạo key thành công hay không
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div/div')))

        bot_reply(user_id, "Mở trang web tạo key thành công")
        log_success("Truy cập trang tạo key thành công")
    except TimeoutError:
        bot_reply(user_id, "Mở trang web tạo key thất bại, xảy ra sự cố kết nối internet")
        log_error("Truy cập trang tạo key thất bại, xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return        

    bot_reply(user_id, "Đăng nhập vào web tạo key")
    log_info("Tiến hành dăng nhập vào web tạo key")
    
    log_info("Đang nhập tài khoản")
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/form/div[1]/input").send_keys('nguyenhoanghuyprocoder@gmail.com')

    log_info("Đang nhập mật khẩu")
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/form/div[2]/div[2]/input").send_keys('123321Huy')

    log_info("Click vào nút đăng nhập")
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/form/div[4]/button").click()

    # Kiểm tra xem có đăng nhập thành công hay không
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/nav/div')))

        bot_reply(user_id, "Đăng nhập vào web tạo key thành công")
        log_success("Đăng nhập thành công")
    except TimeoutError:
        bot_reply(user_id, "Đăng nhập thất bại, xảy ra sự cố kết nối internet")
        log_error("Đăng nhập thất bại, xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return                

    bot_reply(user_id, "Mở trang để tạo key mới")
    log_info("Mở trang để tạo key mới")

    driver.get('https://new.ppapikey.xyz/pagesMain/key')

    # Kiểm tra xem có truy cập trang để tạo key mới thành công hay không
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div/div/div[1]/div/div/div/div[1]/div/div/h4')))
        
        bot_reply(user_id, "Truy cập vào trang để tạo key mới thành công")
        log_success("Truy cập vào trang để tạo key mới thành công")
    except TimeoutError:
        bot_reply(user_id, "Truy cập trang để tạo key mới thất bại, xảy ra sự cố kết nối internet")
        log_error("Truy cập trang để tạo key mới thất bại, xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return

    log_info("Click vào nút tạo key động")
    driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div[1]/div/div/div/div[2]/div[4]/button[2]").click()

    #### ĐIỀN THÔNG TIN KEY ####
    bot_reply(user_id, "Tiến hành điền thông tin của key")
    log_info("Điền thông tin key")

    # log_info("Đang nhập số lượng key")
    # driver.find_element(By.XPATH, "/html/body/main/div/div/div/div/div/div[2]/form/div[1]/div[1]/div/input").send_keys("1")

    # log_info("Đang nhập số lượng thiết bị")
    # driver.find_element(By.XPATH, "/html/body/main/div/div/div/div/div/div[2]/form/div[1]/div[2]/div/input").send_keys("1")

    log_info("Đang nhập thời gian của key")
    input_thoigiankey = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div[1]/div/div/div/div[2]/div[2]/form/div[3]/div/input")
    input_thoigiankey.clear() # Xoá dữ liệu của ô thời gian key
    input_thoigiankey.send_keys(thoigian_key)

    log_info("Chọn package IOS User")
    driver.find_element(By.CSS_SELECTOR, "#packageid2 > option:nth-child(2)").click()

    log_info("Click vào nút tạo key")
    driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div[1]/div/div/div/div[2]/div[2]/form/div[4]/div/button").click()

    # Kiểm tra xem có tạo key thành công hay không
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'swal2-html-container'))
        )
        
        bot_reply(user_id, "Tạo key thành công")
        log_success("Tạo key thành công")
    except TimeoutError:
        bot_reply(user_id, "Tạo key thất bại, xảy ra sự cố kết nối internet")
        log_error("Tạo key thất bại, xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return        

    # Lấy dữ liệu mã key đã tạo
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'swal2-html-container'))
        )

        log_info("Phần tử chứa mã key đã xuất hiện")
    except Exception as e:
        bot_reply(user_id, "Phẩn tử chứa mã key không xuất hiện, xảy ra sự cố kết nối internet")
        log_error("Phẩn tử chứa mã key không xuất hiện, xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return

    # Gửi key cho người dùng

    log_info("Lấy dữ liệu của phần tử chứa mã key")
    dulieu_key = driver.execute_script("return document.querySelector('.swal2-html-container').innerText;")

    log_info(f"Lấy dữ liệu thành công - dữ liệu lấy được là: {dulieu_key}")

    log_info("Gửi key cho người dùng")
    bot_reply(user_id, f"{dulieu_key}")

    log_success("Gửi key cho người dùng thành công")

    log_info("Đóng trình duyệt Chrome")
    driver.quit()

    log_info("Kết thúc tiến trình")
    return
