from smart_home_ui.main_controller import MainController

DATA_FILE = "home_data.json"

def main() -> None:
    print("--- Welcome to the Smart Home Management System (v2) ---")

    app = MainController(DATA_FILE)
    app.run()

if __name__ == "__main__":
    main()
