import keyring

# Give your key a unique name (e.g., "ffxiv_main_2fa", "ffxiv_acc1_2fa")
keyring_name = "ffxiv_main_2fa"

# Paste your authentication key here (with spaces removed)
secret_key = "..."

keyring.set_password(keyring_name, "otp_secret", secret_key)
