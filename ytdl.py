import os
import platform
import sys
import threading
import itertools
from yt_dlp import YoutubeDL
from colorama import Fore, Style, init
import time

# Initialize colorama
init()
def progress_hook(d):
    if d['status'] == 'finished':
        print(Fore.GREEN + f"Download selesai: {d['filename']}" + Style.RESET_ALL)
    # Additional handling can be added here

def clear_terminal():
    # Clear terminal screen based on the operating system
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def print_ascii_art():
    # Display ASCII art or text-based logo
    print(Fore.CYAN + '''
╔═══════════════════════════════════════════════════════════════════╗
║███████╗██╗   ██╗██████╗ ███████╗███╗   ██╗███████╗██████╗ ██╗     ║
║██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝████╗  ██║██╔════╝██╔══██╗██║     ║
║███████╗ ╚████╔╝ ██████╔╝█████╗  ██╔██╗ ██║███████╗██║  ██║██║     ║
║╚════██║  ╚██╔╝  ██╔══██╗██╔══╝  ██║╚██╗██║╚════██║██║  ██║██║     ║
║███████║   ██║   ██║  ██║███████╗██║ ╚████║███████║██████╔╝███████╗║
║╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝╚═════╝ ╚══════╝║
╚═══════════════════https://github.com/allifiz══════════════════════╝
    ''' + Style.RESET_ALL)

def print_thank_you():
    # Display ASCII art "Terima Kasih"
    print(Fore.CYAN + '''
████████╗███████╗██████╗ ██╗███╗   ███╗ █████╗ ██╗  ██╗ █████╗ ███████╗██╗██╗  ██╗  
╚══██╔══╝██╔════╝██╔══██╗██║████╗ ████║██╔══██╗██║ ██╔╝██╔══██╗██╔════╝██║██║  ██║      
   ██║   █████╗  ██████╔╝██║██╔████╔██║███████║█████╔╝ ███████║███████╗██║███████║      
   ██║   ██╔══╝  ██╔══██╗██║██║╚██╔╝██║██╔══██║██╔═██╗ ██╔══██║╚════██║██║██╔══██║  
   ██║   ███████╗██║  ██║██║██║ ╚═╝ ██║██║  ██║██║  ██╗██║  ██║███████║██║██║  ██║     
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═╝    
                  terimakasih telah menggunakan tools ini !         
                      https://github.com/allifiz                                                
    ''' + Style.RESET_ALL)

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def spinner_func(stop_event):
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    while not stop_event.is_set():
        sys.stdout.write(Fore.YELLOW + "\rTunggu, sedang mendownload " + next(spinner) + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * 50 + '\r')  # Clear the spinner line

def download_youtube_video_to_mp3(url, output_path='downloads/music'):
    # Mengunduh dan mengonversi video YouTube ke MP3
    ydl_opts = {
        'format': 'bestaudio/best',  # Unduh audio terbaik
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'noplaylist': True,               # Sembunyikan output yt-dlp
        'quiet': True,               # Sembunyikan output yt-dlp
        'no_warnings': True,         # Sembunyikan peringatan
        'postprocessors': [{         # Konversi ke mp3
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',  # Kualitas audio mp3
        }],
        'progress_hooks': [progress_hook],
    }

    create_folder(output_path)

    stop_spinner = threading.Event()
    spinner_thread = threading.Thread(target=spinner_func, args=(stop_spinner,))
    spinner_thread.start()

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            stop_spinner.set()
            spinner_thread.join()
            clear_terminal()  # Bersihkan terminal sebelum menampilkan ASCII art
            print_thank_you()  # Menampilkan ASCII art "Terima Kasih"
            print(Fore.YELLOW + f"Video '{info_dict['title']}' telah dikonversi dan disimpan sebagai MP3 di folder '{output_path}'." + Style.RESET_ALL)
    except Exception as e:
        stop_spinner.set()
        spinner_thread.join()
        print(Fore.RED + f"Terjadi kesalahan: {e}" + Style.RESET_ALL)

def download_youtube_playlist_to_mp3(playlist_url, output_path='downloads/music'):
    # Mengunduh playlist YouTube dan mengonversi video ke MP3
    ydl_opts = {
        'format': 'bestaudio/best',  # Unduh audio terbaik
        'outtmpl': os.path.join(output_path, '%(playlist_title)s', '%(title)s.%(ext)s'),  # Simpan video dalam folder playlist
        'quiet': True,               # Sembunyikan output yt-dlp
        'no_warnings': True,         # Sembunyikan peringatan
        'noplaylist': False,  # Unduh seluruh playlist
        'postprocessors': [{  # Konversi ke mp3
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',  # Kualitas audio mp3
        }],
        'progress_hooks': [progress_hook],
    }

    create_folder(output_path)

    stop_spinner = threading.Event()
    spinner_thread = threading.Thread(target=spinner_func, args=(stop_spinner,))
    spinner_thread.start()

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(playlist_url, download=True)
            playlist_name = info_dict.get('playlist_title', 'playlist')
            playlist_path = os.path.join(output_path, playlist_name)
            create_folder(playlist_path)
            stop_spinner.set()
            spinner_thread.join()
            clear_terminal()  # Bersihkan terminal sebelum menampilkan ASCII art
            print_thank_you()  # Menampilkan ASCII art "Terima Kasih"
            print(Fore.YELLOW + f"Semua video dari playlist telah dikonversi dan disimpan sebagai MP3 di folder '{playlist_path}'." + Style.RESET_ALL)
    except Exception as e:
        stop_spinner.set()
        spinner_thread.join()
        print(Fore.RED + f"Terjadi kesalahan: {e}" + Style.RESET_ALL)

