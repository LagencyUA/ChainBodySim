from src.drawer import Drawer

def main():
    drawer = Drawer()
    drawer.build_body([30 for _ in range(40)])
    drawer.run()

if __name__ == "__main__":
    main()