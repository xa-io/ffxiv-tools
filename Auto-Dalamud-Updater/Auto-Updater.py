import ctypes
import getpass
import json
import os
import subprocess
import sys
import threading
import time
from ctypes import wintypes
from pathlib import Path

try:
    import psutil
except ImportError:
    print("[ERROR] Required package not installed!")
    print("[ERROR] Install with: pip install psutil")
    input("Press Enter to exit...")
    sys.exit(1)

try:
    import pyotp
    import keyring
    import requests
    OTP_PACKAGES_AVAILABLE = True
except ImportError:
    OTP_PACKAGES_AVAILABLE = False

try:
    from pywinauto import Desktop
    PYWINAUTO_AVAILABLE = True
except ImportError:
    PYWINAUTO_AVAILABLE = False

user = getpass.getuser()

CONFIG_FILE = "config.json"
OTP_LAUNCH_DELAY = 10
OTP_RETRY_INTERVAL = 5
POLL_INTERVAL = 2
GAME_START_TIMEOUT = 3600
GAME_WINDOW_TIMEOUT = 300
CLOSE_GRACE_PERIOD = 15
DEBUG = False


def acc(nickname, pluginconfigs_path, enable_2fa=False, keyring_name=None):
    return {
        "nickname": nickname,
        "pluginconfigs_path": pluginconfigs_path,
        "enable_2fa": bool(enable_2fa),
        "keyring_name": keyring_name,
    }


account_locations = [
    acc(
        "Main",
        rf"C:\Users\{user}\AppData\Roaming\XIVLauncher\pluginConfigs",
        enable_2fa=True,
        keyring_name="ffxiv_main_2fa",
    ),
]

GAME_LAUNCHERS = {
    "Main": rf"C:\Users\{user}\AppData\Local\XIVLauncher\XIVLauncher.exe",
}

user32 = ctypes.windll.user32
WM_CLOSE = 0x0010
SW_RESTORE = 9
VK_MENU = 0x12
VK_Y = 0x59
VK_RETURN = 0x0D
KEYEVENTF_KEYUP = 0x0002
EnumWindowsProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)


def get_window_text(hwnd):
    buffer = ctypes.create_unicode_buffer(512)
    user32.GetWindowTextW(hwnd, buffer, len(buffer))
    return buffer.value


def get_class_name(hwnd):
    buffer = ctypes.create_unicode_buffer(256)
    user32.GetClassNameW(hwnd, buffer, len(buffer))
    return buffer.value


def get_window_pid(hwnd):
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return pid.value


def enumerate_top_windows():
    windows = []

    @EnumWindowsProc
    def callback(hwnd, _):
        if user32.IsWindowVisible(hwnd):
            windows.append(hwnd)
        return True

    user32.EnumWindows(callback, 0)
    return windows


def enumerate_child_windows(parent_hwnd):
    children = []

    @EnumWindowsProc
    def callback(hwnd, _):
        children.append(hwnd)
        return True

    user32.EnumChildWindows(parent_hwnd, callback, 0)
    return children


def get_process_ids_by_name(process_name):
    pids = set()
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            if (proc.info["name"] or "").lower() == process_name.lower():
                pids.add(proc.info["pid"])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return pids


def has_visible_windows(pid):
    for hwnd in enumerate_top_windows():
        if get_window_pid(hwnd) == pid:
            return True
    return False


def get_visible_process_ids_by_name(process_name):
    visible_pids = []
    for pid in sorted(get_process_ids_by_name(process_name)):
        if has_visible_windows(pid):
            visible_pids.append(pid)
    return visible_pids