def download_youtube_video_with_quality(url, output_path='downloads/video'):
    # Defaultkan kualitas video ke 1080p, jika tidak ada, gunakan 720p
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best',  # Menggabungkan video terbaik dengan audio
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'quiet': True,               # Sembunyikan output yt-dlp
        'no_warnings': True,         # Sembunyikan peringatan
        'noplaylist': True,  # Menghindari mengunduh seluruh playlist
        'merge_output_format': 'mp4',  # Gabungkan output ke format MP4
        'progress_hooks': [progress_hook],
    }
    
    create_folder(output_path)
    
    stop_spinner = threading.Event()
    spinner_thread = threading.Thread(target=spinner_func, args=(stop_spinner,))
    spinner_thread.start()

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            stop_spinner.set()
            spinner_thread.join()
            clear_terminal()  # Bersihkan terminal sebelum menampilkan ASCII art
            print_thank_you()  # Menampilkan ASCII art "Terima Kasih"
            print(Fore.YELLOW + f"Video '{info_dict['title']}' telah diunduh dengan audio dan disimpan di folder '{output_path}'." + Style.RESET_ALL)
    except Exception as e:
        stop_spinner.set()
        spinner_thread.join()
        print(Fore.RED + f"Terjadi kesalahan: {e}" + Style.RESET_ALL)

def download_youtube_playlist_with_quality(playlist_url, output_path='downloads/video'):
    # Defaultkan kualitas video ke 1080p, jika tidak ada, gunakan 720p
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best',  # Menggabungkan video terbaik dengan audio
        'outtmpl': os.path.join(output_path, '%(playlist_title)s', '%(title)s.%(ext)s'),
        'quiet': True,               # Sembunyikan output yt-dlp
        'no_warnings': True,         # Sembunyikan peringatan
        'noplaylist': False,  # Mengunduh seluruh playlist
        'merge_output_format': 'mp4',  # Gabungkan output ke format MP4
        'progress_hooks': [progress_hook],
    }

    create_folder(output_path)

    stop_spinner = threading.Event()
    spinner_thread = threading.Thread(target=spinner_func, args=(stop_spinner,))
    spinner_thread.start()

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(playlist_url, download=True)
            playlist_name = info_dict.get('playlist_title', 'playlist')
            playlist_path = os.path.join(output_path, playlist_name)
            create_folder(playlist_path)
            stop_spinner.set()
            spinner_thread.join()
            clear_terminal()  # Bersihkan terminal sebelum menampilkan ASCII art
            print_thank_you()  # Menampilkan ASCII art "Terima Kasih"
            print(Fore.YELLOW + f"Semua video dari playlist telah diunduh dengan audio dan disimpan di folder '{playlist_path}'." + Style.RESET_ALL)
    except Exception as e:
        stop_spinner.set()
        spinner_thread.join()
        print(Fore.RED + f"Terjadi kesalahan: {e}" + Style.RESET_ALL)

def main():
    clear_terminal()
    print_ascii_art()
    print(Fore.YELLOW + "Selamat datang di downloader YouTube!" + Style.RESET_ALL)
    
    while True:
        print(Fore.LIGHTCYAN_EX + "Menu:" + Style.RESET_ALL)
        print(Fore.LIGHTBLUE_EX + "1. Download video dari YouTube (MP3)")
        print("2. Download playlist dari YouTube (MP3)")
        print("3. Download video dari YouTube (Video dengan kualitas terbaik)")
        print("4. Download playlist dari YouTube (Video dengan kualitas terbaik)" + Style.RESET_ALL)
        print(Fore.LIGHTRED_EX+"5. Keluar"+Style.RESET_ALL)

        choice = input(Fore.CYAN +"Masukkan pilihan (1/2/3/4/5): "+ Style.RESET_ALL).strip()

        if choice == '1':
            url = input("Masukkan URL video YouTube: ").strip()
            download_youtube_video_to_mp3(url)
        elif choice == '2':
            playlist_url = input("Masukkan URL playlist YouTube: ").strip()
            download_youtube_playlist_to_mp3(playlist_url)
        elif choice == '3':
            url = input("Masukkan URL video YouTube: ").strip()
            download_youtube_video_with_quality(url)
        elif choice == '4':
            playlist_url = input("Masukkan URL playlist YouTube: ").strip()
            download_youtube_playlist_with_quality(playlist_url)
        elif choice == '5':
            print(Fore.YELLOW + "Terima kasih telah menggunakan tools ini!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Pilihan tidak valid. Silakan coba lagi." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
