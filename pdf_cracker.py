import pikepdf
import itertools
import string
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse


def load_passwords(wordlist_file):
    try:
        with open(wordlist_file, "r") as f:
            for line in f:
                yield line.strip()
    except FileNotFoundError:
        print(f"[!] Wordlist not found: {wordlist_file}")
        return


def generate_passwords(chars, max_length):
    for length in range(1, max_length + 1):
        for combo in itertools.product(chars, repeat=length):
            yield ''.join(combo)


def try_password(pdf_file, password):
    try:
        with pikepdf.open(pdf_file, password=password):
            return password
    except pikepdf._core.PasswordError:
        return None
    except Exception:
        return None


def decrypt_pdf(pdf_file, passwords, thread_count=4):
    print("[+] Starting password attempts...")

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        future_to_pass = {
            executor.submit(try_password, pdf_file, pwd): pwd
            for pwd in passwords
        }

        for future in tqdm(as_completed(future_to_pass), total=len(future_to_pass), desc="Trying", unit="pass"):
            result = future.result()
            if result:
                return result

    return None


def main():
    parser = argparse.ArgumentParser(description="Educational PDF Cracker Tool (Project Purpose Only)")

    parser.add_argument("pdf_file", help="Path to password-protected PDF")
    parser.add_argument("--wordlist", help="Path to a wordlist")
    parser.add_argument("--generate", action="store_true", help="Use brute-force generation")
    parser.add_argument("--max_length", type=int, default=3, help="Max length for brute-force passwords")
    parser.add_argument("--threads", type=int, default=4, help="Thread count")

    args = parser.parse_args()

    if args.wordlist:
        passwords = list(load_passwords(args.wordlist))
    elif args.generate:
        chars = string.ascii_lowercase + string.digits
        passwords = list(generate_passwords(chars, args.max_length))
    else:
        print("[!] You must use --wordlist or --generate")
        return

    print(f"[+] Loaded {len(passwords)} passwords.")
    print("[+] Cracking started...\n")

    result = decrypt_pdf(args.pdf_file, passwords, args.threads)

    if result:
        print(f"\n[+] SUCCESS! Password found: {result}")
    else:
        print("\n[-] Password not found.")


if __name__ == "__main__":
    main()