def kill_process_by_pid(pid, error_tag="PROCESS"):
    try:
        result = subprocess.run(
            ["taskkill", "/F", "/PID", str(pid)],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return True
        print(f"[{error_tag}] Failed to kill PID {pid}: {result.stderr.strip()}")
        return False
    except Exception as e:
        print(f"[{error_tag}] Failed to kill PID {pid}: {e}")
        return False


def cleanup_batch_launcher_processes(batch_file_path):
    batch_path_lower = os.path.abspath(batch_file_path).lower()
    batch_filename = os.path.basename(batch_file_path).lower()
    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            if (proc.info["name"] or "").lower() != "cmd.exe":
                continue
            cmdline = " ".join(proc.info.get("cmdline") or []).lower()
            if batch_path_lower in cmdline or batch_filename in cmdline:
                proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue


def expand_config_path(value):
    if not value:
        return value
    value = os.path.expandvars(value)
    return value.replace("{user}", user)


def load_external_config():
    global OTP_LAUNCH_DELAY, OTP_RETRY_INTERVAL, POLL_INTERVAL
    global GAME_START_TIMEOUT, GAME_WINDOW_TIMEOUT, CLOSE_GRACE_PERIOD, DEBUG
    global account_locations, GAME_LAUNCHERS

    config_path = Path(__file__).parent / CONFIG_FILE
    if not config_path.exists():
        return

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        print(f"[CONFIG] Loaded configuration from {config_path}")
    except json.JSONDecodeError as e:
        print(f"[CONFIG] Error parsing {CONFIG_FILE}: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"[CONFIG] Error reading {CONFIG_FILE}: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)

    OTP_LAUNCH_DELAY = config.get("OTP_LAUNCH_DELAY", OTP_LAUNCH_DELAY)
    OTP_RETRY_INTERVAL = config.get("OTP_RETRY_INTERVAL", OTP_RETRY_INTERVAL)
    POLL_INTERVAL = config.get("POLL_INTERVAL", POLL_INTERVAL)
    GAME_START_TIMEOUT = config.get("GAME_START_TIMEOUT", GAME_START_TIMEOUT)
    GAME_WINDOW_TIMEOUT = config.get("GAME_WINDOW_TIMEOUT", GAME_WINDOW_TIMEOUT)
    CLOSE_GRACE_PERIOD = config.get("CLOSE_GRACE_PERIOD", CLOSE_GRACE_PERIOD)
    DEBUG = config.get("DEBUG", DEBUG)

    if "account_locations" in config:
        new_locations = []
        for acc_config in config["account_locations"]:
            if not acc_config.get("enabled", True):
                continue
            new_locations.append(
                acc(
                    nickname=acc_config.get("nickname", "Unknown"),
                    pluginconfigs_path=expand_config_path(acc_config.get("pluginconfigs_path", "")),
                    enable_2fa=acc_config.get("enable_2fa", False),
                    keyring_name=acc_config.get("keyring_name", None),
                )
            )
        account_locations = new_locations

    if "game_launchers" in config:
        GAME_LAUNCHERS = {
            nickname: expand_config_path(path)
            for nickname, path in config["game_launchers"].items()
        }


load_external_config()


def get_launcher_config_path(account):
    pluginconfigs_path = account.get("pluginconfigs_path", "")
    if not pluginconfigs_path:
        return None
    return Path(pluginconfigs_path).parent / "launcherConfigV3.json"


def validate_launcher_config(account):
    nickname = account["nickname"]
    config_path = get_launcher_config_path(account)
    if config_path is None:
        print(f"[CONFIG-CHECK] No launcher config path configured for {nickname}")
        return False

    if not config_path.exists():
        print(f"[CONFIG-CHECK] Launcher config not found for {nickname}: {config_path}")
        print("[CONFIG-CHECK] Continuing anyway - launcher may create it on first run")
        return True

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        config_updated = False
        autologin_value = data.get("AutologinEnabled", None)
        if autologin_value != "true":
            data["AutologinEnabled"] = "true"
            config_updated = True
            print(f"[CONFIG-CHECK] {nickname}: Fixed AutologinEnabled: '{autologin_value}' -> 'true'")

        if account.get("enable_2fa", False):
            otp_value = data.get("OtpServerEnabled", None)
            if otp_value != "true":
                data["OtpServerEnabled"] = "true"
                config_updated = True
                print(f"[CONFIG-CHECK] {nickname}: Fixed OtpServerEnabled: '{otp_value}' -> 'true'")

        if config_updated:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"[CONFIG-CHECK] Launcher config updated successfully for {nickname}")
        else:
            print(f"[CONFIG-CHECK] Launcher config OK for {nickname}")

        return True
    except json.JSONDecodeError as e:
        print(f"[CONFIG-CHECK] Error parsing launcher config JSON for {nickname}: {e}")
        return False
    except Exception as e:
        print(f"[CONFIG-CHECK] Error checking launcher config for {nickname}: {e}")
        return False


