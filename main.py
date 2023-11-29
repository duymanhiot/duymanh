import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import threading

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng Dụng Xử Lý Ảnh")
        self.root.configure(bg="#F0F0F0")  # Background color

        self.image_path = None
        self.kernel_size = 5
        self.gamma = 1.5  # Giá trị gamma mặc định
        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("Lọc trung vị")  # Giá trị mặc định

        self.create_widgets()

    def apply_noise_reduction(self):
        image = cv2.imread(self.image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.GaussianBlur(gray_image, (self.kernel_size, self.kernel_size), 0)

        # Hiển thị ảnh gốc và ảnh được xử lý cạt nhiễu
        self.display_images(gray_image, "Ảnh Gốc", blurred_image, "Ảnh Đã Xử Lý (Cạt Nhiễu)")

    def apply_contrast(self):
        image = cv2.imread(self.image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced_image = clahe.apply(gray_image)

        # Hiển thị ảnh gốc và ảnh được tăng cường độ tương phản
        self.display_images(gray_image, "Ảnh Gốc", enhanced_image, "Ảnh Đã Xử Lý (Tăng Cường Độ Tương Phản)")

    def apply_stretch(self):
        image = cv2.imread(self.image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        stretched_image = np.power(gray_image / float(np.max(gray_image)), self.gamma) * 255.0
        stretched_image = np.uint8(stretched_image)

        # Hiển thị ảnh gốc và ảnh được dãn
        self.display_images(gray_image, "Ảnh Gốc", stretched_image, "Ảnh Đã Xử Lý (Dãn Ảnh)")

    def apply_max_filter(self):
        image = cv2.imread(self.image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        max_filtered_image = cv2.dilate(gray_image, np.ones((self.kernel_size, self.kernel_size), np.uint8))

        # Hiển thị ảnh gốc và ảnh được lọc tối đa
        self.display_images(gray_image, "Ảnh Gốc", max_filtered_image, "Ảnh Lọc Tối Đa")

    def apply_min_filter(self):
        image = cv2.imread(self.image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        min_filtered_image = cv2.erode(gray_image, np.ones((self.kernel_size, self.kernel_size), np.uint8))

        # Hiển thị ảnh gốc và ảnh được lọc tối thiểu
        self.display_images(gray_image, "Ảnh Gốc", min_filtered_image, "Ảnh Lọc Tối Thiểu")

    def apply_midpoint_filter(self):
        image = cv2.imread(self.image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        max_filtered_image = cv2.dilate(gray_image, np.ones((self.kernel_size, self.kernel_size), np.uint8))
        min_filtered_image = cv2.erode(gray_image, np.ones((self.kernel_size, self.kernel_size), np.uint8))
        midpoint_filtered_image = (max_filtered_image + min_filtered_image) // 2

        # Hiển thị ảnh gốc và ảnh được lọc trung điểm
        self.display_images(gray_image, "Ảnh Gốc", midpoint_filtered_image, "Ảnh Lọc Trung Điểm")

    def apply_Mean_filter(self):
        image = cv2.imread(self.image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        filtered_image = cv2.blur(gray_image, (self.kernel_size, self.kernel_size))

        # Hiển thị ảnh gốc và ảnh được lọc trung bình
        self.display_images(gray_image, "Ảnh Gốc", filtered_image, "Ảnh Đã Lọc (Lọc Trung Bình)")

    def create_widgets(self):
        # Frame để chứa các widget
        main_frame = tk.Frame(self.root, padx=20, pady=20, bg="#F0F0F0")  # Màu nền xám nhạt
        main_frame.pack(expand=True)

        # Nút để chọn ảnh
        select_image_button = tk.Button(main_frame, text="Chọn Ảnh", command=self.select_image, bg="#4CAF50", fg="white")  # Nút màu xanh lá cây
        select_image_button.grid(row=0, column=0, pady=10)

        # Dropdown để chọn thuật toán
        algorithms = ["Lọc trung vị", "Cạt Nhiễu", "Tăng Cường Độ Tương Phản", "Dãn Ảnh", "Lọc Tối Đa và Lọc Tối Thiểu", "Lọc Trung Điểm"]
        algorithm_menu = tk.OptionMenu(main_frame, self.algorithm_var, *algorithms)
        algorithm_menu.config(bg="#4CAF50", fg="white")  # Dropdown màu xanh lá cây
        algorithm_menu.grid(row=0, column=1, pady=10)

        # Nút để xử lý ảnh
        process_button = tk.Button(main_frame, text="Xử Lý Ảnh", command=self.process_image, bg="#008CBA", fg="white")  # Nút màu xanh dương
        process_button.grid(row=0, column=2, pady=10)

        # Labels để hiển thị ảnh gốc và ảnh sau khi xử lý
        self.original_label = tk.Label(main_frame, text="Ảnh Gốc", bg="#F0F0F0")
        self.original_label.grid(row=1, column=0, padx=10)

        self.processed_label = tk.Label(main_frame, text="Ảnh Đã Xử Lý", bg="#F0F0F0")
        self.processed_label.grid(row=1, column=1, padx=10)

    def select_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_path = file_path

    def process_image(self):
        if self.image_path:
            algorithm = self.algorithm_var.get()

            if algorithm == "Lọc trung vị":
                threading.Thread(target=self.apply_median_filter).start()
            elif algorithm == "Cạt Nhiễu":
                threading.Thread(target=self.apply_noise_reduction).start()
            elif algorithm == "Tăng Cường Độ Tương Phản":
                threading.Thread(target=self.apply_contrast).start()
            elif algorithm == "Dãn Ảnh":
                threading.Thread(target=self.apply_stretch).start()
            elif algorithm == "Lọc Tối Đa và Lọc Tối Thiểu":
                threading.Thread(target=self.apply_max_filter).start()
                threading.Thread(target=self.apply_min_filter).start()
            elif algorithm == "Lọc Trung Điểm":
                threading.Thread(target=self.apply_midpoint_filter).start()
            elif algorithm == "Lọc Trung Bình":
                threading.Thread(target=self.apply_Mean_filter).start()

    def display_images(self, image1, title1, image2, title2):
        image_pil1 = Image.fromarray(image1)
        image_tk1 = ImageTk.PhotoImage(image_pil1)

        image_pil2 = Image.fromarray(image2)
        image_tk2 = ImageTk.PhotoImage(image_pil2)

        # Cập nhật các label để hiển thị ảnh
        self.original_label.config(image=image_tk1)
        self.original_label.image = image_tk1
        self.original_label.configure(text=title1, compound='top')

        self.processed_label.config(image=image_tk2)
        self.processed_label.image = image_tk2
        self.processed_label.configure(text=title2, compound='top')

def main():
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
