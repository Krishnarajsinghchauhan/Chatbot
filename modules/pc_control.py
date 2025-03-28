import os
import subprocess
import platform
import difflib
import shutil

def scan_disk_items(roots, item_type="file"):
    results = []
    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root):
            if item_type == "folder":
                for d in dirnames:
                    results.append(os.path.join(dirpath, d))
            else:
                for f in filenames:
                    results.append(os.path.join(dirpath, f))
    return results

def find_best_match(query, items, cutoff=0.5):
    if not items:
        return None
    basenames = [os.path.basename(i).lower() for i in items]
    matches = difflib.get_close_matches(query.lower(), basenames, n=1, cutoff=cutoff)
    if matches:
        for item in items:
            if os.path.basename(item).lower() == matches[0]:
                return item
    return None

def open_app(query):
    system = platform.system()
    if system == "Windows":
        roots = [os.environ.get("ProgramFiles", "C:\\Program Files"), os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), os.path.expanduser("~\\AppData\\Local\\Programs")]
    elif system == "Darwin":
        roots = ["/Applications"]
    else:
        roots = ["/usr/bin", "/usr/local/bin"]
    items = []
    for r in roots:
        if os.path.exists(r):
            items.extend(scan_disk_items([r], item_type="file"))
    best = find_best_match(query, items)
    if best:
        try:
            if system == "Windows":
                os.startfile(best)
            elif system == "Darwin":
                subprocess.Popen(["open", best])
            else:
                subprocess.Popen([best])
            return best
        except Exception as e:
            print(f"Error opening app: {e}")
    else:
        print(f"No application found matching '{query}'.")
    return None

def open_folder(query):
    system = platform.system()
    if system == "Windows":
        roots = [os.path.expanduser("~")]
    elif system == "Darwin":
        roots = ["/Users", os.path.expanduser("~")]
    else:
        roots = ["/"]
    items = []
    for r in roots:
        if os.path.exists(r):
            items.extend(scan_disk_items([r], item_type="folder"))
    best = find_best_match(query, items)
    if best:
        try:
            if system == "Windows":
                os.startfile(best)
            elif system == "Darwin":
                subprocess.Popen(["open", best])
            else:
                subprocess.Popen(["xdg-open", best])
            return best
        except Exception as e:
            print(f"Error opening folder: {e}")
    else:
        print(f"No folder found matching '{query}'.")
    return None

def open_file(query):
    system = platform.system()
    if system == "Windows":
        roots = [os.path.expanduser("~")]
    elif system == "Darwin":
        roots = ["/Users", os.path.expanduser("~")]
    else:
        roots = ["/"]
    items = []
    for r in roots:
        if os.path.exists(r):
            items.extend(scan_disk_items([r], item_type="file"))
    best = find_best_match(query, items)
    if best:
        try:
            if system == "Windows":
                os.startfile(best)
            elif system == "Darwin":
                subprocess.Popen(["open", best])
            else:
                subprocess.Popen(["xdg-open", best])
            return best
        except Exception as e:
            print(f"Error opening file: {e}")
    else:
        print(f"No file found matching '{query}'.")
    return None

def rename_item(query, new_name, item_type="file"):
    system = platform.system()
    if system == "Windows":
        roots = [os.path.expanduser("~")]
    elif system == "Darwin":
        roots = ["/Users", os.path.expanduser("~")]
    else:
        roots = ["/"]
    items = []
    for r in roots:
        if os.path.exists(r):
            items.extend(scan_disk_items([r], item_type=item_type))
    best = find_best_match(query, items)
    if best:
        new_path = os.path.join(os.path.dirname(best), new_name)
        try:
            os.rename(best, new_path)
            return new_path
        except Exception as e:
            print(f"Error renaming item: {e}")
    else:
        print(f"No {item_type} found matching '{query}' for renaming.")
    return None

def delete_item(query, item_type="file"):
    system = platform.system()
    if system == "Windows":
        roots = [os.path.expanduser("~")]
    elif system == "Darwin":
        roots = ["/Users", os.path.expanduser("~")]
    else:
        roots = ["/"]
    items = []
    for r in roots:
        if os.path.exists(r):
            items.extend(scan_disk_items([r], item_type=item_type))
    best = find_best_match(query, items)
    if best:
        try:
            if item_type == "folder":
                shutil.rmtree(best)
            else:
                os.remove(best)
            return best
        except Exception as e:
            print(f"Error deleting item: {e}")
    else:
        print(f"No {item_type} found matching '{query}' for deletion.")
    return None

def copy_item(query, dest_folder, item_type="file"):
    system = platform.system()
    if system == "Windows":
        roots = [os.path.expanduser("~")]
    elif system == "Darwin":
        roots = ["/Users", os.path.expanduser("~")]
    else:
        roots = ["/"]
    items = []
    for r in roots:
        if os.path.exists(r):
            items.extend(scan_disk_items([r], item_type=item_type))
    best = find_best_match(query, items)
    if best:
        dest_path = os.path.join(dest_folder, os.path.basename(best))
        try:
            if item_type == "folder":
                shutil.copytree(best, dest_path)
            else:
                shutil.copy2(best, dest_path)
            return dest_path
        except Exception as e:
            print(f"Error copying item: {e}")
    else:
        print(f"No {item_type} found matching '{query}' for copying.")
    return None
def close_app(app_name):
    """Closes the application by its name."""
    import os
    os.system(f"taskkill /f /im {app_name}.exe")

