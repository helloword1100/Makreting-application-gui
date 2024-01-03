from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox
import qrcode
import cv2
from datetime import datetime

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Marketing Application")
        self.root.config(bg="#f5f5f5")

        # Title
        title_frame = Frame(self.root, bg="#394240", bd=5)
        title_frame.place(relx=0, rely=0, relwidth=1, height=70)

        title_label = Label(title_frame, text="Marketing Application", font=("Helvetica", 24, "bold"),
                            bg="#394240", fg="white", padx=20)
        title_label.pack(side=LEFT, fill=BOTH)

        # Signup and Login Buttons
        btn_frame = Frame(self.root, bg="#394240")
        btn_frame.place(relx=0.75, rely=0, relwidth=0.25, height=70)

        btn_signup = Button(btn_frame, text="Signup", font=("Helvetica", 14, "bold"),
                            bg="#ffd700", fg="#394240", cursor="hand2", command=self.signup_window)
        btn_signup.pack(side=LEFT, fill=BOTH)

        btn_login = Button(btn_frame, text="Login", font=("Helvetica", 14, "bold"),
                           bg="#ffd700", fg="#394240", cursor="hand2", command=self.login_window)
        btn_login.pack(side=LEFT, fill=BOTH)

        # Clock
        self.clock_label = Label(self.root, text=self.get_datetime_string(),
                                 font=("Helvetica", 12), bg="#4d636d", fg="white")
        self.clock_label.place(relx=0, rely=0.1, relwidth=1, height=30)

        # Left Menu
        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="#394240")
        LeftMenu.place(relx=0, rely=0.15, relwidth=0.15, relheight=0.8)

        # Search
        search_frame = Frame(LeftMenu, bg="#394240")
        search_frame.pack(side=TOP, fill=X)

        query_label = Label(search_frame, text='Query', font=("Helvetica", 12, 'bold'), bg="#394240", fg="white")
        query_label.pack(side=TOP, fill=X)

        self.question_field = Entry(search_frame, font=("Helvetica", 12), bd=4, relief=SUNKEN)
        self.question_field.pack(side=TOP, fill=X)

        search_button = Button(search_frame, text="Search", font=("Helvetica", 12, "bold"), bg="#ffd700", command=self.search_items)
        search_button.pack(side=TOP, fill=X)

        # Menu
        menu_label = Label(LeftMenu, text="Menu", font=("Helvetica", 16, "bold"), bg="#394240", fg="white")
        menu_label.pack(side=TOP, fill=X)

        # Promotion Categories
        btn_promotion = Button(LeftMenu, text="Promotion", font=("Helvetica", 12, "bold"),
                               bg="#4caf50", fg="white", cursor="hand2", command=self.show_promotion_categories)
        btn_promotion.pack(side=TOP, fill=X)

        self.promo_frame = Frame(LeftMenu, bg="#394240")  # Frame to hold the promotion categories
        self.discount_btn = Button(self.promo_frame, text="Discount", font=("Helvetica", 12, "bold"),
                                   bg="#4caf50", fg="white", cursor="hand2", command=lambda: self.show_promotions('Discount'))
        self.discount_btn.pack(side=TOP, fill=X)

        self.promotion_btn = Button(self.promo_frame, text="Promotion", font=("Helvetica", 12, "bold"),
                                    bg="#4caf50", fg="white", cursor="hand2", command=lambda: self.show_promotions('Promotion'))
        self.promotion_btn.pack(side=TOP, fill=X)

        self.promo_frame.pack_forget()  
        # Button for QR Code Generation
        btn_generate_qr = Button(LeftMenu, text="Generate QR Code", font=("Helvetica", 12, "bold"),
                                 bg="#4caf50", fg="white", cursor="hand2", command=self.generate_qr)
        btn_generate_qr.pack(side=TOP, fill=X)

        # Button for QR Code Scanning
        btn_scan_qr = Button(LeftMenu, text="Scan QR Code", font=("Helvetica", 12, "bold"),
                             bg="#2196f3", fg="white", cursor="hand2", command=self.scan_qr)
        btn_scan_qr.pack(side=TOP, fill=X)

        # Menu Footer
        menu_footer = Label(LeftMenu, text="Marketing Application", font=("Helvetica", 12),
                            bg="#394240", fg="white")
        menu_footer.pack(side=BOTTOM, fill=X)

        # Footer
        lbl_footer = Label(self.root, text="Marketing Application", font=("Helvetica", 12),
                           bg="#394240", fg="white")
        lbl_footer.place(relx=0, rely=0.95, relwidth=1, height=30)

    def show_promotion_categories(self):
       
        if self.promo_frame.winfo_ismapped():
            self.promo_frame.pack_forget()
        else:
            self.promo_frame.pack(side=TOP, fill=X)

    def show_promotions(self, category):
       
        print(f"Show promotions for category: {category}")

    def search_items(self):
        query = self.question_field.get().lower()

        
        for widget in self.promo_frame.winfo_children():
            widget.destroy()

        matching_categories = [category for category in ['Discount', 'Promotion'] if query in category.lower()]

        if matching_categories:
            for category in matching_categories:
                btn_category = Button(self.promo_frame, text=category, font=("Helvetica", 12, "bold"),
                                      bg="#4caf50", fg="white", cursor="hand2", command=lambda c=category: self.show_promotions(c))
                btn_category.pack(side=TOP, fill=X)

            # Show the updated promotion frame
            self.promo_frame.pack(side=TOP, fill=X)
            messagebox.showinfo("Found", f"Found: {matching_categories}")
        else:
            messagebox.showinfo("Not Found", "No matching items found.")

    def signup_window(self):
        signup_window = Toplevel(self.root)
        signup_window.title("Signup")
        signup_window.geometry("400x250")
        signup_window.config(bg="#f5f5f5")

        lbl_username = Label(signup_window, text="Username:", font=("Helvetica", 14), bg="#f5f5f5")
        lbl_username.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        entry_username = Entry(signup_window, font=("Helvetica", 14))
        entry_username.grid(row=0, column=1, padx=10, pady=10)

        lbl_password = Label(signup_window, text="Password:", font=("Helvetica", 14), bg="#f5f5f5")
        lbl_password.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        entry_password = Entry(signup_window, show="*", font=("Helvetica", 14))
        entry_password.grid(row=1, column=1, padx=10, pady=10)

        lbl_age = Label(signup_window, text="Age:", font=("Helvetica", 14), bg="#f5f5f5")
        lbl_age.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        entry_age = Entry(signup_window, font=("Helvetica", 14))
        entry_age.grid(row=2, column=1, padx=10, pady=10)

        btn_submit = Button(signup_window, text="Submit", font=("Helvetica", 14), bg="#4caf50", fg="white",
                            command=lambda: self.submit_signup(entry_username, entry_password, entry_age, signup_window))
        btn_submit.grid(row=3, column=0, columnspan=2, pady=10)

    def login_window(self):
        login_window = Toplevel(self.root)
        login_window.title("Login")
        login_window.geometry("400x200")
        login_window.config(bg="#f5f5f5")

        lbl_username = Label(login_window, text="Username:", font=("Helvetica", 14), bg="#f5f5f5")
        lbl_username.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        entry_username = Entry(login_window, font=("Helvetica", 14))
        entry_username.grid(row=0, column=1, padx=10, pady=10)

        lbl_password = Label(login_window, text="Password:", font=("Helvetica", 14), bg="#f5f5f5")
        lbl_password.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        entry_password = Entry(login_window, show="*", font=("Helvetica", 14))
        entry_password.grid(row=1, column=1, padx=10, pady=10)

        btn_submit = Button(login_window, text="Submit", font=("Helvetica", 14), bg="#2196f3", fg="white",
                            command=lambda: self.submit_login(entry_username, entry_password, login_window))
        btn_submit.grid(row=2, column=0, columnspan=2, pady=10)

    def submit_signup(self, entry_username, entry_password, entry_age, signup_window):
        try:
            age = int(entry_age.get())
            if age > 18:
                connection = sqlite3.connect("gui.db")
                cursor = connection.cursor()

               
                cursor.execute('''CREATE TABLE IF NOT EXISTS signup (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    username TEXT NOT NULL,
                                    password TEXT NOT NULL
                                 )''')

               
                cursor.execute("INSERT INTO signup (username, password) VALUES (?, ?)",
                               (entry_username.get(), entry_password.get()))
                connection.commit()
                connection.close()

                messagebox.showinfo("Success", "Signup successful!")
                signup_window.destroy()
            else:
                messagebox.showerror("Error", "You must be 18 years or older to create an account.")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid age.")

        except Exception as e:
            messagebox.showerror("Error", f"Error during signup: {e}")

    def submit_login(self, entry_username, entry_password, login_window):
        try:
            connection = sqlite3.connect("gui.db")
            cursor = connection.cursor()

           
            cursor.execute("SELECT * FROM signup WHERE username=? AND password=?",
                           (entry_username.get(), entry_password.get()))
            user_data = cursor.fetchone()

            if user_data:
                messagebox.showinfo("Success", "Login successful!")
            else:
                messagebox.showerror("Error", "Invalid username or password. Please sign up.")

            connection.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error during login: {e}")

    def generate_qr(self):
        qr_data = "promotion 2k24 granted" 
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        qr_img.save("promotion_qr.png")  

        messagebox.showinfo("QR Code Generated", "QR Code generated successfully and saved as 'promotion_qr.png'!")

    def scan_qr(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()

            if not ret:
                messagebox.showerror("Error", "Failed to capture video. Please try again.")
                break

            detector = cv2.QRCodeDetector()
            retval, decoded_info, points, straight_qrcode = detector.detectAndDecode(frame)

            if retval:
                messagebox.showinfo("QR Code Scanned", f"QR Code contains: {decoded_info}")
                break

            cv2.imshow("QR Code Scanner", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def get_datetime_string(self):
        
        now = datetime.now()
        formatted_date_time = now.strftime("Welcome to Marketing Application\t\t Date: %b %d, %Y\t\t Time: %H:%M:%S")
        return formatted_date_time


root = Tk()
obj = IMS(root)
root.mainloop()
