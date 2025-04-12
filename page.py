class Page:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def __repr__(self):
        return f"Page(title={self.title}, content={self.content})"
    
    def setup(self):
        """Setup the page content."""
        pass

    def loop(self):
        """Main loop for the page."""
        pass

    def onOk(self):
        """Action on OK button press."""
        pass

    def onUp(self):
        """Action on UP button press."""
        pass

    def onDown(self):
        """Action on DOWN button press."""
        pass

    def onLeft(self):
        """Action on LEFT button press."""
        pass

    def onRight(self):
        """Action on RIGHT button press."""
        pass