def launch_launcher(account):
    nickname = account["nickname"]
    launcher_path = GAME_LAUNCHERS.get(nickname)
    if not launcher_path:
        print(f"[ERROR] No launcher configured for {nickname}")
        return False

    if not os.path.exists(launcher_path):
        print(f"[ERROR] Launcher not found for {nickname}: {launcher_path}")
        return False

    try:
        is_batch_file = launcher_path.lower().endswith(".bat")
        if is_batch_file:
            detached_process = 0x00000008
            subprocess.Popen(
                f'cmd.exe /c "{launcher_path}"',
                shell=False,
                creationflags=detached_process | subprocess.CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            def delayed_cleanup():
                time.sleep(30)
                cleanup_batch_launcher_processes(launcher_path)

            threading.Thread(target=delayed_cleanup, daemon=True).start()
        else:
            subprocess.Popen(
                [launcher_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )

        print(f"[LAUNCH] Launcher started for {nickname}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to start launcher for {nickname}: {e}")
        return False


def find_update_dialog_hwnd():
    for hwnd in enumerate_top_windows():
        title = get_window_text(hwnd).strip()
        class_name = get_class_name(hwnd).strip()
        if title == "Out of date":
            return hwnd
        if class_name == "Window" and "out of date" in title.lower():
            return hwnd
    return None


def press_virtual_key(vk_code):
    user32.keybd_event(vk_code, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)


def press_hotkey(*vk_codes):
    for vk_code in vk_codes:
        user32.keybd_event(vk_code, 0, 0, 0)
    time.sleep(0.05)
    for vk_code in reversed(vk_codes):
        user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)


def try_click_update_yes_via_uia():
    if not PYWINAUTO_AVAILABLE:
        return False

    try:
        dialog = Desktop(backend="uia").window(title="Out of date", control_type="Window")
        if not dialog.exists(timeout=0.2):
            return False

        button = dialog.child_window(auto_id="Button1", control_type="Button")
        if not button.exists(timeout=0.2):
            button = dialog.child_window(title="Yes", control_type="Button")
        if not button.exists(timeout=0.2):
            return False

        wrapper = button.wrapper_object()
        if hasattr(wrapper, "invoke"):
            wrapper.invoke()
        else:
            wrapper.click_input()
        print("[UPDATE] Clicked 'Yes' on the out-of-date popup via UI Automation")
        return True
    except Exception as e:
        if DEBUG:
            print(f"[UPDATE] UI Automation click failed: {e}")
        return False


def try_click_update_yes_via_keyboard():
    dialog_hwnd = find_update_dialog_hwnd()
    if not dialog_hwnd:
        return False

    try:
        user32.ShowWindow(dialog_hwnd, SW_RESTORE)
        user32.SetForegroundWindow(dialog_hwnd)
    except Exception as e:
        if DEBUG:
            print(f"[UPDATE] Failed to focus out-of-date popup: {e}")

    time.sleep(0.25)

    for method_name, action in (
        ("Alt+Y", lambda: press_hotkey(VK_MENU, VK_Y)),
        ("Y", lambda: press_virtual_key(VK_Y)),
        ("Enter", lambda: press_virtual_key(VK_RETURN)),
    ):
        action()
        time.sleep(0.5)
        if find_update_dialog_hwnd() is None:
            print(f"[UPDATE] Clicked 'Yes' on the out-of-date popup via {method_name}")
            return True

    return False


def click_update_yes_if_present():
    if find_update_dialog_hwnd() is None:
        return False
    if try_click_update_yes_via_uia():
        return True
    if try_click_update_yes_via_keyboard():
        return True
    if DEBUG:
        print("[UPDATE] Out-of-date popup detected but no click method succeeded")
    return False


def try_send_otp_code(account):
    nickname = account["nickname"]
    if not account.get("enable_2fa", False):
        return True

    if not OTP_PACKAGES_AVAILABLE:
        print(f"[ERROR] 2FA is enabled for {nickname} but required packages are not installed")
        print("[ERROR] Install with: pip install pyotp keyring requests")
        return False

    keyring_name = account.get("keyring_name")
    if not keyring_name:
        print(f"[ERROR] 2FA is enabled for {nickname} but keyring_name is empty")
        return False

    otp_secret = keyring.get_password(keyring_name, "otp_secret")
    if not otp_secret:
        print(f"[ERROR] OTP secret not found in keyring '{keyring_name}' for {nickname}")
        return False

    try:
        code = pyotp.TOTP(otp_secret).now()
        url = f"http://localhost:4646/ffxivlauncher/{code}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        if response.status_code == 200:
            print(f"[2FA] OTP code accepted for {nickname}")
            return True
        print(f"[2FA] Unexpected response for {nickname}: {response.status_code}")
        return False
    except requests.exceptions.RequestException as e:
        if DEBUG:
            print(f"[2FA] OTP send not ready yet for {nickname}: {e}")
        return False


def close_active_dalamud_crash_handlers():
    closed_any = False
    for pid in get_visible_process_ids_by_name("DalamudCrashHandler.exe"):
        print(f"[CRASH-HANDLER] Closing active DalamudCrashHandler.exe PID {pid}")
        if kill_process_by_pid(pid, "CRASH_HANDLER"):
            closed_any = True
    return closed_any


def wait_for_new_game_process(account, existing_game_pids, launch_time):
    otp_sent = not account.get("enable_2fa", False)
    last_otp_attempt = 0.0
    deadline = launch_time + GAME_START_TIMEOUT

    while time.time() < deadline:
        if account.get("enable_2fa", False) and not otp_sent:
            now = time.time()
            if now - launch_time >= OTP_LAUNCH_DELAY and now - last_otp_attempt >= OTP_RETRY_INTERVAL:
                otp_sent = try_send_otp_code(account)
                last_otp_attempt = now

        click_update_yes_if_present()
        close_active_dalamud_crash_handlers()

        current_game_pids = get_process_ids_by_name("ffxiv_dx11.exe")
        new_game_pids = sorted(pid for pid in current_game_pids if pid not in existing_game_pids)
        if new_game_pids:
            pid = new_game_pids[0]
            print(f"[GAME] Detected launched game process PID {pid} for {account['nickname']}")
            return pid

        time.sleep(POLL_INTERVAL)

    return None


def wait_for_game_window(pid):
    deadline = time.time() + GAME_WINDOW_TIMEOUT

    while time.time() < deadline:
        close_active_dalamud_crash_handlers()
        for hwnd in enumerate_top_windows():
            if get_window_pid(hwnd) != pid:
                continue
            title = get_window_text(hwnd).strip()
            if title:
                print(f"[GAME] Visible game window detected: {title}")
                return True
        time.sleep(POLL_INTERVAL)

    return False


def wait_for_process_exit(pid, timeout_seconds):
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        if not psutil.pid_exists(pid):
            return True
        time.sleep(1)
    return not psutil.pid_exists(pid)


def close_game(pid):
    for hwnd in enumerate_top_windows():
        if get_window_pid(hwnd) == pid:
            user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)

    if wait_for_process_exit(pid, CLOSE_GRACE_PERIOD):
        print(f"[CLOSE] Game PID {pid} closed cleanly")
        return True

    try:
        result = subprocess.run(
            ["taskkill", "/F", "/PID", str(pid)],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and wait_for_process_exit(pid, 10):
            print(f"[CLOSE] Game PID {pid} force closed")
            return True
        print(f"[CLOSE] Failed to close PID {pid}: {result.stderr.strip()}")
        return False
    except Exception as e:
        print(f"[CLOSE] Failed to close PID {pid}: {e}")
        return False


def process_account(account):
    nickname = account["nickname"]
    print("-" * 60)
    print(f"[ACCOUNT] Starting updater flow for {nickname}")

    existing_game_pids = get_process_ids_by_name("ffxiv_dx11.exe")
    close_active_dalamud_crash_handlers()

    if account.get("enable_2fa", False) and not OTP_PACKAGES_AVAILABLE:
        print(f"[ACCOUNT] 2FA packages are missing for {nickname}")
        print("[ACCOUNT] Install with: pip install pyotp keyring requests")
        return False

    if not validate_launcher_config(account):
        print(f"[ACCOUNT] Launcher config validation failed for {nickname}")
        return False

    if not launch_launcher(account):
        print(f"[ACCOUNT] Launcher start failed for {nickname}")
        return False

    launch_time = time.time()
    game_pid = wait_for_new_game_process(account, existing_game_pids, launch_time)
    if not game_pid:
        close_active_dalamud_crash_handlers()
        print(f"[ACCOUNT] Timed out waiting for the game process to launch for {nickname}")
        return False

    if not wait_for_game_window(game_pid):
        close_game(game_pid)
        close_active_dalamud_crash_handlers()
        print(f"[ACCOUNT] Game process started but no visible window appeared in time for {nickname}")
        return False

    if not close_game(game_pid):
        close_active_dalamud_crash_handlers()
        print(f"[ACCOUNT] Game opened, but the script could not close it cleanly for {nickname}")
        return False

    close_active_dalamud_crash_handlers()
    print(f"[ACCOUNT] Update flow completed successfully for {nickname}")
    return True


def main():
    print("=" * 60)
    print("  XIVLauncher Auto Updater")
    print("=" * 60)
    print()

    if not account_locations:
        print("[DONE] No enabled accounts configured.")
        return 1

    failed_accounts = []
    for account in account_locations:
        if not process_account(account):
            failed_accounts.append(account["nickname"])
        print()

    if failed_accounts:
        print(f"[DONE] Script completed with errors for: {', '.join(failed_accounts)}")
        return 1

    print("[DONE] Script completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
