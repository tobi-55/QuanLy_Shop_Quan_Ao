# Ứng dụng Quản lý Shop Quần Áo

## Mô tả
Ứng dụng quản lý shop quần áo được phát triển bằng Python và Tkinter, hỗ trợ các chức năng CRUD hoàn chỉnh.

## Tính năng
-  Đăng nhập/Đăng ký với phân quyền
-  Quản lý sản phẩm (CRUD)
-  Tìm kiếm sản phẩm
-  Lấy dữ liệu từ API
-  Lưu trữ dữ liệu bằng JSON
-  Giao diện thân thiện với người dùng

## Cài đặt

### Yêu cầu hệ thống
- Python 3.7+
- Kết nối internet (cho chức năng API)

### Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Chạy ứng dụng
```bash
python main.py
```

## Tài khoản mặc định
- **Admin**: username: `admin`, password: `admin123`
- **User**: username: `user`, password: `user123`

## Đóng gói ứng dụng

### Tạo file thực thi
```bash
python setup.py build
```

Sau khi build thành công, file thực thi sẽ nằm trong thư mục `build/`

## Cấu trúc dự án
```
├── main.py              # File chính
├── setup.py            # Script đóng gói
├── requirements.txt    # Dependencies
├── products.json       # Dữ liệu sản phẩm
├── users.json          # Dữ liệu người dùng
└── README.md          # Hướng dẫn
```

## Chức năng chi tiết

### Đăng nhập/Đăng ký
- Hỗ trợ tạo tài khoản mới
- Mã hóa mật khẩu SHA-256
- Phân quyền Admin/User

### Quản lý sản phẩm (Admin)
- Thêm sản phẩm mới
- Cập nhật thông tin sản phẩm
- Xóa sản phẩm
- Lấy dữ liệu từ API

### Tìm kiếm
- Tìm kiếm theo tên, loại, mô tả
- Tìm kiếm real-time

### API Integration
- Lấy dữ liệu mẫu từ API
- Xử lý bất đồng bộ với threading

## Hỗ trợ
Nếu gặp vấn đề, vui lòng tạo issue hoặc liên hệ developer.