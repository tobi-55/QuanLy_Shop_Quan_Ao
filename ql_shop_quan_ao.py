import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import hashlib
import requests
from datetime import datetime
import threading

class ClothingShopManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quản Lý Shop Quần Áo")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f0f0')
        
        # File paths
        self.products_file = "products.json"
        self.users_file = "users.json"
        
        # Current user
        self.current_user = None
        self.is_admin = False
        
        # Initialize data files
        self.init_data_files()
        
        # Create login window
        self.create_login_window()
        
    def init_data_files(self):
        """Khởi tạo các file dữ liệu nếu chưa tồn tại"""
        try:
            # Initialize products file
            if not os.path.exists(self.products_file):
                print("Creating products.json file")
                with open(self.products_file, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
            
            # Initialize users file with default admin
            if not os.path.exists(self.users_file):
                print("Creating users.json file")
                default_users = [
                    {
                        "username": "admin",
                        "password": self.hash_password("admin123"),
                        "role": "admin",
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    },
                    {
                        "username": "user",
                        "password": self.hash_password("user123"),
                        "role": "user",
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                ]
                with open(self.users_file, 'w', encoding='utf-8') as f:
                    json.dump(default_users, f, ensure_ascii=False, indent=2)
                print(f"Created default users: admin/admin123, user/user123")
                
        except Exception as e:
            print(f"Error initializing data files: {str(e)}")
            messagebox.showerror("Lỗi", f"Không thể khởi tạo file dữ liệu: {str(e)}")
    
    def hash_password(self, password):
        """Mã hóa mật khẩu"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def load_json_data(self, filename):
        """Đọc dữ liệu từ file JSON"""
        try:
            if not os.path.exists(filename):
                print(f"File {filename} không tồn tại, tạo file mới")
                return []
            
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"Loaded data from {filename}: {len(data)} items")
                return data
        except json.JSONDecodeError as e:
            print(f"JSON decode error in {filename}: {str(e)}")
            return []
        except Exception as e:
            print(f"Error loading {filename}: {str(e)}")
            return []
    
    def save_json_data(self, filename, data):
        """Lưu dữ liệu vào file JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False
    
    def create_login_window(self):
        """Tạo cửa sổ đăng nhập"""
        # Clear main window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Center frame
        login_frame = tk.Frame(self.root, bg='white', padx=40, pady=40)
        login_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title
        title_label = tk.Label(login_frame, text="QUẢN LÝ SHOP QUẦN ÁO", 
                              font=('Arial', 20, 'bold'), bg='white', fg='#2c3e50')
        title_label.pack(pady=(0, 30))
        
        # Username
        tk.Label(login_frame, text="Tên đăng nhập:", font=('Arial', 12), bg='white').pack(anchor='w')
        self.username_entry = tk.Entry(login_frame, font=('Arial', 12), width=25)
        self.username_entry.pack(pady=(5, 15))
        
        # Password
        tk.Label(login_frame, text="Mật khẩu:", font=('Arial', 12), bg='white').pack(anchor='w')
        self.password_entry = tk.Entry(login_frame, font=('Arial', 12), width=25, show='*')
        self.password_entry.pack(pady=(5, 20))
        
        # Buttons
        btn_frame = tk.Frame(login_frame, bg='white')
        btn_frame.pack()
        
        login_btn = tk.Button(btn_frame, text="Đăng nhập", command=self.login,
                             bg='#3498db', fg='white', font=('Arial', 12), width=12, pady=5)
        login_btn.pack(side='left', padx=(0, 10))
        
        register_btn = tk.Button(btn_frame, text="Đăng ký", command=self.show_register_dialog,
                               bg='#2ecc71', fg='white', font=('Arial', 12), width=12, pady=5)
        register_btn.pack(side='left')
        
        # Default credentials info
        info_frame = tk.Frame(login_frame, bg='white')
        info_frame.pack(pady=(20, 0))
        
        #tk.Label(info_frame, text="Tài khoản mặc định:", font=('Arial', 10, 'bold'), bg='white').pack()
        #tk.Label(info_frame, text="Admin: admin/admin123", font=('Arial', 9), bg='white', fg='#7f8c8d').pack()
        #tk.Label(info_frame, text="User: user/user123", font=('Arial', 9), bg='white', fg='#7f8c8d').pack()
        
        # Bind Enter key to login
        self.username_entry.bind('<Return>', lambda e: self.login())
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Focus on username entry
        self.username_entry.focus_set()
    
    def login(self):
        """Xử lý đăng nhập"""
        try:
            username = self.username_entry.get().strip()
            password = self.password_entry.get().strip()
            
            print(f"Attempting login with username: {username}")  # Debug
            
            if not username or not password:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            users = self.load_json_data(self.users_file)
            print(f"Loaded {len(users)} users from file")  # Debug
            
            hashed_password = self.hash_password(password)
            print(f"Hashed password: {hashed_password}")  # Debug
            
            for user in users:
                print(f"Checking user: {user['username']}, stored hash: {user['password']}")  # Debug
                if user['username'] == username and user['password'] == hashed_password:
                    self.current_user = username
                    self.is_admin = (user['role'] == 'admin')
                    print(f"Login successful for {username}, admin: {self.is_admin}")  # Debug
                    self.create_main_window()
                    return
            
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")
            
        except Exception as e:
            print(f"Login error: {str(e)}")  # Debug
            messagebox.showerror("Lỗi", f"Lỗi đăng nhập: {str(e)}")
    
    def show_register_dialog(self):
        """Hiển thị dialog đăng ký"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Đăng ký tài khoản")
        dialog.geometry("400x300")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        frame = tk.Frame(dialog, bg='white', padx=20, pady=20)
        frame.pack(fill='both', expand=True)
        
        tk.Label(frame, text="Đăng ký tài khoản mới", font=('Arial', 16, 'bold'), bg='white').pack(pady=(0, 20))
        
        # Username
        tk.Label(frame, text="Tên đăng nhập:", font=('Arial', 12), bg='white').pack(anchor='w')
        username_entry = tk.Entry(frame, font=('Arial', 12), width=30)
        username_entry.pack(pady=(5, 10))
        
        # Password
        tk.Label(frame, text="Mật khẩu:", font=('Arial', 12), bg='white').pack(anchor='w')
        password_entry = tk.Entry(frame, font=('Arial', 12), width=30, show='*')
        password_entry.pack(pady=(5, 10))
        
        # Confirm Password
        tk.Label(frame, text="Xác nhận mật khẩu:", font=('Arial', 12), bg='white').pack(anchor='w')
        confirm_entry = tk.Entry(frame, font=('Arial', 12), width=30, show='*')
        confirm_entry.pack(pady=(5, 20))
        
        def register():
            username = username_entry.get()
            password = password_entry.get()
            confirm = confirm_entry.get()
            
            if not username or not password or not confirm:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            if password != confirm:
                messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
                return
            
            if len(password) < 6:
                messagebox.showerror("Lỗi", "Mật khẩu phải có ít nhất 6 ký tự!")
                return
            
            users = self.load_json_data(self.users_file)
            
            # Check if username exists
            for user in users:
                if user['username'] == username:
                    messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại!")
                    return
            
            # Add new user
            new_user = {
                "username": username,
                "password": self.hash_password(password),
                "role": "user",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            users.append(new_user)
            
            if self.save_json_data(self.users_file, users):
                messagebox.showinfo("Thành công", "Đăng ký thành công!")
                dialog.destroy()
            else:
                messagebox.showerror("Lỗi", "Không thể lưu thông tin đăng ký!")
        
        btn_frame = tk.Frame(frame, bg='white')
        btn_frame.pack()
        
        tk.Button(btn_frame, text="Đăng ký", command=register,
                 bg='#2ecc71', fg='white', font=('Arial', 12), width=10, pady=5).pack(side='left', padx=(0, 10))
        tk.Button(btn_frame, text="Hủy", command=dialog.destroy,
                 bg='#e74c3c', fg='white', font=('Arial', 12), width=10, pady=5).pack(side='left')
    
    def create_main_window(self):
        """Tạo cửa sổ chính"""
        # Clear login window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#2c3e50', height=60)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Title and user info
        title_label = tk.Label(header_frame, text="QUẢN LÝ SHOP QUẦN ÁO", 
                              font=('Arial', 18, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(side='left', padx=20, pady=15)
        
        user_info = f"Xin chào, {self.current_user} ({'Quản trị viên' if self.is_admin else 'Người dùng'})"
        user_label = tk.Label(header_frame, text=user_info, 
                             font=('Arial', 12), bg='#2c3e50', fg='white')
        user_label.pack(side='right', padx=20, pady=15)
        
        # Content frame
        content_frame = tk.Frame(main_frame, bg='#f0f0f0')
        content_frame.pack(fill='both', expand=True)
        
        # Left panel - Controls
        left_panel = tk.Frame(content_frame, bg='white', width=300)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Right panel - Product list
        right_panel = tk.Frame(content_frame, bg='white')
        right_panel.pack(side='right', fill='both', expand=True)
        
        self.create_control_panel(left_panel)
        self.create_product_list(right_panel)
        
        # Load initial data
        self.load_products()
        
        # Add logout button
        logout_btn = tk.Button(header_frame, text="Đăng xuất", command=self.logout,
                              bg='#e74c3c', fg='white', font=('Arial', 10), pady=5)
        logout_btn.pack(side='right', padx=(0, 20), pady=15)
    
    def create_control_panel(self, parent):
        """Tạo panel điều khiển"""
        # Title
        tk.Label(parent, text="ĐIỀU KHIỂN", font=('Arial', 14, 'bold'), 
                bg='white', fg='#2c3e50').pack(pady=20)
        
        # Product form
        form_frame = tk.LabelFrame(parent, text="Thông tin sản phẩm", 
                                  font=('Arial', 12, 'bold'), bg='white')
        form_frame.pack(fill='x', padx=20, pady=10)
        
        # Form fields
        tk.Label(form_frame, text="Tên sản phẩm:", bg='white').pack(anchor='w', padx=10, pady=(10, 0))
        self.name_entry = tk.Entry(form_frame, font=('Arial', 10), width=25)
        self.name_entry.pack(padx=10, pady=(5, 10))
        
        tk.Label(form_frame, text="Loại:", bg='white').pack(anchor='w', padx=10)
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(form_frame, textvariable=self.category_var, 
                                     values=['Áo', 'Quần', 'Váy', 'Phụ kiện'], width=22)
        category_combo.pack(padx=10, pady=(5, 10))
        
        tk.Label(form_frame, text="Giá:", bg='white').pack(anchor='w', padx=10)
        self.price_entry = tk.Entry(form_frame, font=('Arial', 10), width=25)
        self.price_entry.pack(padx=10, pady=(5, 10))
        
        tk.Label(form_frame, text="Số lượng:", bg='white').pack(anchor='w', padx=10)
        self.quantity_entry = tk.Entry(form_frame, font=('Arial', 10), width=25)
        self.quantity_entry.pack(padx=10, pady=(5, 10))
        
        tk.Label(form_frame, text="Mô tả:", bg='white').pack(anchor='w', padx=10)
        self.description_text = tk.Text(form_frame, height=3, width=25, font=('Arial', 10))
        self.description_text.pack(padx=10, pady=(5, 15))
        
        # Buttons
        btn_frame = tk.Frame(parent, bg='white')
        btn_frame.pack(fill='x', padx=20, pady=10)
        
        if self.is_admin:
            tk.Button(btn_frame, text="Thêm sản phẩm", command=self.add_product,
                     bg='#2ecc71', fg='white', font=('Arial', 10), width=15).pack(pady=5)
            tk.Button(btn_frame, text="Cập nhật", command=self.update_product,
                     bg='#f39c12', fg='white', font=('Arial', 10), width=15).pack(pady=5)
            tk.Button(btn_frame, text="Xóa sản phẩm", command=self.delete_product,
                     bg='#e74c3c', fg='white', font=('Arial', 10), width=15).pack(pady=5)
            tk.Button(btn_frame, text="Lấy dữ liệu API", command=self.fetch_api_data,
                     bg='#9b59b6', fg='white', font=('Arial', 10), width=15).pack(pady=5)
            #tk.Button(btn_frame, text="Đọc dữ liệu", command=self.load_custom_json_data,
                     #bg='#1abc9c', fg='white', font=('Arial', 10), width=15).pack(pady=5)
        
        tk.Button(btn_frame, text="Làm mới", command=self.load_products,
                 bg='#3498db', fg='white', font=('Arial', 10), width=15).pack(pady=5)
        
        # Search
        search_frame = tk.LabelFrame(parent, text="Tìm kiếm", font=('Arial', 12, 'bold'), bg='white')
        search_frame.pack(fill='x', padx=20, pady=10)
        
        self.search_entry = tk.Entry(search_frame, font=('Arial', 10), width=25)
        self.search_entry.pack(padx=10, pady=10)
        self.search_entry.bind('<KeyRelease>', self.search_products)
    
    def create_product_list(self, parent):
        """Tạo danh sách sản phẩm"""
        tk.Label(parent, text="DANH SÁCH SẢN PHẨM", font=('Arial', 14, 'bold'), 
                bg='white', fg='#2c3e50').pack(pady=20)
        
        # Treeview
        tree_frame = tk.Frame(parent, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        columns = ('ID', 'Tên sản phẩm', 'Loại', 'Giá', 'Số lượng', 'Mô tả')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Column headings
        for col in columns:
            self.tree.heading(col, text=col)
            if col == 'ID':
                self.tree.column(col, width=50)
            elif col == 'Tên sản phẩm':
                self.tree.column(col, width=200)
            elif col == 'Loại':
                self.tree.column(col, width=100)
            elif col == 'Giá':
                self.tree.column(col, width=100)
            elif col == 'Số lượng':
                self.tree.column(col, width=100)
            else:
                self.tree.column(col, width=150)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack
        self.tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind selection
        self.tree.bind('<<TreeviewSelect>>', self.on_select_product)
    
    def load_products(self):
        """Tải danh sách sản phẩm"""
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        products = self.load_json_data(self.products_file)
        
        for i, product in enumerate(products, 1):
            self.tree.insert('', 'end', values=(
                i,
                product.get('name', ''),
                product.get('category', ''),
                f"{product.get('price', 0):,} VNĐ",
                product.get('quantity', 0),
                product.get('description', '')[:50] + '...' if len(product.get('description', '')) > 50 else product.get('description', '')
            ))
    
    def on_select_product(self, event):
        """Xử lý khi chọn sản phẩm"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            if values:
                # Load product data
                products = self.load_json_data(self.products_file)
                product_index = int(values[0]) - 1
                
                if 0 <= product_index < len(products):
                    product = products[product_index]
                    
                    # Fill form
                    self.name_entry.delete(0, tk.END)
                    self.name_entry.insert(0, product.get('name', ''))
                    
                    self.category_var.set(product.get('category', ''))
                    
                    self.price_entry.delete(0, tk.END)
                    self.price_entry.insert(0, str(product.get('price', '')))
                    
                    self.quantity_entry.delete(0, tk.END)
                    self.quantity_entry.insert(0, str(product.get('quantity', '')))
                    
                    self.description_text.delete(1.0, tk.END)
                    self.description_text.insert(1.0, product.get('description', ''))
    
    def add_product(self):
        """Thêm sản phẩm mới"""
        if not self.is_admin:
            messagebox.showerror("Lỗi", "Bạn không có quyền thực hiện chức năng này!")
            return
        
        name = self.name_entry.get().strip()
        category = self.category_var.get().strip()
        price_str = self.price_entry.get().strip()
        quantity_str = self.quantity_entry.get().strip()
        description = self.description_text.get(1.0, tk.END).strip()
        
        if not name or not category or not price_str or not quantity_str:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        try:
            price = float(price_str)
            quantity = int(quantity_str)
        except ValueError:
            messagebox.showerror("Lỗi", "Giá và số lượng phải là số!")
            return
        
        if price < 0 or quantity < 0:
            messagebox.showerror("Lỗi", "Giá và số lượng phải là số dương!")
            return
        
        products = self.load_json_data(self.products_file)
        
        new_product = {
            "name": name,
            "category": category,
            "price": price,
            "quantity": quantity,
            "description": description,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "created_by": self.current_user
        }
        
        products.append(new_product)
        
        if self.save_json_data(self.products_file, products):
            messagebox.showinfo("Thành công", "Thêm sản phẩm thành công!")
            self.clear_form()
            self.load_products()
        else:
            messagebox.showerror("Lỗi", "Không thể lưu sản phẩm!")
    
    def update_product(self):
        """Cập nhật sản phẩm"""
        if not self.is_admin:
            messagebox.showerror("Lỗi", "Bạn không có quyền thực hiện chức năng này!")
            return
        
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Lỗi", "Vui lòng chọn sản phẩm cần cập nhật!")
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        product_index = int(values[0]) - 1
        
        name = self.name_entry.get().strip()
        category = self.category_var.get().strip()
        price_str = self.price_entry.get().strip()
        quantity_str = self.quantity_entry.get().strip()
        description = self.description_text.get(1.0, tk.END).strip()
        
        if not name or not category or not price_str or not quantity_str:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        try:
            price = float(price_str)
            quantity = int(quantity_str)
        except ValueError:
            messagebox.showerror("Lỗi", "Giá và số lượng phải là số!")
            return
        
        if price < 0 or quantity < 0:
            messagebox.showerror("Lỗi", "Giá và số lượng phải là số dương!")
            return
        
        products = self.load_json_data(self.products_file)
        
        if 0 <= product_index < len(products):
            products[product_index].update({
                "name": name,
                "category": category,
                "price": price,
                "quantity": quantity,
                "description": description,
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updated_by": self.current_user
            })
            
            if self.save_json_data(self.products_file, products):
                messagebox.showinfo("Thành công", "Cập nhật sản phẩm thành công!")
                self.load_products()
            else:
                messagebox.showerror("Lỗi", "Không thể cập nhật sản phẩm!")
    
    def delete_product(self):
        """Xóa sản phẩm"""
        if not self.is_admin:
            messagebox.showerror("Lỗi", "Bạn không có quyền thực hiện chức năng này!")
            return
        
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Lỗi", "Vui lòng chọn sản phẩm cần xóa!")
            return
        
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sản phẩm này?"):
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        product_index = int(values[0]) - 1
        
        products = self.load_json_data(self.products_file)
        
        if 0 <= product_index < len(products):
            products.pop(product_index)
            
            if self.save_json_data(self.products_file, products):
                messagebox.showinfo("Thành công", "Xóa sản phẩm thành công!")
                self.clear_form()
                self.load_products()
            else:
                messagebox.showerror("Lỗi", "Không thể xóa sản phẩm!")
                
    def load_custom_json_data(self):
        """Load dữ liệu từ file JSON tùy chỉnh và hiển thị lên giao diện"""
        filename = 'products_load.json'  
        
        if not os.path.exists(filename):
            messagebox.showerror("Lỗi", f"Không tìm thấy file {filename}")
            return
        
        try:
            with open(filename, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
            
            # Xóa dữ liệu cũ trong Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Thêm dữ liệu mới
            for i, product in enumerate(data, 1):
                self.tree.insert('', 'end', values=(
                    i,
                    product.get('name', ''),
                    product.get('category', ''),
                    f"{product.get('price', 0):,} VNĐ",
                    product.get('quantity', 0),
                    product.get('description', '')[:50] + '...' if len(product.get('description', '')) > 50 else product.get('description', '')
                ))
            
            messagebox.showinfo("Thành công", "Đã load dữ liệu từ file JSON!")
        
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc dữ liệu: {str(e)}")

    

    def fetch_api_data(self):
        """Lấy dữ liệu từ API giả lập - tự phát sinh sản phẩm"""
        if not self.is_admin:
            messagebox.showerror("Lỗi", "Bạn không có quyền thực hiện chức năng này!")
            return
        
        def fetch_data():
            try:
                # Giả lập thời gian xử lý API
                import time
                time.sleep(2)  # Giả lập thời gian chờ API
                
                # Dữ liệu mẫu để tạo sản phẩm
                product_names = [
                    "Áo thun nam basic", "Áo sơ mi nữ công sở", "Quần jean nam slim fit",
                    "Váy midi hoa nhí", "Áo khoác bomber", "Quần short thể thao",
                    "Đầm maxi bohemian", "Áo polo nam", "Chân váy chữ A",
                    "Áo hoodie unisex", "Quần tây nữ", "Áo croptop nữ",
                    "Quần jogger nam", "Váy suông tay dài", "Áo blazer nữ"
                ]
                
                categories = ['Áo', 'Quần', 'Váy', 'Phụ kiện', 'Đồ thể thao']
                
                colors = ['Đen', 'Trắng', 'Xanh', 'Đỏ', 'Vàng', 'Hồng', 'Xám', 'Nâu']
                
                brands = ['Nike', 'Adidas', 'Zara', 'H&M', 'Uniqlo', 'Local Brand', 'Fashion House']
                
                descriptions = [
                    "Chất liệu cotton cao cấp, thoáng mát",
                    "Thiết kế hiện đại, phù hợp nhiều dáng người",
                    "Form dáng chuẩn, dễ phối đồ",
                    "Màu sắc trẻ trung, năng động",
                    "Chất lượng tốt, giá cả hợp lý",
                    "Xu hướng thời trang mới nhất",
                    "Phong cách Hàn Quốc",
                    "Thiết kế tối giản, thanh lịch"
                ]
                
                import random
                
                products = self.load_json_data(self.products_file)
                
                # Tạo 8 sản phẩm ngẫu nhiên
                api_products = []
                for i in range(8):
                    base_name = random.choice(product_names)
                    color = random.choice(colors)
                    brand = random.choice(brands)
                    
                    new_product = {
                        "name": f"{base_name} {color} - {brand}",
                        "category": random.choice(categories),
                        "price": random.randint(89000, 899000),  # Giá từ 89k-899k
                        "quantity": random.randint(5, 50),  # Số lượng 5-50
                        "description": f"{random.choice(descriptions)}. Size: S, M, L, XL",
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "created_by": self.current_user,
                        "source": "API_Generated",
                        "brand": brand,
                        "color": color,
                        "sku": f"API-{random.randint(10000, 99999)}"
                    }
                    
                    # Điều chỉnh category dựa trên tên sản phẩm
                    if "áo" in base_name.lower():
                        new_product["category"] = "Áo"
                    elif "quần" in base_name.lower():
                        new_product["category"] = "Quần"
                    elif "váy" in base_name.lower() or "đầm" in base_name.lower():
                        new_product["category"] = "Váy"
                    elif "short" in base_name.lower() or "jogger" in base_name.lower():
                        new_product["category"] = "Đồ thể thao"
                    
                    api_products.append(new_product)
                    products.append(new_product)
                
                if self.save_json_data(self.products_file, products):
                    self.root.after(0, lambda: messagebox.showinfo("Thành công", 
                                                                  f"Đã thêm {len(api_products)} sản phẩm từ API giả lập!\n"
                                                                  f"Tổng cộng: {len(products)} sản phẩm"))
                    self.root.after(0, self.load_products)
                else:
                    self.root.after(0, lambda: messagebox.showerror("Lỗi", "Không thể lưu dữ liệu!"))
            
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Lỗi", f"Lỗi xử lý dữ liệu: {str(e)}"))
        messagebox.showinfo("Thông báo", "Đang kết nối và lấy dữ liệu từ API...")
        thread = threading.Thread(target=fetch_data)
        thread.daemon = True
        thread.start()
    def search_products(self, event=None):
        """Tìm kiếm sản phẩm"""
        search_term = self.search_entry.get().lower().strip()
        
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        products = self.load_json_data(self.products_file)
        
        filtered_products = []
        if search_term:
            for product in products:
                if (search_term in product.get('name', '').lower() or
                    search_term in product.get('category', '').lower() or
                    search_term in product.get('description', '').lower()):
                    filtered_products.append(product)
        else:
            filtered_products = products
        
        for i, product in enumerate(filtered_products, 1):
            self.tree.insert('', 'end', values=(
                i,
                product.get('name', ''),
                product.get('category', ''),
                f"{product.get('price', 0):,} VNĐ",
                product.get('quantity', 0),
                product.get('description', '')[:50] + '...' if len(product.get('description', '')) > 50 else product.get('description', '')
            ))
    
    def clear_form(self):
        """Xóa form nhập liệu"""
        self.name_entry.delete(0, tk.END)
        self.category_var.set('')
        self.price_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.description_text.delete(1.0, tk.END)
    
    def logout(self):
        """Đăng xuất"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất?"):
            self.current_user = None
            self.is_admin = False
            self.create_login_window()
    
    def run(self):
        """Chạy ứng dụng"""
        self.root.mainloop()

# File setup.py để đóng gói ứng dụng
def create_setup_file():
    setup_content = '''
from cx_Freeze import setup, Executable
import sys

# Thêm các file cần thiết
build_exe_options = {
    "packages": ["tkinter", "json", "os", "hashlib", "requests", "datetime", "threading"],
    "excludes": ["unittest"],
    "include_files": [],
}

# Thiết lập cho Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="ClothingShopManager",
    version="1.0",
    description="Ứng dụng Quản lý Shop Quần Áo",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main.py",
            base=base,
            target_name="QuanLyShopQuanAo.exe",
            icon=None
        )
    ],
)
'''
    
    with open('setup.py', 'w', encoding='utf-8') as f:
        f.write(setup_content.strip())

# File requirements.txt
def create_requirements_file():
    requirements = '''
requests>=2.25.1
cx-Freeze>=6.8
'''
    
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements.strip())

# File README.md
def create_readme_file():
    readme_content = '''
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
'''
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content.strip())

if __name__ == "__main__":
    # Tạo các file hỗ trợ
    create_setup_file()
    create_requirements_file() 
    create_readme_file()
    
    # Chạy ứng dụng
    app = ClothingShopManager()
    app.run()