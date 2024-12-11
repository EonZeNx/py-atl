if __name__ == '__main__':
    try:
        import clr_loader
    except ImportError:
        import pip
        pip.main(['install', 'clr-loader'])
        import clr_loader

    try:
        import pythonnet
    except ImportError:
        import pip
        pip.main(["install", "pythonnet"])
        import pythonnet

    from main import setup_dll
    setup_dll()
