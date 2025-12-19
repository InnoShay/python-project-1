
from tkinter import *
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import webbrowser
import os
import json
import hashlib
import random
import warnings

warnings.filterwarnings("ignore")


class MovieStreamingApp:
    def __init__(self, root):
        self.root = root

        # files and dirs
        self.data_file = "users.json"
        self.images_dir = "movie_images"

        # load users first (doesn't depend on images_dir)
        self.users = self.load_users()
        self.current_user = None

        # color scheme (kept but not strictly used everywhere)
        self.colors = {
            'bg': '#0a0a0a',
            'card_bg': '#1a1a1a',
            'accent': '#e50914',
            'text': '#ffffff',
            'text_secondary': '#b3b3b3',
        }

        # test PIL and setup image dir + generate posters if missing
        self.test_pil()
        self.setup_images_directory()

        # create UI
        self.create_main_page()

    # ---------------- UI: main / login / register / home ----------------
    def create_main_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title('FROZZLE - Premium Streaming Platform')
        self.root.config(bg=self.colors['bg'])
        self.center_window(1000, 700)

        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)

        welcome_label = tk.Label(main_frame,
                                 text="Welcome to FROZZLE",
                                 font=('Arial', 32, 'bold'),
                                 fg='white',
                                 bg=self.colors['bg'])
        welcome_label.pack(pady=20)

        subtitle_label = tk.Label(main_frame,
                                  text="Premium Streaming Platform",
                                  font=('Arial', 18),
                                  fg=self.colors['text_secondary'],
                                  bg=self.colors['bg'])
        subtitle_label.pack(pady=10)

        button_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        button_frame.pack(pady=50)

        login_btn = tk.Button(button_frame,
                              text="Login",
                              font=('Arial', 16),
                              bg=self.colors['accent'],
                              fg='white',
                              width=15,
                              height=2,
                              command=self.open_login)
        login_btn.pack(side=tk.LEFT, padx=20)

        register_btn = tk.Button(button_frame,
                                 text="Register",
                                 font=('Arial', 16),
                                 bg='#333333',
                                 fg='white',
                                 width=15,
                                 height=2,
                                 command=self.open_register)
        register_btn.pack(side=tk.LEFT, padx=20)

        self.status_label = tk.Label(main_frame,
                                     text="",
                                     font=('Arial', 12),
                                     fg=self.colors['text_secondary'],
                                     bg=self.colors['bg'])
        self.status_label.pack(pady=20)

        self.update_status()

    def open_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title('FROZZLE - Login')
        self.root.config(bg=self.colors['bg'])
        self.center_window(400, 500)

        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        title_label = tk.Label(main_frame,
                               text="Login to FROZZLE",
                               font=('Arial', 24, 'bold'),
                               fg='white',
                               bg=self.colors['bg'])
        title_label.pack(pady=20)

        tk.Label(main_frame, text="Username:", fg='white', bg=self.colors['bg'], font=('Arial', 12)).pack(anchor='w',
                                                                                                         pady=(20, 5))
        username_entry = tk.Entry(main_frame, font=('Arial', 14), width=25)
        username_entry.pack(fill='x', pady=5)

        tk.Label(main_frame, text="Password:", fg='white', bg=self.colors['bg'], font=('Arial', 12)).pack(anchor='w',
                                                                                                         pady=(20, 5))
        password_entry = tk.Entry(main_frame, font=('Arial', 14), width=25, show='*')
        password_entry.pack(fill='x', pady=5)

        login_btn = tk.Button(main_frame,
                              text="Login",
                              font=('Arial', 14),
                              bg=self.colors['accent'],
                              fg='white',
                              width=20,
                              height=2,
                              command=lambda: self.login_user(username_entry.get(), password_entry.get()))
        login_btn.pack(pady=30)

        back_btn = tk.Button(main_frame,
                             text="← Back",
                             font=('Arial', 12),
                             bg='#333333',
                             fg='white',
                             command=self.create_main_page)
        back_btn.pack(pady=10)

    def open_register(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title('FROZZLE - Register')
        self.root.config(bg=self.colors['bg'])
        self.center_window(400, 600)

        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        title_label = tk.Label(main_frame,
                               text="Join FROZZLE",
                               font=('Arial', 24, 'bold'),
                               fg='white',
                               bg=self.colors['bg'])
        title_label.pack(pady=20)

        tk.Label(main_frame, text="Username:", fg='white', bg=self.colors['bg'], font=('Arial', 12)).pack(anchor='w',
                                                                                                          pady=(20, 5))
        username_entry = tk.Entry(main_frame, font=('Arial', 14), width=25)
        username_entry.pack(fill='x', pady=5)

        tk.Label(main_frame, text="Email:", fg='white', bg=self.colors['bg'], font=('Arial', 12)).pack(anchor='w',
                                                                                                       pady=(20, 5))
        email_entry = tk.Entry(main_frame, font=('Arial', 14), width=25)
        email_entry.pack(fill='x', pady=5)

        tk.Label(main_frame, text="Password:", fg='white', bg=self.colors['bg'], font=('Arial', 12)).pack(anchor='w',
                                                                                                           pady=(20, 5))
        password_entry = tk.Entry(main_frame, font=('Arial', 14), width=25, show='*')
        password_entry.pack(fill='x', pady=5)

        tk.Label(main_frame, text="Confirm Password:", fg='white', bg=self.colors['bg'], font=('Arial', 12)).pack(
            anchor='w', pady=(20, 5))
        confirm_password_entry = tk.Entry(main_frame, font=('Arial', 14), width=25, show='*')
        confirm_password_entry.pack(fill='x', pady=5)

        register_btn = tk.Button(main_frame,
                                 text="Create Account",
                                 font=('Arial', 14),
                                 bg=self.colors['accent'],
                                 fg='white',
                                 width=20,
                                 height=2,
                                 command=lambda: self.register_user(
                                     username_entry.get(),
                                     email_entry.get(),
                                     password_entry.get(),
                                     confirm_password_entry.get()
                                 ))
        register_btn.pack(pady=30)

        back_btn = tk.Button(main_frame,
                             text="← Back",
                             font=('Arial', 12),
                             bg='#333333',
                             fg='white',
                             command=self.create_main_page)
        back_btn.pack(pady=10)

    def login_user(self, username, password):
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        if username in self.users:
            hashed_password = self.hash_password(password)
            if self.users[username]['password'] == hashed_password:
                self.current_user = username
                messagebox.showinfo("Success", f"Welcome back, {username}!")
                self.create_home_page()
            else:
                messagebox.showerror("Error", "Invalid password")
        else:
            messagebox.showerror("Error", "Username not found")

    def register_user(self, username, email, password, confirm_password):
        if not all([username, email, password, confirm_password]):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        valid_username, msg = self.validate_username(username)
        if not valid_username:
            messagebox.showerror("Error", msg)
            return

        valid_password, msg = self.validate_password(password)
        if not valid_password:
            messagebox.showerror("Error", msg)
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        if username in self.users:
            messagebox.showerror("Error", "Username already exists")
            return

        self.users[username] = {
            'email': email,
            'password': self.hash_password(password),
            'plan': 'basic'
        }
        self.save_users()
        messagebox.showinfo("Success", "Account created successfully!")
        self.create_main_page()

    def create_home_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        user = self.current_user or "Guest"
        self.root.title(f'FROZZLE - Welcome {user}')
        self.root.config(bg=self.colors['bg'])
        self.center_window(1200, 800)

        header = tk.Frame(self.root, bg='#1a1a1a', height=60)
        header.pack(fill='x', padx=0, pady=0)
        header.pack_propagate(False)

        logo_label = tk.Label(header, text="FROZZLE", font=('Arial', 24, 'bold'),
                              fg=self.colors['accent'], bg='#1a1a1a')
        logo_label.pack(side='left', padx=20, pady=10)

        nav_frame = tk.Frame(header, bg='#1a1a1a')
        nav_frame.pack(side='left', padx=50)

        home_btn = tk.Button(nav_frame, text="Home", font=('Arial', 12),
                             bg='#1a1a1a', fg='white', bd=0,
                             command=self.create_home_page)
        home_btn.pack(side='left', padx=10)

        movies_btn = tk.Button(nav_frame, text="Movies", font=('Arial', 12),
                               bg='#1a1a1a', fg='white', bd=0,
                               command=self.open_movies)
        movies_btn.pack(side='left', padx=10)

        series_btn = tk.Button(nav_frame, text="TV Series", font=('Arial', 12),
                               bg='#1a1a1a', fg='white', bd=0,
                               command=self.open_webseries)
        series_btn.pack(side='left', padx=10)

        user_frame = tk.Frame(header, bg='#1a1a1a')
        user_frame.pack(side='right', padx=20)

        user_label = tk.Label(user_frame, text=f"Welcome, {user}",
                              font=('Arial', 12), fg='white', bg='#1a1a1a')
        user_label.pack(side='left', padx=10)

        logout_btn = tk.Button(user_frame, text="Logout", font=('Arial', 10),
                               bg=self.colors['accent'], fg='white',
                               command=self.logout)
        logout_btn.pack(side='left', padx=5)

        content_frame = tk.Frame(self.root, bg=self.colors['bg'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)

        welcome_section = tk.Frame(content_frame, bg=self.colors['bg'])
        welcome_section.pack(fill='x', pady=20)

        welcome_label = tk.Label(welcome_section,
                                 text=f"Hello, {user}!",
                                 font=('Arial', 28, 'bold'),
                                 fg='white',
                                 bg=self.colors['bg'])
        welcome_label.pack(anchor='w')

        subtitle_label = tk.Label(welcome_section,
                                  text="What would you like to watch today?",
                                  font=('Arial', 16),
                                  fg=self.colors['text_secondary'],
                                  bg=self.colors['bg'])
        subtitle_label.pack(anchor='w', pady=(5, 20))

        quick_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        quick_frame.pack(fill='x', pady=20)

        movies_quick_btn = tk.Button(quick_frame,
                                     text="🎬 Browse Movies",
                                     font=('Arial', 14),
                                     bg=self.colors['accent'],
                                     fg='white',
                                     width=20,
                                     height=2,
                                     command=self.open_movies)
        movies_quick_btn.pack(side='left', padx=10)

        series_quick_btn = tk.Button(quick_frame,
                                     text="📺 Browse Series",
                                     font=('Arial', 14),
                                     bg='#333333',
                                     fg='white',
                                     width=20,
                                     height=2,
                                     command=self.open_webseries)
        series_quick_btn.pack(side='left', padx=10)

        featured_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        featured_frame.pack(fill='x', pady=20)

        featured_label = tk.Label(featured_frame,
                                  text="Featured Content",
                                  font=('Arial', 20, 'bold'),
                                  fg='white',
                                  bg=self.colors['bg'])
        featured_label.pack(anchor='w')

        featured_movies = self.get_movies_data()[:6]
        self.create_content_grid(featured_frame, featured_movies, "Movies")

        featured_series = self.get_series_data()[:6]
        self.create_content_grid(featured_frame, featured_series, "TV Series")

    def create_content_grid(self, parent, content, title):
        section_frame = tk.Frame(parent, bg=self.colors['bg'])
        section_frame.pack(fill='x', pady=20)

        title_label = tk.Label(section_frame,
                               text=title,
                               font=('Arial', 18, 'bold'),
                               fg='white',
                               bg=self.colors['bg'])
        title_label.pack(anchor='w', pady=(0, 10))

        grid_frame = tk.Frame(section_frame, bg=self.colors['bg'])
        grid_frame.pack(fill='x')

        for i, item in enumerate(content):
            if i >= 6:
                break

            item_frame = tk.Frame(grid_frame, bg='#1a1a1a', width=180, height=280)
            item_frame.pack(side='left', padx=10, pady=5)
            item_frame.pack_propagate(False)

            image_path = self.find_image_file(item.get('image', ''))
            if image_path:
                try:
                    img = Image.open(image_path)
                    resample = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS
                    img = img.resize((160, 200), resample)
                    photo = ImageTk.PhotoImage(img)
                    img_label = tk.Label(item_frame, image=photo, bg='#1a1a1a')
                    img_label.image = photo
                    img_label.pack(pady=10)
                except Exception:
                    fallback_label = tk.Label(item_frame, text="No Image",
                                              bg='#1a1a1a', fg='white', width=20, height=10)
                    fallback_label.pack(pady=10)
            else:
                fallback_label = tk.Label(item_frame, text="No Image",
                                          bg='#1a1a1a', fg='white', width=20, height=10)
                fallback_label.pack(pady=10)

            title_text = item['name'] if len(item['name']) <= 20 else item['name'][:17] + "..."
            title_label = tk.Label(item_frame, text=title_text,
                                   font=('Arial', 10, 'bold'),
                                   fg='white', bg='#1a1a1a',
                                   wraplength=160)
            title_label.pack(pady=5)

            genre_label = tk.Label(item_frame, text=item.get('genre', ''),
                                   font=('Arial', 8),
                                   fg=self.colors['text_secondary'], bg='#1a1a1a')
            genre_label.pack(pady=2)

            watch_btn = tk.Button(item_frame, text="Watch Now",
                                  font=('Arial', 9),
                                  bg=self.colors['accent'], fg='white',
                                  command=lambda url=item.get('url', ''): self.open_content_window(url))
            watch_btn.pack(pady=5)

    # ---------------- Browse pages / posters ----------------
    def open_movies(self):
        self.create_browse_page("Movies", self.get_movies_data())

    def open_webseries(self):
        self.create_browse_page("TV Series", self.get_series_data())

    def create_browse_page(self, title, content):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title(f'FROZZLE - {title}')
        self.root.config(bg=self.colors['bg'])
        self.center_window(1200, 800)

        header = tk.Frame(self.root, bg='#1a1a1a', height=60)
        header.pack(fill='x', padx=0, pady=0)
        header.pack_propagate(False)

        logo_label = tk.Label(header, text="FROZZLE", font=('Arial', 24, 'bold'),
                              fg=self.colors['accent'], bg='#1a1a1a')
        logo_label.pack(side='left', padx=20, pady=10)

        nav_frame = tk.Frame(header, bg='#1a1a1a')
        nav_frame.pack(side='left', padx=50)

        tk.Button(nav_frame, text="Home", font=('Arial', 12),
                  bg='#1a1a1a', fg='white', bd=0, command=self.create_home_page).pack(side='left', padx=10)
        tk.Button(nav_frame, text="Movies", font=('Arial', 12),
                  bg='#1a1a1a', fg='white', bd=0, command=self.open_movies).pack(side='left', padx=10)
        tk.Button(nav_frame, text="TV Series", font=('Arial', 12),
                  bg='#1a1a1a', fg='white', bd=0, command=self.open_webseries).pack(side='left', padx=10)

        user_frame = tk.Frame(header, bg='#1a1a1a')
        user_frame.pack(side='right', padx=20)
        tk.Label(user_frame, text=f"Welcome, {self.current_user or 'Guest'}",
                 font=('Arial', 12), fg='white', bg='#1a1a1a').pack(side='left', padx=10)
        tk.Button(user_frame, text="Logout", font=('Arial', 10),
                  bg=self.colors['accent'], fg='white', command=self.logout).pack(side='left', padx=5)

        content_frame = tk.Frame(self.root, bg=self.colors['bg'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)

        title_label = tk.Label(content_frame, text=title,
                               font=('Arial', 28, 'bold'),
                               fg='white', bg=self.colors['bg'])
        title_label.pack(anchor='w', pady=20)

        self.create_poster_grid(content_frame, content)

    def create_poster_grid(self, parent, content):
        canvas = tk.Canvas(parent, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for i, item in enumerate(content):
            if i % 4 == 0:
                row_frame = tk.Frame(scrollable_frame, bg=self.colors['bg'])
                row_frame.pack(fill='x', pady=10)
            self.create_poster_item(row_frame, item)

    def create_poster_item(self, parent, item):
        item_frame = tk.Frame(parent, bg='#1a1a1a', width=220, height=320)
        item_frame.pack(side='left', padx=15, pady=10)
        item_frame.pack_propagate(False)

        image_path = self.find_image_file(item.get('image', ''))
        if image_path:
            try:
                img = Image.open(image_path)
                resample = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS
                img = img.resize((200, 250), resample)
                photo = ImageTk.PhotoImage(img)

                img_label = tk.Label(item_frame, image=photo, bg='#1a1a1a', cursor='hand2')
                img_label.image = photo
                img_label.pack(pady=10)
                img_label.bind("<Button-1>", lambda e, url=item.get('url', ''): self.open_content_window(url))
            except Exception:
                self.create_fallback_poster(item_frame, item.get('name', ''))
        else:
            self.create_fallback_poster(item_frame, item.get('name', ''))

        title_text = item.get('name', '') if len(item.get('name', '')) <= 25 else item.get('name', '')[:22] + "..."
        title_label = tk.Label(item_frame, text=title_text,
                               font=('Arial', 11, 'bold'),
                               fg='white', bg='#1a1a1a',
                               wraplength=180, cursor='hand2')
        title_label.pack(pady=5)
        title_label.bind("<Button-1>", lambda e, url=item.get('url', ''): self.open_content_window(url))

        genre_label = tk.Label(item_frame, text=item.get('genre', ''),
                               font=('Arial', 9),
                               fg=self.colors['text_secondary'], bg='#1a1a1a')
        genre_label.pack(pady=2)

        watch_btn = tk.Button(item_frame, text="▶ Watch Now",
                              font=('Arial', 10),
                              bg=self.colors['accent'], fg='white',
                              command=lambda url=item.get('url', ''): self.open_content_window(url))
        watch_btn.pack(pady=8)

    def create_fallback_poster(self, parent, title):
        fallback_frame = tk.Frame(parent, bg='#2a2a2a', width=200, height=250)
        fallback_frame.pack(pady=10)
        fallback_frame.pack_propagate(False)

        title_label = tk.Label(fallback_frame, text=title,
                               font=('Arial', 12, 'bold'),
                               fg='white', bg='#2a2a2a',
                               wraplength=180)
        title_label.pack(expand=True)

    def open_content_window(self, url):
        try:
            if not url:
                messagebox.showwarning("No URL", "No content URL provided.")
                return
            webbrowser.open(url)
            messagebox.showinfo("Success", "Opening in your web browser...")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open content: {str(e)}")

    def logout(self):
        self.current_user = None
        self.create_main_page()

    def update_status(self):
        if os.path.exists(self.images_dir):
            files = [f for f in os.listdir(self.images_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
            self.status_label.config(text=f"Ready with {len(files)} movies & series available")
        else:
            self.status_label.config(text="Setting up...")

    # ---------------- Image generation / helpers ----------------
    def test_pil(self):
        try:
            test_img = Image.new('RGB', (10, 10), color='red')
            test_img.save('test_delete_me.jpg')
            if os.path.exists('test_delete_me.jpg'):
                os.remove('test_delete_me.jpg')
            print("✓ PIL is working correctly")
            return True
        except Exception as e:
            print(f"✗ PIL Error: {e}")
            messagebox.showerror("PIL Error", f"Pillow library not working: {e}\n\nRun: pip install pillow")
            return False

    def center_window(self, width, height):
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def setup_images_directory(self):
        print("Setting up images directory...")
        os.makedirs(self.images_dir, exist_ok=True)
        existing_files = [f for f in os.listdir(self.images_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        print(f"Found {len(existing_files)} existing images")
        # generate if fewer than some threshold (example 50)
        if len(existing_files) < 50:
            print("Generating missing images...")
            self.generate_all_images()
        else:
            print("Images already exist, skipping generation")

    def sanitize_image_name(self, image_name):
        # Remove extension and illegal chars, produce safe filename base
        base = os.path.splitext(image_name)[0]
        base = base.replace(" ", "_")
        # strip any remaining slashes etc.
        return "".join(c for c in base if c.isalnum() or c in "_-")

    def find_image_file(self, image_name):
        """Return first existing file path for given image base (tries common extensions)."""
        if not image_name:
            return None
        base = self.sanitize_image_name(image_name)
        for ext in ('.jpg', '.jpeg', '.png'):
            candidate = os.path.join(self.images_dir, base + ext)
            if os.path.exists(candidate):
                return candidate
        # fallback: sometimes the image_name itself might be a full filename inside images_dir
        candidate_full = os.path.join(self.images_dir, image_name)
        if os.path.exists(candidate_full):
            return candidate_full
        return None

    def generate_all_images(self):
        try:
            print("Starting image generation...")

            movies = self.get_movies_data()
            print(f"Generating {len(movies)} movie posters...")
            for i, movie in enumerate(movies):
                base = self.sanitize_image_name(movie.get('image', movie.get('name', f"movie_{i}")))
                image_path = os.path.join(self.images_dir, f"{base}.jpg")
                if not os.path.exists(image_path):
                    self.create_simple_poster(movie["name"], base, movie.get("genre", ""))
                if (i + 1) % 20 == 0:
                    print(f"Processed {i + 1}/{len(movies)} movies")

            series = self.get_series_data()
            print(f"Generating {len(series)} series posters...")
            for i, show in enumerate(series):
                base = self.sanitize_image_name(show.get('image', show.get('name', f"series_{i}")))
                image_path = os.path.join(self.images_dir, f"{base}.jpg")
                if not os.path.exists(image_path):
                    self.create_simple_poster(show["name"], base, show.get("genre", ""), is_series=True)
                if (i + 1) % 10 == 0:
                    print(f"Processed {i + 1}/{len(series)} series")

            print("✓ All images generated successfully!")

        except Exception as e:
            print(f"Error generating images: {e}")
            self.create_emergency_images()

    def create_simple_poster(self, title, image_name, genre, is_series=False):
        try:
            width, height = 200, 300
            colors = ['#e50914', '#00a8ff', '#9c88ff', '#fbc531', '#4cd137', '#487eb0', '#e84118', '#8c7ae6']
            bg_color = random.choice(colors)

            img = Image.new('RGB', (width, height), color=bg_color)
            draw = ImageDraw.Draw(img)

            try:
                title_font = ImageFont.truetype("arial.ttf", 16)
                genre_font = ImageFont.truetype("arial.ttf", 12)
                tag_font = ImageFont.truetype("arial.ttf", 10)
            except Exception:
                title_font = ImageFont.load_default()
                genre_font = ImageFont.load_default()
                tag_font = ImageFont.load_default()

            # simple gradient bottom
            try:
                r, g, b = int(bg_color[1:3], 16), int(bg_color[3:5], 16), int(bg_color[5:7], 16)
            except Exception:
                r, g, b = 50, 50, 50
            for i in range(40):
                y = height - 40 + i
                new_color = (max(0, r - i // 2), max(0, g - i // 2), max(0, b - i // 2))
                draw.rectangle([0, y, width, y + 1], fill=new_color)

            # Title wrapping (very approximate)
            words = title.split()
            lines = []
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                approx_width = len(test_line) * 8  # smaller factor for default font
                if approx_width <= width - 20:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(' '.join(current_line))

            title_y = 80 - (len(lines) * 8)
            for i, line in enumerate(lines):
                draw.text((width // 2, title_y + i * 18), line, fill="white", font=title_font, anchor="mm")

            draw.text((width // 2, 180), genre.upper(), fill="white", font=genre_font, anchor="mm")

            badge_text = "SERIES" if is_series else "MOVIE"
            badge_color = "#ff6b6b" if is_series else "#74b9ff"

            badge_width = 80
            badge_height = 25
            badge_x = (width - badge_width) // 2
            badge_y = 220

            draw.rectangle([badge_x, badge_y, badge_x + badge_width, badge_y + badge_height], fill=badge_color)
            draw.text((width // 2, badge_y + badge_height // 2), badge_text, fill="white", font=tag_font, anchor="mm")

            draw.text((width // 2, 260), "FROZZLE", fill="white", font=tag_font, anchor="mm")

            image_path = os.path.join(self.images_dir, f"{image_name}.jpg")
            img.save(image_path)

        except Exception as e:
            print(f"Error creating poster for {title}: {e}")
            self.create_basic_fallback(title, image_name)

    def create_basic_fallback(self, title, image_name):
        try:
            img = Image.new('RGB', (200, 300), color='#2a2a2a')
            draw = ImageDraw.Draw(img)

            short_title = title
            if len(short_title) > 25:
                short_title = short_title[:22] + "..."

            draw.text((100, 130), short_title, fill="white", anchor="mm")
            draw.text((100, 180), "FROZZLE", fill="#e50914", anchor="mm")

            image_path = os.path.join(self.images_dir, f"{image_name}.jpg")
            img.save(image_path)
            print(f"✓ Created fallback: {image_name}.jpg")

        except Exception as e:
            print(f"Critical error creating fallback for {title}: {e}")

    def create_emergency_images(self):
        print("Creating emergency fallback images...")
        colors = ['red', 'blue', 'green', 'purple', 'orange']

        all_content = self.get_movies_data() + self.get_series_data()
        for i, item in enumerate(all_content[:30]):
            try:
                img = Image.new('RGB', (200, 300), color=colors[i % len(colors)])
                draw = ImageDraw.Draw(img)
                draw.text((100, 150), item["name"][:15], fill="white", anchor="mm")
                base = self.sanitize_image_name(item.get('image', item.get('name', f"item_{i}")))
                image_path = os.path.join(self.images_dir, f"{base}.jpg")
                img.save(image_path)
            except Exception:
                pass

    # ---------------- Data storage / validation ----------------
    def load_users(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    return json.load(f) or {}
        except Exception:
            pass
        return {}

    def save_users(self):
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save user data: {str(e)}")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_username(self, username):
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        return True, ""

    def validate_password(self, password):
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        return True, ""

    # ---------------- Content datasets ----------------
    def get_movies_data(self):
        return [
            {"name": "URI: The Surgical Strike", "url": "https://www.cineby.gd/movie/554600", "image": "URI", "genre": "Action"},
            {"name": "Sitare zamee par", "url": "https://www.cineby.gd/movie/1190511", "image": "SZP", "genre": "Comedy"},
            {"name": "Dangal", "url": "https://www.cineby.gd/movie/360814", "image": "dangal", "genre": "Sports"},
            {"name": "3 Idiots", "url": "https://www.cineby.gd/movie/244267", "image": "3idiots", "genre": "Comedy"},
            {"name": "Bahubali: The Beginning", "url": "https://www.cineby.gd/movie/256040", "image": "bahubali1", "genre": "Action"},
            {"name": "Bahubali: The Conclusion", "url": "https://www.cineby.gd/movie/350312", "image": "bahubali2", "genre": "Action"},
            {"name": "KGF: Chapter 1", "url": "https://www.cineby.gd/movie/564147", "image": "kgf1", "genre": "Action"},
            {"name": "KGF: Chapter 2", "url": "https://www.cineby.gd/movie/587412", "image": "kgf2", "genre": "Action"},
            {"name": "RRR", "url": "https://www.cineby.gd/movie/579974", "image": "rrr", "genre": "Action"},
            {"name": "Pushpa: The Rise", "url": "https://www.cineby.gd/movie/690957", "image": "pushpa", "genre": "Action"},
            {"name": "Vikram Vedha", "url": "https://www.cineby.gd/movie/432139", "image": "vikramvedha", "genre": "Action"},
            {"name": "War", "url": "https://www.cineby.gd/movie/585268", "image": "war", "genre": "Action"},
            {"name": "Kabir Singh", "url": "https://www.cineby.gd/movie/577328", "image": "kabirsingh", "genre": "Romance"},
            {"name": "Andhadhun", "url": "https://www.cineby.gd/movie/534780", "image": "andhadhun", "genre": "Thriller"},
            {"name": "Stree", "url": "https://www.cineby.gd/movie/533991", "image": "stree", "genre": "Comedy"},
            # Add more movies if you like
        ]

    def get_series_data(self):
        return [
            {"name": "Squid Game", "url": "https://www.cineby.gd/tv/93405", "image": "squidgame", "genre": "Thriller"},
            {"name": "Stranger Things", "url": "https://www.cineby.gd/tv/66732", "image": "strangerthings", "genre": "Sci-Fi"},
            {"name": "Money Heist", "url": "https://www.cineby.gd/tv/71446", "image": "moneyheist", "genre": "Crime"},
            {"name": "The Witcher", "url": "https://www.cineby.gd/tv/71912", "image": "thewitcher", "genre": "Fantasy"},
            {"name": "Breaking Bad", "url": "https://www.cineby.gd/tv/1396", "image": "breakingbad", "genre": "Drama"},
            {"name": "Game of Thrones", "url": "https://www.cineby.gd/tv/1399", "image": "gameofthrones", "genre": "Fantasy"},
            {"name": "The Mandalorian", "url": "https://www.cineby.gd/tv/82856", "image": "mandalorian", "genre": "Sci-Fi"},
            {"name": "Wednesday", "url": "https://www.cineby.gd/tv/119051", "image": "wednesday", "genre": "Comedy"},
            {"name": "Lucifer", "url": "https://www.cineby.gd/tv/564704", "image": "lucifer", "genre": "Crime"},
            {"name": "The Crown", "url": "https://www.cineby.gd/tv/65494", "image": "thecrown", "genre": "Drama"},
            {"name": "Mirzapur", "url": "https://www.cineby.gd/tv/84105", "image": "mirzapur", "genre": "Crime"},
            {"name": "Sacred Games", "url": "https://www.cineby.gd/tv/79352", "image": "sacredgames", "genre": "Thriller"},
            {"name": "The Family Man", "url": "https://www.cineby.gd/tv/5994", "image": "familyman", "genre": "Action"},
            {"name": "Panchayat", "url": "https://www.cineby.gd/tv/101352", "image": "panchayat", "genre": "Comedy"},
            {"name": "Kota Factory", "url": "https://www.cineby.gd/tv/89113", "image": "kotafactory", "genre": "Drama"},
            # Add more series if you like
        ]


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieStreamingApp(root)
    root.mainloop()
